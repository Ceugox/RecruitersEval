"""
render_preview.py — Gera HTMLs de preview dos e-mails simulando uma data específica.

Uso:
    python render_preview.py                           # Usa sexta passada, so HTML
    python render_preview.py 2026-05-29                # Data específica, so HTML
    python render_preview.py 2026-05-29 --send EMAIL   # Gera HTML + envia por email
"""

import os
import sys
import argparse
from datetime import date, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

parser = argparse.ArgumentParser()
parser.add_argument("data", nargs="?", help="Data alvo yyyy-mm-dd")
parser.add_argument("--send", metavar="EMAIL", help="Envia todos os emails para este endereco")
parser.add_argument("--recrutador", metavar="NOME", help="Processa apenas este recrutador (primeiro_nome)")
args = parser.parse_args()

# ── Data alvo ─────────────────────────────────────────────────────────────────
if args.data:
    TARGET_DATE = date.fromisoformat(args.data)
else:
    today = date.today()
    days_since_friday = (today.weekday() - 4) % 7 or 7
    TARGET_DATE = today - timedelta(days=days_since_friday)

IS_SEXTA = TARGET_DATE.weekday() == 4
_DIAS_PT = {
    0: "segunda-feira", 1: "terca-feira", 2: "quarta-feira",
    3: "quinta-feira",  4: "sexta-feira", 5: "sabado", 6: "domingo",
}
DIA_NOME = _DIAS_PT[TARGET_DATE.weekday()]

# ── Monkey-patch de date.today() nos módulos ──────────────────────────────────
class FakeDate(date):
    @classmethod
    def today(cls):
        return TARGET_DATE

import performance
import email_templates
performance.date = FakeDate
email_templates.date = FakeDate

# ── Imports após patch ────────────────────────────────────────────────────────
import json
from sheets_reader import read_sheet
from performance import (
    calcular_vagas_semana, calcular_vagas_semana_passada,
    calcular_projecao, get_tendencia, get_ultima_vaga,
    calcular_percentual, get_tipo_mensagem,
    get_week_start, calcular_resumo_mes,
)
from email_templates import render_elogio_top, render_elogio, render_motivacao, IMG_HEADER, IMG_FOOTER
from ai_generator import gerar_texto

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

meta              = config.get("meta_semanal", 10)
threshold_elogio  = config.get("threshold_elogio", 0.70)
threshold_top     = config.get("threshold_elogio_top", 1.0)
apps_script_token = config["apps_script"]["token"]
anthropic_key     = config.get("anthropic", {}).get("api_key", "")
sender_email      = config["gmail"]["sender_email"]
app_password      = config["gmail"]["app_password"]
recrutadores      = config.get("recrutadores", [])
if args.recrutador:
    recrutadores = [r for r in recrutadores if r["primeiro_nome"].lower() == args.recrutador.lower()]

print(f"[INFO] Data simulada : {TARGET_DATE.strftime('%d/%m/%Y')} ({DIA_NOME})")
print(f"[INFO] Semana        : {get_week_start().strftime('%d/%m')} a {TARGET_DATE.strftime('%d/%m')}")
print(f"[INFO] Modo          : {'ENVIAR para ' + args.send if args.send else 'somente HTML'}")
print(f"[INFO] Lendo planilha...")
records = read_sheet(apps_script_token)
print(f"[INFO] {len(records)} registros carregados.\n")

resumo_mes = calcular_resumo_mes(records, recrutadores)

OUTPUT_DIR = os.path.join(BASE_DIR, "preview")
os.makedirs(OUTPUT_DIR, exist_ok=True)

for rec in recrutadores:
    nome_planilha = rec["nome_planilha"]
    primeiro_nome = rec["primeiro_nome"]

    vagas          = calcular_vagas_semana(records, nome_planilha)
    vagas_ant      = calcular_vagas_semana_passada(records, nome_planilha)
    projecao       = calcular_projecao(vagas)
    tendencia      = get_tendencia(vagas, vagas_ant)
    ultima_vaga    = get_ultima_vaga(records, nome_planilha)
    percentual_int = round(calcular_percentual(vagas, meta) * 100)
    tipo           = get_tipo_mensagem(vagas, meta, threshold_elogio, threshold_top)

    contexto = {
        "primeiro_nome"       : primeiro_nome,
        "vagas"               : vagas,
        "meta"                : meta,
        "percentual"          : percentual_int,
        "dia_semana"          : DIA_NOME,
        "vagas_semana_passada": vagas_ant,
        "tendencia"           : tendencia,
        "projecao"            : projecao,
        "ultima_vaga"         : ultima_vaga,
        "vagas_mes"           : next(
            (r["vagas_mes"] for r in resumo_mes if r["primeiro_nome"] == primeiro_nome), 0
        ),
        "resumo_mes"          : resumo_mes,
        "tipo"                : tipo,
        "sexta"               : IS_SEXTA,
    }

    print(f"  [{tipo.upper():12s}] {primeiro_nome:10s} {vagas:2d}/{meta} vagas ({percentual_int:3d}%) — gerando texto IA...")
    texto_ia = gerar_texto(anthropic_key, contexto)

    if tipo == "elogio_top":
        template = render_elogio_top(contexto, texto_ia)
    elif tipo == "elogio":
        template = render_elogio(contexto, texto_ia)
    else:
        template = render_motivacao(contexto, texto_ia)

    html_path = os.path.join(OUTPUT_DIR, f"email_{primeiro_nome.lower()}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(template["html"])

    if args.send:
        from email_sender import send_email
        try:
            send_email(
                sender_email=sender_email,
                app_password=app_password,
                recipient_email=args.send,
                subject=f"[PREVIEW] {template['subject']}",
                html_body=template["html"],
                img_header=IMG_HEADER if os.path.exists(IMG_HEADER) else None,
                img_footer=IMG_FOOTER if os.path.exists(IMG_FOOTER) else None,
            )
            print(f"             >> enviado para {args.send}")
        except Exception as e:
            print(f"             >> ERRO ao enviar: {e}")

print(f"\n[DONE] HTMLs salvos em: {OUTPUT_DIR}")
