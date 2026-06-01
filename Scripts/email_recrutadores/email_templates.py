"""
email_templates.py — Templates HTML de e-mail (elogio + motivação).

Imagens enviadas como CID (inline attachments).
"""

import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", ".."))
ASSETS_DIR = os.path.join(ROOT_DIR, "Assets")

IMG_HEADER = os.path.join(ASSETS_DIR, "email_header.png")
IMG_FOOTER = os.path.join(ASSETS_DIR, "email_footer.png")

CID_HEADER = "header_raiz"
CID_FOOTER = "footer_raiz"

# ── Paleta Raíz ──────────────────────────────────────────────────────────────
AZUL    = "#1565C0"
LARANJA = "#F7941D"
TEAL    = "#7EC8C8"
BRANCO  = "#FFFFFF"


def _dia_semana_pt() -> str:
    nomes = {
        0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
        3: "quinta-feira",  4: "sexta-feira", 5: "sábado", 6: "domingo",
    }
    return nomes[date.today().weekday()]


def _mes_pt() -> str:
    meses = {
        1: "janeiro", 2: "fevereiro", 3: "março",    4: "abril",
        5: "maio",    6: "junho",     7: "julho",     8: "agosto",
        9: "setembro",10: "outubro",  11: "novembro", 12: "dezembro",
    }
    return meses[date.today().month]


# ── Cabeçalho / Rodapé (fallback HTML caso imagens não existam) ───────────────
HEADER_HTML = f"""
<table width="600" cellpadding="0" cellspacing="0"
       style="background:{AZUL};width:100%;max-width:600px;">
  <tr>
    <!-- Texto RAIZ COMUNICA -->
    <td width="220" style="padding:28px 0 0 32px;vertical-align:top;">
      <span style="font-family:Arial Black,Arial,sans-serif;font-weight:900;
                   font-size:34px;color:{BRANCO};line-height:1.05;
                   letter-spacing:-0.5px;display:block;">
        RAIZ<br>COMUNICA
      </span>
    </td>
    <!-- Onda laranja + teal + estrela (SVG inline) -->
    <td style="padding:0;vertical-align:bottom;text-align:right;">
      <svg width="340" height="90" viewBox="0 0 340 90"
           xmlns="http://www.w3.org/2000/svg" style="display:block;">
        <!-- Onda teal (fundo) -->
        <path d="M0,90 Q120,30 200,55 Q270,75 340,20 L340,90 Z"
              fill="{TEAL}" opacity="0.85"/>
        <!-- Onda laranja (frente) -->
        <path d="M0,90 Q100,20 190,48 Q260,68 340,10 L340,90 Z"
              fill="{LARANJA}"/>
        <!-- Linha tracejada branca -->
        <path d="M10,78 Q110,18 195,44 Q262,64 335,8"
              fill="none" stroke="{BRANCO}" stroke-width="2"
              stroke-dasharray="6,5" opacity="0.8"/>
        <!-- Estrela -->
        <polygon points="310,4 314,16 326,16 317,23 320,35 310,28 300,35 303,23 294,16 306,16"
                 fill="{BRANCO}" stroke="{LARANJA}" stroke-width="1.5"/>
        <!-- Texto tagline -->
        <text x="198" y="36" fill="{LARANJA}"
              font-family="Arial,sans-serif" font-size="8.5"
              font-weight="bold" letter-spacing="0.3">OUSAMOS EM BUSCA</text>
        <text x="198" y="48" fill="{LARANJA}"
              font-family="Arial,sans-serif" font-size="8.5"
              font-weight="bold" letter-spacing="0.3">DE MELHORES</text>
        <text x="198" y="60" fill="{LARANJA}"
              font-family="Arial,sans-serif" font-size="8.5"
              font-weight="bold" letter-spacing="0.3">SOLUÇÕES.</text>
      </svg>
    </td>
  </tr>
</table>"""


