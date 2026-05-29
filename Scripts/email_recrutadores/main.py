"""
main.py — Entry point do sistema de e-mails semanais para recrutadores.

Valores sensíveis podem vir de variáveis de ambiente (GitHub Actions)
ou do config.json (uso local). Variáveis de ambiente têm prioridade.

Uso:
    python main.py                        # Envia e-mails para todos
    python main.py --dry-run              # Imprime no console, não envia
    python main.py --test SEU@EMAIL.COM   # Envia tudo para um e-mail de teste
    python main.py --recrutador "Nome"    # Envia apenas para um recrutador
"""

import argparse
import json
import os
import sys
from datetime import date

from sheets_reader import read_sheet
from performance import (calcular_vagas_semana, calcular_vagas_semana_passada,
                         calcular_projecao, get_tendencia, get_ultima_vaga,
                         calcular_percentual, get_tipo_mensagem,
                         get_week_start, calcular_resumo_mes)
from email_templates import render_elogio_top, render_elogio, render_motivacao, IMG_HEADER, IMG_FOOTER
from email_sender import send_email
from ai_generator import gerar_texto


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        print(f"[ERRO] config.json não encontrado em {BASE_DIR}")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve(config_value: str, env_var: str) -> str:
    """Retorna env var se definida, senão valor do config."""
    return os.environ.get(env_var) or config_value


def get_threshold(config: dict) -> float:
    """Mantido por compatibilidade — não usado com os 3 níveis."""
    return config.get("threshold_elogio", 0.70)


def _dia_semana_local() -> str:
    nomes = {
        0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
        3: "quinta-feira",  4: "sexta-feira", 5: "sábado", 6: "domingo",
    }
    return nomes[date.today().weekday()]


def main():
    parser = argparse.ArgumentParser(
        description="Dispara e-mails de performance para recrutadores."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Imprime e-mails no console sem enviar.",
    )
    parser.add_argument(
        "--test",
        metavar="EMAIL",
        help="Envia todos os e-mails para este endereço (validação).",
    )
    parser.add_argument(
        "--recrutador",
        metavar="NOME",
        help="Envia apenas para o recrutador com este primeiro_nome.",
    )
    args = parser.parse_args()

    config = load_config()

    meta = config.get("meta_semanal", 10)
    threshold = get_threshold(config)

    # Valores sensíveis: env var tem prioridade sobre config.json
    apps_script_token = resolve(config["apps_script"]["token"], "APPS_SCRIPT_TOKEN")
    sheet_name = config["google_sheets"]["sheet_name"]
    sender_email = resolve(config["gmail"]["sender_email"], "GMAIL_SENDER")
    app_password = resolve(config["gmail"]["app_password"], "GMAIL_APP_PASSWORD")

    anthropic_api_key = resolve(config.get("anthropic", {}).get("api_key", ""), "ANTHROPIC_API_KEY")

    threshold_elogio = config.get("threshold_elogio", 0.70)
    threshold_top    = config.get("threshold_elogio_top", 1.0)

    recrutadores = config.get("recrutadores", [])

    if args.recrutador:
        recrutadores = [
            r for r in recrutadores
            if r["primeiro_nome"].lower() == args.recrutador.lower()
        ]
        if not recrutadores:
            print(f"[ERRO] Recrutador '{args.recrutador}' não encontrado no config.json")
            sys.exit(1)

    print(f"[INFO] Lendo planilha '{sheet_name}' via Apps Script...")
    records = read_sheet(apps_script_token)
    print(f"[INFO] {len(records)} registros carregados.")

    week_start = get_week_start()
    print(
        f"[INFO] Semana: {week_start.strftime('%d/%m')} a {date.today().strftime('%d/%m/%Y')}"
    )
    print(f"[INFO] Meta: {meta} vagas | Threshold elogio: {threshold*100:.0f}%\n")

    # Resumo mensal calculado uma vez para todos (usa lista completa de recrutadores)
    resumo_mes = calcular_resumo_mes(records, config.get("recrutadores", []))

    results = []

    for rec in recrutadores:
        nome_planilha = rec["nome_planilha"]
        primeiro_nome = rec["primeiro_nome"]
        email_destino = args.test if args.test else rec["email"]

        vagas = calcular_vagas_semana(records, nome_planilha)
        vagas_ant = calcular_vagas_semana_passada(records, nome_planilha)
        projecao = calcular_projecao(vagas)
        tendencia = get_tendencia(vagas, vagas_ant)
        ultima_vaga = get_ultima_vaga(records, nome_planilha)
        percentual_int = round(calcular_percentual(vagas, meta) * 100)
        sexta = date.today().weekday() == 4
        tipo = get_tipo_mensagem(vagas, meta, threshold_elogio, threshold_top)

        contexto = {
            "primeiro_nome": primeiro_nome,
            "vagas": vagas,
            "meta": meta,
            "percentual": percentual_int,
            "dia_semana": _dia_semana_local(),
            "vagas_semana_passada": vagas_ant,
            "tendencia": tendencia,
            "projecao": projecao,
            "ultima_vaga": ultima_vaga,
            "vagas_mes": next(
                (r["vagas_mes"] for r in resumo_mes if r["primeiro_nome"] == primeiro_nome), 0
            ),
            "resumo_mes": resumo_mes,
            "tipo": tipo,
            "sexta": sexta,
        }

        # Gera texto via IA (retorna None se não configurado ou erro)
        texto_ia = gerar_texto(anthropic_api_key, contexto) if not args.dry_run else None

        if tipo == "elogio_top":
            template = render_elogio_top(contexto, texto_ia)
        elif tipo == "elogio":
            template = render_elogio(contexto, texto_ia)
        else:
            template = render_motivacao(contexto, texto_ia)

        tipo = tipo.upper()

        subject = template["subject"]
        html_body = template["html"]

        if args.dry_run:
            print(f"--- [{tipo}] {primeiro_nome} ({vagas}/{meta} vagas = {percentual_int}%) ---")
            print(f"Para: {email_destino}")
            print(f"Assunto: {subject}")
            print(f"[HTML gerado — {len(html_body)} chars]\n")
        else:
            try:
                send_email(
                    sender_email=sender_email,
                    app_password=app_password,
                    recipient_email=email_destino,
                    subject=subject,
                    html_body=html_body,
                    img_header=IMG_HEADER if os.path.exists(IMG_HEADER) else None,
                    img_footer=IMG_FOOTER if os.path.exists(IMG_FOOTER) else None,
                )
                status = "OK"
            except Exception as e:
                status = f"ERRO: {e}"

            print(
                f"[{status}] [{tipo}] {primeiro_nome} - {email_destino} "
                f"({vagas}/{meta} vagas = {percentual_int}%)"
            )

        results.append({
            "nome": primeiro_nome,
            "vagas": vagas,
            "percentual": f"{percentual_int}%",
            "tipo": tipo,
            "email": email_destino,
        })

    print("\n=== RESUMO ===")
    for r in results:
        print(
            f"  {r['nome']:20s} {r['vagas']:2d} vagas ({r['percentual']:>4s}) - {r['tipo']}"
        )
    print(f"\nTotal: {len(results)} recrutador(es) processado(s).")


if __name__ == "__main__":
    main()