# ── Rodapé ────────────────────────────────────────────────────────────────────
FOOTER_HTML = f"""
<table width="600" cellpadding="0" cellspacing="0"
       style="width:100%;max-width:600px;background:{AZUL};">
  <tr>
    <td style="padding:0;">
      <svg width="600" height="70" viewBox="0 0 600 70"
           xmlns="http://www.w3.org/2000/svg" style="display:block;">
        <!-- Fundo branco acima da onda -->
        <rect width="600" height="35" fill="{BRANCO}"/>
        <!-- Onda laranja -->
        <path d="M0,0 Q150,60 300,30 Q450,0 600,50 L600,70 L0,70 Z"
              fill="{LARANJA}"/>
        <!-- Azul abaixo -->
        <rect y="50" width="600" height="20" fill="{AZUL}"/>
      </svg>
    </td>
  </tr>
  <!-- Logo Raíz texto -->
  <tr>
    <td style="background:{AZUL};padding:6px 24px 18px;text-align:right;">
      <span style="font-family:Arial Black,Arial,sans-serif;font-weight:900;
                   font-size:18px;color:{BRANCO};letter-spacing:1px;">RAIZ</span>
      <span style="font-family:Arial,sans-serif;font-size:10px;
                   color:{BRANCO};display:block;text-align:right;
                   letter-spacing:2px;margin-top:-2px;">educação</span>
    </td>
  </tr>
</table>"""


# ── Tabela de ranking mensal ───────────────────────────────────────────────────
def _tabela_mes_html(resumo_mes: list[dict], primeiro_nome_atual: str) -> str:
    medalhas = ["🥇", "🥈", "🥉"]
    linhas = ""
    for i, rec in enumerate(resumo_mes):
        destaque = rec["primeiro_nome"] == primeiro_nome_atual
        bg     = "#FFF3E0" if destaque else ("#F4F8FF" if i % 2 == 0 else BRANCO)
        peso   = "bold"   if destaque else "normal"
        cor    = AZUL     if destaque else "#333333"
        pos    = medalhas[i] if i < 3 else f"{i+1}."
        borda  = f"border-left:3px solid {LARANJA};" if destaque else ""
        linhas += f"""
        <tr style="background:{bg};{borda}">
          <td style="padding:11px 14px;font-size:16px;">{pos}</td>
          <td style="padding:11px 14px;font-weight:{peso};color:{cor};font-size:14px;">
            {rec['primeiro_nome']}
          </td>
          <td style="padding:11px 14px;text-align:center;font-weight:{peso};
                     color:{cor};font-size:14px;">{rec['vagas_mes']}</td>
          <td style="padding:11px 14px;text-align:right;font-size:12px;color:#888;">
            {"&nbsp;você!" if destaque else ""}
          </td>
        </tr>"""

    mes = _mes_pt().capitalize()
    return f"""
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-collapse:collapse;margin-top:28px;
              border:1px solid #DDDDDD;border-radius:6px;overflow:hidden;">
  <tr style="background:{AZUL};">
    <th colspan="4"
        style="padding:13px 16px;color:{BRANCO};font-size:14px;
               text-align:left;font-weight:bold;letter-spacing:0.3px;">
      Ranking do mês — {mes} {date.today().year}
    </th>
  </tr>
  <tr style="background:#1976D2;">
    <th style="padding:8px 14px;color:{BRANCO};font-size:11px;
               text-align:left;font-weight:normal;width:40px;"></th>
    <th style="padding:8px 14px;color:{BRANCO};font-size:11px;
               text-align:left;font-weight:normal;">Consultor</th>
    <th style="padding:8px 14px;color:{BRANCO};font-size:11px;
               text-align:center;font-weight:normal;width:70px;">Vagas</th>
    <th style="width:50px;"></th>
  </tr>
  {linhas}
</table>"""


# ─────────────────────────────────────────────────────────────────────────────
# Pools de fallback (usados quando a IA não está disponível)
# Organização: dia × tipo  →  6 pools distintos
#
#   QUARTA — incentivo + análise de ritmo + projeção até sexta
#   SEXTA  — conclusão da semana + bom descanso
# ─────────────────────────────────────────────────────────────────────────────

# ── QUARTA ────────────────────────────────────────────────────────────────────

_QUARTA_ELOGIO_TOP = [
    ("É {dia} e a meta já está batida, {nome}! {vagas} vagas — {percentual}% — e ainda sobram dois dias.\n"
     "Aproveita esse ritmo e vê até onde você chega. O time todo tá olhando!"),
    ("{nome}, {vagas} vagas na {dia} e a meta no bolso! {extra}Ritmo excelente — a semana tá sendo sua.\n"
     "Com dois dias ainda pela frente, até onde você consegue ir? Continua assim!"),
    ("Que ritmo, {nome}! Meta batida já na {dia}: {vagas} vagas, {percentual}%.\n"
     "No mês você já acumula {vagas_mes} vagas. Dois dias ainda pela frente — bora empilhar mais?"),
]

_QUARTA_ELOGIO = [
    ("É {dia} e você está com {vagas} vagas — {percentual}% da meta. Bom ritmo!\n"
     "A projeção aponta para {projecao} vagas até sexta. Faltam {faltam} pra bater — dá mais que tempo, vai com tudo!"),
    ("{nome}, {vagas} vagas nessa {dia} — você tá bem encaminhado!\n"
     "Se manter esse passo, a projeção é de {projecao} até sexta. Os {faltam} que faltam estão ao alcance."),
    ("Lindo ritmo, {nome}! {vagas} vagas até a {dia}, {percentual}% da meta.\n"
     "A projeção é {projecao} no fechamento da semana — {faltam} vagas pra meta. Tá perto demais pra parar agora."),
]

_QUARTA_MOTIVACAO = [
    ("{nome}, é {dia} e você está com {vagas} vagas. A projeção aponta para {projecao} até sexta.\n"
     "Ainda dá pra virar — quinta e sexta são seus. Foco total e vai nessa!"),
    ("É {dia}, {nome}. {vagas} vagas até agora, e o melhor ainda está por vir.\n"
     "Com o ritmo certo nesses dois dias, a projeção pode chegar a {projecao}. O jogo ainda está aberto!"),
    ("{nome}, {vagas} vagas na {dia} e dois dias inteiros pela frente.\n"
     "Projeção de {projecao} até sexta se você acelerar agora. Dois dias, foco total — bora!"),
]

# ── SEXTA ─────────────────────────────────────────────────────────────────────

_SEXTA_ELOGIO_TOP = [
    ("Que semana, {nome}! Meta batida e encerrada com {vagas} vagas — {percentual}%, {diff_semana} em relação à semana passada.\n"
     "Você merece descansar esse final de semana. Segunda-feira a gente começa do zero — e você já sabe o nível!"),
    ("{nome}, semana incrível: {vagas} vagas, meta batida, {extra}e ainda {diff_semana} comparado à semana passada.\n"
     "No mês você acumula {vagas_mes}. Aproveita o descanso — semana que vem o bar vai ser ainda mais alto!"),
    ("É {dia} e a semana foi sua, {nome}! {vagas} vagas fechadas, {percentual}% da meta.\n"
     "Esse é o padrão. Descansa com merecimento — semana que vem a gente mantém esse nível!"),
]

_SEXTA_ELOGIO = [
    ("{nome}, semana encerrada com {vagas} vagas — {percentual}% da meta, {diff_semana} na comparação com a semana passada.\n"
     "Foi uma boa semana! Descansa bem — segunda-feira a gente vem pra bater a meta completa."),
    ("É {dia}, {nome}! {vagas} vagas no bolso essa semana, {vagas_mes} no mês. {diff_semana} em relação à semana passada.\n"
     "Chegou perto — semana que vem você fecha. Bom descanso!"),
    ("{nome}, semana de {vagas} vagas e bom ritmo — {diff_semana} comparado à semana passada.\n"
     "Aproveita o final de semana para recarregar. Na próxima, a meta vem!"),
]

_SEXTA_MOTIVACAO = [
    ("{nome}, semana encerrada com {vagas} vagas — {percentual}% da meta. {diff_semana} em relação à semana passada.\n"
     "Descansa esse final de semana com tudo. Segunda começa do zero e a próxima semana vai ser diferente!"),
    ("É {dia}, {nome}. {vagas} vagas essa semana, {vagas_mes} no mês. {diff_semana} na comparação com a semana passada.\n"
     "Merece descansar — segunda-feira a gente retoma com tudo e vira o jogo."),
    ("{nome}, semana encerrada. {vagas} vagas, {diff_semana} em relação à semana passada.\n"
     "Aproveita o descanso — a próxima semana é uma nova largada. Semana que vem a história vai ser outra!"),
]

# ── Roteador de pools ──────────────────────────────────────────────────────────
_POOLS = {
    (False, "elogio_top"): _QUARTA_ELOGIO_TOP,
    (False, "elogio"):     _QUARTA_ELOGIO,
    (False, "motivacao"):  _QUARTA_MOTIVACAO,
    (True,  "elogio_top"): _SEXTA_ELOGIO_TOP,
    (True,  "elogio"):     _SEXTA_ELOGIO,
    (True,  "motivacao"):  _SEXTA_MOTIVACAO,
}


def _formatar_diff(vagas_atual: int, vagas_anterior: int) -> str:
    diff = vagas_atual - vagas_anterior
    if diff > 0:
        return f"{diff} {'vaga a mais' if diff == 1 else 'vagas a mais'}"
    if diff < 0:
        return f"{abs(diff)} {'vaga a menos' if abs(diff) == 1 else 'vagas a menos'}"
    return "mesmo ritmo"


def _selecionar_template(pool: list, nome: str) -> str:
    """Seleciona template do pool de forma consistente por nome + semana ISO."""
    from datetime import date
    idx = (hash(nome + str(date.today().isocalendar()[1])) & 0xFFFF) % len(pool)
    return pool[idx]


def _render(contexto: dict, pool: list) -> str:
    """Renderiza template com os dados do contexto."""
    nome        = contexto["primeiro_nome"]
    vagas       = contexto["vagas"]
    meta        = contexto["meta"]
    percentual  = contexto["percentual"]
    dia         = contexto["dia_semana"]
    vagas_ant   = contexto.get("vagas_semana_passada", 0)
    projecao    = contexto.get("projecao", vagas)
    vagas_mes   = contexto.get("vagas_mes", 0)
    faltam      = max(0, meta - vagas)
    diff        = _formatar_diff(vagas, vagas_ant)

    tmpl = _selecionar_template(pool, nome)
    # Substitui placeholders simples
    return (tmpl
        .replace("{nome}", nome)
        .replace("{dia}", dia)
        .replace("{vagas}", str(vagas))
        .replace("{meta}", str(meta))
        .replace("{percentual}", str(percentual))
        .replace("{projecao}", str(projecao))
        .replace("{vagas_mes}", str(vagas_mes))
        .replace("{faltam}", str(faltam))
        .replace("{diff_semana}", diff)
        .replace("{extra}", f"{vagas - meta} acima! " if vagas > meta else "")
    )


def _corpo_para_html(texto: str) -> str:
    """Converte \n em parágrafos HTML."""
    return "".join(
        f'<p style="margin:0 0 18px 0;font-size:16px;line-height:1.7;color:#333333;">{p}</p>'
        for p in texto.strip().split("\n")
        if p.strip()
    )


def _montar_template(contexto: dict, pool: list, texto_ia: str | None) -> dict:
    """Monta o dict final com subject e html."""
    corpo_texto = texto_ia if texto_ia else _render(contexto, pool)
    paragrafos  = _corpo_para_html(corpo_texto)

    # Destaque da última vaga (aparece após os parágrafos se texto não vier da IA)
    destaque = ""
    ultima = contexto.get("ultima_vaga")
    if ultima and not texto_ia:
        cargo   = ultima.get("cargo", "")
        unidade = ultima.get("unidade", "")
        local   = f" · {unidade}" if unidade else ""
        destaque = (
            f'<p style="margin:0 0 18px 0;font-size:14px;line-height:1.6;'
            f'color:#555;border-left:3px solid {LARANJA};padding-left:12px;">'
            f'Último fechamento: <strong>{cargo}</strong>{local}</p>'
        ) if cargo else ""

    tabela  = _tabela_mes_html(contexto.get("resumo_mes", []), contexto["primeiro_nome"])
    html    = _build_html(paragrafos + destaque, tabela)
    return {"subject": contexto["subject"], "html": html}


# ── Builder principal ──────────────────────────────────────────────────────────
def _build_html(paragrafos: str, tabela: str) -> str:
    header = (
        f'<img src="cid:{CID_HEADER}" alt="Raiz Comunica" '
        f'style="width:100%;max-width:600px;display:block;"/>'
        if os.path.exists(IMG_HEADER) else HEADER_HTML
    )
    footer = (
        f'<img src="cid:{CID_FOOTER}" alt="Raiz Educacao" '
        f'style="width:100%;max-width:600px;display:block;"/>'
        if os.path.exists(IMG_FOOTER) else FOOTER_HTML
    )
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/></head>
<body style="margin:0;padding:0;background:#F0F4F8;font-family:Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#F0F4F8;padding:28px 0;">
  <tr><td align="center">
    <table width="600" cellpadding="0" cellspacing="0"
           style="max-width:600px;width:100%;background:#FFFFFF;border-radius:10px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,0.10);">
      <tr><td style="padding:0;">{header}</td></tr>
      <tr><td style="padding:36px 40px 8px;">{paragrafos}</td></tr>
      <tr><td style="padding:0 40px 32px;">{tabela}</td></tr>
      <tr><td style="padding:0 40px 20px;">
        <p style="margin:16px 0 0;font-size:12px;color:#AAAAAA;border-top:1px solid #EEEEEE;padding-top:16px;">
          Mensagem automática · Sistema de Acompanhamento P&amp;C · Raíz Educação
        </p>
      </td></tr>
      <tr><td style="padding:0;">{footer}</td></tr>
    </table>
  </td></tr>
</table>
</body>
</html>"""


# ── Subjects por dia × tipo ────────────────────────────────────────────────────
_SUBJECTS = {
    (False, "elogio_top"): "{nome}, META BATIDA na quarta! Ritmo incrível!",
    (False, "elogio"):     "{nome}, você tá voando essa semana!",
    (False, "motivacao"):  "{nome}, a semana ainda não acabou!",
    (True,  "elogio_top"): "{nome}, META BATIDA! Que semana incrível!",
    (True,  "elogio"):     "{nome}, boa semana! Bom descanso!",
    (True,  "motivacao"):  "{nome}, bom descanso e até segunda!",
}


# ── Templates públicos ─────────────────────────────────────────────────────────
def render_elogio_top(contexto: dict, texto_ia: str | None = None) -> dict:
    sexta = contexto.get("sexta", False)
    contexto["subject"] = _SUBJECTS[(sexta, "elogio_top")].replace("{nome}", contexto["primeiro_nome"])
    return _montar_template(contexto, _POOLS[(sexta, "elogio_top")], texto_ia)


def render_elogio(contexto: dict, texto_ia: str | None = None) -> dict:
    sexta = contexto.get("sexta", False)
    contexto["subject"] = _SUBJECTS[(sexta, "elogio")].replace("{nome}", contexto["primeiro_nome"])
    return _montar_template(contexto, _POOLS[(sexta, "elogio")], texto_ia)


def render_motivacao(contexto: dict, texto_ia: str | None = None) -> dict:
    sexta = contexto.get("sexta", False)
    contexto["subject"] = _SUBJECTS[(sexta, "motivacao")].replace("{nome}", contexto["primeiro_nome"])
    return _montar_template(contexto, _POOLS[(sexta, "motivacao")], texto_ia)


def _render_motivacao_legado(contexto: dict, texto_ia: str | None = None) -> dict:
    sexta = contexto.get("sexta", False)
    if sexta:
        contexto["subject"] = f"{contexto['primeiro_nome']}, bom descanso e até segunda!"
        return _montar_template(contexto, _SEXTA_MOTIVACAO, texto_ia)
    else:
        contexto["subject"] = f"{contexto['primeiro_nome']}, a semana ainda não acabou!"
        return _montar_template(contexto, _QUARTA_MOTIVACAO, texto_ia)
