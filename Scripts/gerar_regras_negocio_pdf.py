"""
Gerador de PDF — Regras de Negócio do Dashboard P&C
Raíz Educação · Pessoas e Cultura
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_raiz.png")

# ── Paleta ─────────────────────────────────────────────────────
C_DARK   = HexColor("#16432a")
C_MID    = HexColor("#1f6b40")
C_LIGHT  = HexColor("#2a9d5c")
C_PALE   = HexColor("#e4f4ec")
C_GOLD   = HexColor("#e8a020")
C_GOLDLT = HexColor("#fef3d8")
C_WHITE  = colors.white
C_GRAY   = HexColor("#f3f4f6")
C_GBORD  = HexColor("#d1d5db")
C_RED    = HexColor("#dc2626")
C_REDBG  = HexColor("#fef2f2")
C_AMBER  = HexColor("#d97706")
C_AMBBG  = HexColor("#fffbeb")
C_TXTD   = HexColor("#111827")
C_TXTM   = HexColor("#374151")
C_TXTMU  = HexColor("#6b7280")

PW, PH = A4
MARGIN_L = 2.0 * cm
MARGIN_R = 2.0 * cm
MARGIN_T = 2.5 * cm
MARGIN_B = 2.0 * cm
CONTENT_W = PW - MARGIN_L - MARGIN_R

# ── Estilos ────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def sty(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

S_TITLE    = sty("Title2",    fontName="Helvetica-Bold",   fontSize=22, textColor=C_WHITE,  leading=28, spaceAfter=0)
S_SUBTITLE = sty("Sub2",      fontName="Helvetica",        fontSize=11, textColor=HexColor("#c8e8d8"), leading=14, spaceAfter=0)
S_SECTION  = sty("Sec",       fontName="Helvetica-Bold",   fontSize=13, textColor=C_WHITE,  leading=16)
S_RN_TITLE = sty("RNTitle",   fontName="Helvetica-Bold",   fontSize=12, textColor=C_DARK,   leading=15, spaceBefore=4, spaceAfter=4)
S_BODY     = sty("Body2",     fontName="Helvetica",        fontSize=9.5, textColor=C_TXTM,  leading=14, spaceAfter=0, alignment=TA_JUSTIFY)
S_NOTE     = sty("Note",      fontName="Helvetica-Oblique",fontSize=8.5, textColor=C_TXTMU, leading=12, spaceAfter=0)
S_CODE     = sty("Code",      fontName="Courier",          fontSize=8,   textColor=C_DARK,  leading=11, backColor=C_GRAY, spaceAfter=0)
S_TH       = sty("TH",        fontName="Helvetica-Bold",   fontSize=8.5, textColor=C_WHITE, leading=11)
S_TD       = sty("TD",        fontName="Helvetica",        fontSize=8.5, textColor=C_TXTM,  leading=11)
S_TD_BOLD  = sty("TDB",       fontName="Helvetica-Bold",   fontSize=8.5, textColor=C_TXTD,  leading=11)
S_FOOTER   = sty("Footer",    fontName="Helvetica",        fontSize=7.5, textColor=C_TXTMU, leading=10)
S_TOC_ITEM = sty("TOC",       fontName="Helvetica",        fontSize=10,  textColor=C_TXTM,  leading=16)
S_TOC_RN   = sty("TOCRN",     fontName="Helvetica-Bold",   fontSize=10,  textColor=C_DARK,  leading=16)

# ── Helpers ────────────────────────────────────────────────────
def p(text, style=None):
    return Paragraph(text, style or S_BODY)

def sp(h=0.3):
    return Spacer(1, h * cm)

def hr(color=C_GBORD, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=4, spaceBefore=4)

def condition_table(rows, accent=C_DARK):
    """rows = list of (campo, regra) tuples"""
    data = [[p("Campo / Condição", S_TH), p("Regra", S_TH)]]
    for campo, regra in rows:
        data.append([p(campo, S_TD_BOLD), p(regra, S_TD)])
    t = Table(data, colWidths=[CONTENT_W * 0.38, CONTENT_W * 0.62])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  accent),
        ("BACKGROUND",  (0, 1), (-1, 1),  C_PALE),
        ("BACKGROUND",  (0, 2), (-1, 2),  C_WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_PALE, C_WHITE]),
        ("GRID",        (0, 0), (-1, -1), 0.4, C_GBORD),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",(0, 0), (-1, -1), 7),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
    ]))
    return t

def wide_table(headers, rows, col_widths=None, accent=C_DARK):
    """Generic table with header row"""
    col_widths = col_widths or [CONTENT_W / len(headers)] * len(headers)
    data = [[p(h, S_TH) for h in headers]]
    for i, row in enumerate(rows):
        bg = C_PALE if i % 2 == 0 else C_WHITE
        data.append([p(str(cell), S_TD_BOLD if j == 0 else S_TD)
                     for j, cell in enumerate(row)])
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  accent),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [C_PALE, C_WHITE]),
        ("GRID",          (0, 0), (-1, -1), 0.4, C_GBORD),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    return t

def note_box(text, accent=C_MID, bg=C_PALE):
    data = [[p(f"<b>ℹ</b>  {text}", S_NOTE)]]
    t = Table(data, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), bg),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LINEBEFORE",   (0, 0), (0, -1),  3, accent),
    ]))
    return t

def warn_box(text):
    return note_box(text, accent=C_AMBER, bg=C_AMBBG)

def rn_header(code, title, accent=C_DARK):
    """Renders the RN-XX badge + title inline via a Table"""
    badge = p(f"<b>{code}</b>", ParagraphStyle("badge", fontName="Helvetica-Bold",
              fontSize=9, textColor=C_WHITE, leading=11))
    tit   = p(f"<b>{title}</b>", ParagraphStyle("rntit", fontName="Helvetica-Bold",
              fontSize=12, textColor=C_WHITE, leading=15))
    t = Table([[badge, tit]], colWidths=[1.6*cm, CONTENT_W - 1.6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), accent),
        ("TOPPADDING",   (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
        ("LEFTPADDING",  (0, 0), (0, -1),  8),
        ("LEFTPADDING",  (1, 0), (1, -1),  6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t

def section_break(title):
    """Full-width section separator band"""
    t = Table([[p(f"<b>{title}</b>", S_SECTION)]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), C_MID),
        ("TOPPADDING",   (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
        ("LEFTPADDING",  (0, 0), (-1, -1), 12),
    ]))
    return t

def formula_box(lines):
    """Monospaced formula/code block"""
    text = "<br/>".join(lines)
    t = Table([[p(text, S_CODE)]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), C_GRAY),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING",   (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
        ("LINEBEFORE",   (0, 0), (0, -1),  3, C_MID),
    ]))
    return t

# ── Header/Footer de página ─────────────────────────────────────
class PageHeader:
    def __init__(self, doc):
        self.doc = doc

def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Header bar
    canvas.setFillColor(C_DARK)
    canvas.rect(0, h - 1.4*cm, w, 1.4*cm, fill=1, stroke=0)
    # Gold accent line
    canvas.setFillColor(C_GOLD)
    canvas.rect(0, h - 1.4*cm - 0.12*cm, w, 0.12*cm, fill=1, stroke=0)
    # Header text left
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(C_WHITE)
    canvas.drawString(MARGIN_L, h - 0.95*cm, "Raíz Educação · Pessoas e Cultura")
    # Header text right
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#c8e8d8"))
    canvas.drawRightString(w - MARGIN_R, h - 0.95*cm, "Dashboard Estratégico P&C — Regras de Negócio")
    # Footer line
    canvas.setStrokeColor(C_GBORD)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, 1.3*cm, w - MARGIN_R, 1.3*cm)
    # Footer left
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(C_TXTMU)
    canvas.drawString(MARGIN_L, 0.85*cm, "Confidencial · Uso interno")
    # Footer right (page number)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(C_MID)
    canvas.drawRightString(w - MARGIN_R, 0.85*cm, f"Página {doc.page}")
    canvas.restoreState()

def on_first_page(canvas, doc):
    canvas.saveState()
    w, h = A4

    # ── Cover band ──────────────────────────────────────────────────
    canvas.setFillColor(C_DARK)
    canvas.rect(0, h - 7.5*cm, w, 7.5*cm, fill=1, stroke=0)
    canvas.setFillColor(C_GOLD)
    canvas.rect(0, h - 7.5*cm - 0.15*cm, w, 0.15*cm, fill=1, stroke=0)

    # ── Raíz Educação logo (imagem PNG — lado direito da faixa) ─────
    logo_w = 3.4*cm
    logo_h = logo_w * (168 / 140)   # mantém proporção original
    logo_x = w - MARGIN_R - logo_w
    logo_y = h - 3.75*cm - logo_h / 2  # centralizado na faixa
    canvas.drawImage(LOGO_PATH, logo_x, logo_y,
                     width=logo_w, height=logo_h, mask='auto')

    # ── Left side text ───────────────────────────────────────────────
    # Org label
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(C_GOLD)
    canvas.drawString(MARGIN_L, h - 1.5*cm, "RAÍZ EDUCAÇÃO · PESSOAS E CULTURA")

    # Tag pill — text sized to fit inside pill
    pill_text = "REGRAS DE NEGÓCIO"
    pill_w    = 4.0*cm
    pill_h    = 0.5*cm
    pill_y    = h - 2.45*cm
    canvas.setFillColor(C_GOLD)
    canvas.roundRect(MARGIN_L, pill_y, pill_w, pill_h, 4, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(C_DARK)
    canvas.drawString(MARGIN_L + 0.22*cm, pill_y + 0.14*cm, pill_text)

    # Main title
    canvas.setFont("Helvetica-Bold", 28)
    canvas.setFillColor(C_WHITE)
    canvas.drawString(MARGIN_L, h - 3.75*cm, "Regras de Negócio")

    # Section subtitle
    canvas.setFont("Helvetica-Bold", 19)
    canvas.setFillColor(C_GOLD)
    canvas.drawString(MARGIN_L, h - 4.7*cm, "Dashboard Estratégico P&C")

    # Description line
    canvas.setFont("Helvetica", 10)
    canvas.setFillColor(HexColor("#b0d8c0"))
    canvas.drawString(MARGIN_L, h - 5.5*cm,
        "Definições formais de métricas, condições e thresholds")

    # Meta row
    meta = [("Versão", "1.2 — Maio 2026"), ("Área", "Pessoas e Cultura"), ("Classificação", "Confidencial")]
    for i, (lbl, val) in enumerate(meta):
        xi = MARGIN_L + i * 5.5*cm
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(HexColor("#7aad90"))
        canvas.drawString(xi, h - 6.65*cm, lbl.upper())
        canvas.setFont("Helvetica-Bold", 9)
        canvas.setFillColor(C_WHITE)
        canvas.drawString(xi, h - 7.0*cm, val)

    # ── Footer ───────────────────────────────────────────────────────
    canvas.setStrokeColor(C_GBORD)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, 1.3*cm, w - MARGIN_R, 1.3*cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(C_TXTMU)
    canvas.drawString(MARGIN_L, 0.85*cm, "Confidencial · Uso interno")
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(C_MID)
    canvas.drawRightString(w - MARGIN_R, 0.85*cm, f"Página {doc.page}")
    canvas.restoreState()

# ══════════════════════════════════════════════════════════════
# CONTEÚDO
# ══════════════════════════════════════════════════════════════
story = []

# ── Espaço abaixo da capa ──────────────────────────────────────
story.append(sp(7.8))   # empurra para baixo do bloco de capa

# ── Sumário ────────────────────────────────────────────────────
story.append(section_break("Índice de Regras de Negócio"))
story.append(sp(0.4))

toc_data = [
    ("RN-01", "Vaga Fechada por R&S"),
    ("RN-02", "Vaga Fechada por Admissão"),
    ("RN-03", "Vaga Aberta (pipeline R&S)"),
    ("RN-04", "Vaga em Processo de Admissão"),
    ("RN-05", "Vaga Congelada"),
    ("RN-06", "Vaga Cancelada"),
    ("RN-07", "SLA de R&S — Tempo de Recrutamento"),
    ("RN-08", "SLA de Admissão — Tempo de Onboarding"),
    ("RN-09", "SLA Total"),
    ("RN-10", "Aging de Vaga Aberta"),
    ("RN-11", "Faixas de Aging"),
    ("RN-12", "Vagas Críticas (threshold > 30 dias)"),
    ("RN-13", "Taxa de Cumprimento do SLA de R&S"),
    ("RN-14", "Taxa de Cumprimento do SLA de Admissão"),
    ("RN-15", "Taxa de Cancelamento"),
    ("RN-16", "Performance do Recrutador — Janela de 3 Meses"),
    ("RN-17", "Projeção de Fechamentos do Mês"),
    ("RN-18", "Variações MoM (Month-over-Month)"),
    ("RN-19", "Lógica de Calendário e Relações de Data"),
]
for code, title in toc_data:
    row_data = [[p(f"<b>{code}</b>", S_TOC_RN), p(title, S_TOC_ITEM),
                 p("· · · · · · · · · · · · · · · · · · · · · ·", S_FOOTER)]]
    t = Table(row_data, colWidths=[1.7*cm, CONTENT_W*0.6, CONTENT_W*0.28])
    t.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t)

story.append(sp(0.5))
story.append(hr(C_MID, 1))
story.append(sp(0.3))
story.append(p("Este documento define as condições formais que governam o comportamento de cada métrica no modelo de dados Power BI do Dashboard P&C. "
               "Serve como referência para auditorias, manutenção do modelo e onboarding de novos membros da equipe.", S_NOTE))
story.append(sp(0.5))

# ─────────────────────────────────────────────────────────────
# SEÇÃO 1 — CICLO DE VIDA DA VAGA
# ─────────────────────────────────────────────────────────────
story.append(section_break("Seção 1 — Ciclo de Vida da Vaga"))
story.append(sp(0.5))

# RN-01
story.append(KeepTogether([
    rn_header("RN-01", "Vaga Fechada por R&S"),
    sp(0.25),
    p("Uma vaga é considerada <b>fechada por R&S</b> quando <b>todas</b> as condições abaixo são verdadeiras simultaneamente:"),
    sp(0.2),
    condition_table([
        ("Tipo da solicitação",  'TIPO DE SOLICITAÇÃO RECEBIDA = "R&S"'),
        ("Status válido",        'STATUS  não pertence a {"CANCELADA", "DESISTENTE"}'),
        ("Candidato identificado","NOME COMPLETO  não está em branco"),
        ("Data de encerramento", "DATA DE FECHAMENTO DA VAGA  não está em branco"),
    ]),
    sp(0.2),
    p("<b>Fórmula DAX:</b>"),
    sp(0.1),
    formula_box([
        "VagasFechadaR&S =",
        "  CALCULATE(",
        "    COUNTROWS(FILTER('Fonte_Sheets',",
        "      NOT(ISBLANK([DATA DE FECHAMENTO DA VAGA]))",
        "        && NOT(ISBLANK([NOME COMPLETO]))",
        "        && NOT([STATUS] IN {\"CANCELADA\", \"DESISTENTE\"}))),",
        "    [TIPO DE SOLICITAÇÃO RECEBIDA] = \"R&S\",",
        "    USERELATIONSHIP(dCalendario[Date], [DATA DE FECHAMENTO DA VAGA])",
        "  )",
    ]),
    sp(0.2),
    warn_box("Esta regra difere intencionalmente da RN-02 (Admissão). Em R&S, o campo STATUS pode permanecer em "
             "estados intermediários de admissão (ex: \"INICIAR ADMISSÃO\", \"ENTREGA DE DOCUMENTOS\") mesmo após "
             "o recrutamento ser concluído e o candidato aprovado. A presença de DATA DE FECHAMENTO DA VAGA "
             "preenchida é o indicador definitivo de que o R&S foi encerrado com sucesso. "
             "Apenas CANCELADA e DESISTENTE invalidam a contratação e devem ser excluídos."),
    sp(0.1),
    note_box("Granularidade: a contagem é feita por linha (TICKET + NOME COMPLETO), permitindo que um mesmo ticket "
             "registre múltiplas contratações. A relação de data ativa é DATA DE FECHAMENTO DA VAGA — o filtro de "
             "período age sobre o mês de fechamento, não de abertura."),
]))
story.append(sp(0.5))

# RN-02
story.append(KeepTogether([
    rn_header("RN-02", "Vaga Fechada por Admissão"),
    sp(0.25),
    p("Uma vaga é considerada <b>fechada por Admissão</b> quando <b>todas</b> as condições abaixo são verdadeiras:"),
    sp(0.2),
    condition_table([
        ("Tipo da solicitação",        'TIPO DE SOLICITAÇÃO RECEBIDA = "Admissão"'),
        ("Status terminal",            'STATUS = "FECHADA"'),
        ("Responsável identificado",   "RESPONSÁVEL PELA ADMISSÃO  não está em branco"),
        ("Data de encerramento",       "DATA DE FECHAMENTO DA VAGA  não está em branco"),
    ]),
    sp(0.2),
    note_box("Diferente do R&S, o campo de controle do responsável é RESPONSÁVEL PELA ADMISSÃO (não CONSULTOR DE R&S "
             "nem NOME COMPLETO). Vagas de Admissão representam candidatos já pré-aprovados pelo gestor em processo "
             "de integração ao sistema (documentação, cadastro na Gupy, início). O processo começa com o candidato definido."),
]))
story.append(sp(0.5))

# RN-03
story.append(KeepTogether([
    rn_header("RN-03", "Vaga Aberta — Pipeline de R&S"),
    sp(0.25),
    p("Uma vaga é considerada <b>em aberto no pipeline de R&S</b> quando <b>todas</b> as condições abaixo são verdadeiras:"),
    sp(0.2),
    condition_table([
        ("Sem data de encerramento",  "DATA DE FECHAMENTO DA VAGA  está em branco"),
        ("Status não é terminal",     "STATUS  não pertence ao conjunto de status terminais (ver abaixo)"),
        ("Status preenchido",         "STATUS  não está em branco"),
        ("Sem integração Gupy",       "DATA DE INTEGRAÇÃO NA GUPY  está em branco"),
        ("Relação de data ativa",     "USERELATIONSHIP(dCalendario[Date], Fonte_Sheets[DATA DE ABERTURA DA VAGA])"),
    ]),
    sp(0.2),
    p("<b>Status terminais excluídos:</b>"),
    sp(0.1),
    formula_box([
        "CANCELADA | DESISTENTE | CONGELADA | FECHADA",
        "INICIAR ADMISSÃO | ENTREGA DE DOCUMENTOS | FALTA FINALIZAR ADMISSÃO",
        "AGUARDANDO CADASTRO PJ | AGUARDANDO CADASTRO NA GUPY",
    ]),
    sp(0.2),
    note_box("Os status de admissão são excluídos porque a vaga já tem candidato aprovado — o recrutamento foi concluído. "
             "Incluí-los inflaria o indicador de abertas de forma enganosa."),
]))
story.append(sp(0.5))

# RN-04
story.append(KeepTogether([
    rn_header("RN-04", "Vaga em Processo de Admissão"),
    sp(0.25),
    p("Uma vaga é considerada <b>em etapa de admissão</b> (R&S concluído, aguardando integração) quando o STATUS pertence a <b>qualquer um</b> dos valores abaixo:"),
    sp(0.2),
    formula_box([
        "INICIAR ADMISSÃO",
        "ENTREGA DE DOCUMENTOS",
        "FALTA FINALIZAR ADMISSÃO",
        "AGUARDANDO CADASTRO PJ",
        "AGUARDANDO CADASTRO NA GUPY",
    ]),
    sp(0.2),
    note_box("Essas vagas são contabilizadas pela medida Vagas_Em_Processo_Admissão e excluídas de Vagas_Abertas (R&S), "
             "pois o processo de seleção já foi concluído."),
]))
story.append(sp(0.5))

# RN-05
story.append(KeepTogether([
    rn_header("RN-05", "Vaga Congelada"),
    sp(0.25),
    condition_table([
        ("Status específico", 'STATUS = "CONGELADA"'),
    ]),
    sp(0.2),
    note_box("Vagas congeladas representam pausas temporárias autorizadas pelo negócio (ex: restrição orçamentária, "
             "mudança de headcount). São excluídas do cálculo de vagas abertas ativas — não há processo ativo acontecendo. "
             "Contabilizadas pela medida Vagas_Congeladas."),
]))
story.append(sp(0.5))

# RN-06
story.append(KeepTogether([
    rn_header("RN-06", "Vaga Cancelada"),
    sp(0.25),
    condition_table([
        ("Status específico", 'STATUS = "CANCELADA"'),
    ]),
    sp(0.2),
    note_box("Vagas canceladas entram no numerador da Taxa_Cancelamento_%. São excluídas de todos os indicadores de "
             "volume ativo e aging. Cancelamentos frequentes em uma unidade podem sinalizar falta de planejamento de "
             "headcount ou processo de aprovação inadequado."),
]))
story.append(sp(0.5))

# ─────────────────────────────────────────────────────────────
# SEÇÃO 2 — SLA
# ─────────────────────────────────────────────────────────────
story.append(section_break("Seção 2 — SLA (Service Level Agreement)"))
story.append(sp(0.5))

# RN-07
story.append(KeepTogether([
    rn_header("RN-07", "SLA de R&S — Tempo de Recrutamento"),
    sp(0.25),
    p("O <b>SLA R&S</b> de uma vaga é o número de dias corridos entre a abertura e o fechamento, calculado pela coluna SLA R&S na fonte de dados."),
    sp(0.2),
    condition_table([
        ("Início do prazo",       "DATA DE ABERTURA DA VAGA"),
        ("Fim do prazo",          "DATA DE FECHAMENTO DA VAGA"),
        ("Meta de cumprimento",   "≤ 30 dias"),
        ("Agregação padrão",      "AVERAGE(Fonte_Sheets[SLA R&S])"),
        ("Contexto de cálculo",   "AVERAGE ignora linhas com SLA R&S em branco — vagas não fechadas são naturalmente excluídas"),
        ("Relação de data ativa", "dCalendario[Date] → DATA DE FECHAMENTO DA VAGA  (relação ativa padrão)"),
    ]),
    sp(0.2),
    note_box("O filtro de período age sobre o mês de fechamento — não de abertura. Ao selecionar 'Maio 2026', "
             "o SLA exibido é a média das vagas que FECHARAM em maio, independente de quando foram abertas."),
]))
story.append(sp(0.5))

# RN-08
story.append(KeepTogether([
    rn_header("RN-08", "SLA de Admissão — Tempo de Onboarding"),
    sp(0.25),
    p("O <b>SLA ADM</b> mede o tempo desde a aprovação do candidato até a integração completa na Gupy."),
    sp(0.2),
    condition_table([
        ("Base de cálculo",     "Coluna SLA ADM da fonte"),
        ("Meta de cumprimento", "≤ 45 dias"),
        ("Agregação padrão",    "AVERAGE(Fonte_Sheets[SLA ADM])"),
        ("Contexto",            "AVERAGE ignora linhas com SLA ADM em branco — vagas não fechadas são naturalmente excluídas"),
    ]),
    sp(0.2),
    warn_box("A meta de 45 dias para Admissão reflete a complexidade do processo: coleta de documentos, "
             "cadastro em sistemas e integração na Gupy. Atrasos nessa etapa são frequentemente causados por "
             "demora do candidato ou do gestor — não do P&C. O dashboard permite identificar essa distinção."),
]))
story.append(sp(0.5))

# RN-09
story.append(KeepTogether([
    rn_header("RN-09", "SLA Total"),
    sp(0.25),
    condition_table([
        ("Base de cálculo", "Coluna SLA TOTAL da fonte (R&S + ADM combinados)"),
        ("Agregação",       "AVERAGE(Fonte_Sheets[SLA TOTAL])"),
        ("Uso principal",   "Visão executiva — número único de resumo para diretoria"),
    ]),
    sp(0.2),
    note_box("O SLA Total é uma média geral e não deve ser usado para diagnóstico de gargalos. Para identificar "
             "onde está o problema, sempre desagregar em SLA R&S e SLA ADM separadamente."),
]))
story.append(sp(0.5))

# ─────────────────────────────────────────────────────────────
# SEÇÃO 3 — AGING E CRITICIDADE
# ─────────────────────────────────────────────────────────────
story.append(section_break("Seção 3 — Aging e Criticidade de Vagas"))
story.append(sp(0.5))

# RN-10
story.append(KeepTogether([
    rn_header("RN-10", "Aging de Vaga Aberta — Dias em Aberto"),
    sp(0.25),
    p("O <b>aging</b> de uma vaga aberta é o número de dias corridos desde a DATA DE ABERTURA DA VAGA até <b>hoje</b>, "
      "calculado pela coluna calculada <i>Aging Dias Vaga Aberta</i> na tabela Fonte_Sheets."),
    sp(0.2),
    p("<b>Critérios para uma vaga ter aging calculado:</b>"),
    sp(0.15),
    condition_table([
        ("Sem data de fechamento",    "DATA DE FECHAMENTO DA VAGA  está em branco"),
        ("Sem integração Gupy",       "DATA DE INTEGRAÇÃO NA GUPY  está em branco"),
        ("Data de abertura existente","DATA DE ABERTURA DA VAGA  não está em branco"),
        ("Status não é terminal",     'STATUS  não pertence a {CANCELADA, DESISTENTE, FECHADA}'),
        ("Status preenchido",         "STATUS  não está em branco e não é string vazia"),
        ("Filtro de calendário",      "REMOVEFILTERS(dCalendario) — aging sempre calculado em relação a HOJE"),
    ]),
    sp(0.2),
    note_box("O REMOVEFILTERS(dCalendario) é crítico: garante que vagas abertas em meses anteriores não fiquem "
             "invisíveis quando o usuário filtra por um período específico. O aging deve sempre refletir o "
             "estado atual da vaga, independente do filtro de data ativo na tela."),
]))
story.append(sp(0.5))

# RN-11
story.append(KeepTogether([
    rn_header("RN-11", "Faixas de Aging"),
    sp(0.25),
    p("As vagas abertas são classificadas em <b>4 faixas de aging</b> com base no número de dias em aberto, "
      "calibradas em relação às metas de SLA R&S (≤ 15 dias) e SLA ADM (≤ 10 dias):"),
    sp(0.2),
    wide_table(
        ["Faixa", "Intervalo", "Status operacional", "Ação recomendada"],
        [
            ("0–7 dias",   "Aging ≥ 0 e ≤ 7",   "Saudável — dentro das metas R&S e ADM",        "Nenhuma. Fluxo normal de triagem."),
            ("8–15 dias",  "Aging ≥ 8 e ≤ 15",  "Atenção — ADM acima da meta (>10d); R&S no limite", "Verificar andamento e cobrar atualização."),
            ("16–30 dias", "Aging ≥ 16 e ≤ 30", "Risco — ambos os SLAs de R&S e ADM vencidos",  "Intervenção imediata do responsável."),
            ("+30 dias",   "Aging > 30",         "CRÍTICO — threshold de criticidade superado",   "Escalonamento para liderança. Revisar condições da vaga."),
        ],
        col_widths=[1.8*cm, 2.5*cm, 6.0*cm, 5.4*cm],
        accent=C_DARK,
    ),
    sp(0.2),
    note_box("A coluna calculada Faixa Aging na tabela Fonte_Sheets implementa essa classificação. "
             "A medida Vagas_Aging_Distribuicao usa KEEPFILTERS(NOT(ISBLANK(Faixa Aging))) para preservar "
             "o contexto de faixa no visual de colunas da aba Aging."),
]))
story.append(sp(0.5))

# RN-12
story.append(KeepTogether([
    rn_header("RN-12", "Vagas Críticas — Threshold > 30 Dias", accent=C_RED),
    sp(0.25),
    p("Uma vaga é considerada <b>crítica</b> e entra na Tabela de Vagas Críticas quando:"),
    sp(0.2),
    condition_table([
        ("Data de abertura existente", "DATA DE ABERTURA DA VAGA  não está em branco"),
        ("Sem encerramento",           "DATA DE FECHAMENTO DA VAGA  está em branco"),
        ("Status não é terminal",      'STATUS  não pertence a {CANCELADA, DESISTENTE, CONGELADA, FECHADA}'),
        ("Status preenchido",          "STATUS  não está em branco e não é string vazia"),
        ("Threshold de criticidade",   "Aging Dias Vaga Aberta > 30"),
        ("Filtro de calendário",       "REMOVEFILTERS(dCalendario)"),
    ], accent=C_RED),
    sp(0.2),
    warn_box("O threshold crítico é 30 dias — não 45. Uma vaga que ultrapassa 30 dias indica que ambas as metas "
             "de SLA (R&S ≤ 15d e ADM ≤ 10d) já foram amplamente extrapoladas. Requer escalonamento imediato para "
             "a liderança e revisão das condições da vaga (salário, requisitos, processo)."),
]))
story.append(sp(0.5))

# ─────────────────────────────────────────────────────────────
# SEÇÃO 4 — QUALIDADE E EFICIÊNCIA
# ─────────────────────────────────────────────────────────────
story.append(section_break("Seção 4 — Qualidade e Eficiência"))
story.append(sp(0.5))

# RN-13
story.append(KeepTogether([
    rn_header("RN-13", "Taxa de Cumprimento do SLA de R&S"),
    sp(0.25),
    p("Uma vaga R&S é considerada <b>dentro do SLA</b> para fins desta taxa quando:"),
    sp(0.2),
    condition_table([
        ("Tipo",                   'TIPO DE SOLICITAÇÃO RECEBIDA = "R&S"'),
        ("Status",                 'STATUS = "FECHADA"'),
        ("Candidato identificado", "NOME COMPLETO  não está em branco"),
        ("Data de fechamento",     "DATA DE FECHAMENTO DA VAGA  não está em branco"),
        ("Threshold de prazo",     "SLA R&S ≤ 30  (meta em dias)"),
    ]),
    sp(0.2),
    p("<b>Fórmula:</b>"),
    sp(0.1),
    formula_box([
        "Taxa_SLA_Cumprido_R&S_%  =",
        "  VAR MetaSLA = 30",
        "  Vagas R&S fechadas com STATUS=FECHADA e SLA R&S ≤ MetaSLA",
        "  ÷",
        "  [VagasFechadaR&S]  (denominador com regra própria — ver RN-01)",
    ]),
    sp(0.2),
    note_box("Atenção: numerador usa STATUS = FECHADA (filtro explícito), enquanto o denominador VagasFechadaR&S "
             "usa a regra da RN-01 (exclusão de CANCELADA/DESISTENTE). Isso é intencional: a taxa de SLA mede "
             "apenas as vagas formalmente fechadas, garantindo que o benchmark seja sobre processos concluídos."),
]))
story.append(sp(0.5))

# RN-14
story.append(KeepTogether([
    rn_header("RN-14", "Taxa de Cumprimento do SLA de Admissão"),
    sp(0.25),
    p("Uma vaga ADM é considerada <b>dentro do SLA</b> quando:"),
    sp(0.2),
    condition_table([
        ("Tipo",                   'TIPO DE SOLICITAÇÃO RECEBIDA = "Admissão"'),
        ("Status",                 'STATUS = "FECHADA"'),
        ("Candidato identificado", "NOME COMPLETO  não está em branco"),
        ("Data de fechamento",     "DATA DE FECHAMENTO DA VAGA  não está em branco"),
        ("Threshold de prazo",     "SLA ADM ≤ 45  (meta em dias)"),
    ]),
    sp(0.2),
    p("<b>Fórmula:</b>"),
    sp(0.1),
    formula_box([
        "Taxa_SLA_Cumprido_ADM_%  =",
        "  VAR MetaSLA = 45",
        "  Vagas ADM fechadas com STATUS=FECHADA e SLA ADM ≤ MetaSLA",
        "  ÷",
        "  [VagasFechadasAdmissão]",
    ]),
]))
story.append(sp(0.5))

# RN-15
story.append(KeepTogether([
    rn_header("RN-15", "Taxa de Cancelamento"),
    sp(0.25),
    p("A <b>taxa de cancelamento</b> é a proporção de vagas canceladas sobre o total de solicitações recebidas:"),
    sp(0.2),
    condition_table([
        ("Numerador",   'DISTINCTCOUNT(TICKET)  onde STATUS = "CANCELADA"'),
        ("Denominador", "DISTINCTCOUNT(TICKET)  onde STATUS  não está em branco  (todas as solicitações)"),
    ]),
    sp(0.2),
    p("<b>Fórmula:</b>"),
    sp(0.1),
    formula_box([
        "Taxa_Cancelamento_%  =",
        "  Vagas Canceladas  ÷  Total de Solicitações Recebidas",
    ]),
    sp(0.2),
    note_box("Alta taxa de cancelamento pode sinalizar falta de planejamento de headcount ou processo de "
             "aprovação de vagas inadequado — o problema não está no recrutamento, mas na abertura da vaga."),
]))
story.append(sp(0.5))

# ─────────────────────────────────────────────────────────────
# SEÇÃO 5 — PERFORMANCE DE RECRUTADORES
# ─────────────────────────────────────────────────────────────
story.append(section_break("Seção 5 — Performance de Recrutadores"))
story.append(sp(0.5))

# RN-16
story.append(KeepTogether([
    rn_header("RN-16", "Performance do Recrutador — Janela de 3 Meses"),
    sp(0.25),
    p("A avaliação usa uma <b>janela fixa de 3 meses completos</b>, excluindo sempre o mês atual:"),
    sp(0.2),
    condition_table([
        ("Início da janela",      "EDATE(DATE(ANO, MÊS_ATUAL, 1), -3)"),
        ("Fim da janela",         "DATE(ANO, MÊS_ATUAL, 1) − 1  (último dia do mês anterior)"),
        ("Exclusão do mês atual", "Sempre excluído — dados incompletos"),
        ("Exemplo (Maio 2026)",   "Janela = Fevereiro, Março e Abril de 2026"),
    ]),
    sp(0.2),
    p("<b>Métricas derivadas:</b>"),
    sp(0.15),
    wide_table(
        ["Medida", "Fórmula / Critério", "Significado"],
        [
            ("Rec_RS_3M",            "VagasFechadaR&S filtrado pela janela de 3M (DATA DE FECHAMENTO DA VAGA)",  "Produção absoluta R&S no período"),
            ("Rec_ADM_3M",           "Vagas ADM com DATA DE INICIO PREVISTA na janela de 3M (≠ data fechamento)", "Produção absoluta Admissão no período"),
            ("Rec_MesesAtivos_RS_3M","Meses distintos com ≥ 1 fechamento R&S na janela",                         "Denominador justo — novos vs. veteranos R&S"),
            ("Rec_MesesAtivos_ADM_3M","Meses distintos com ≥ 1 ADM por DATA DE INICIO PREVISTA na janela",       "Denominador justo — novos vs. veteranos ADM"),
            ("Rec_RS_MediaMensal",   "Rec_RS_3M ÷ Rec_MesesAtivos_RS_3M",                                        "Média mensal R&S — métrica primária de constância"),
            ("Rec_ADM_MediaMensal",  "Rec_ADM_3M ÷ Rec_MesesAtivos_ADM_3M",                                      "Média mensal ADM — métrica primária de constância"),
            ("Rec_Rank_RS",          "RANKX(Rec_RS_MediaMensal, DESC, Dense) — BLANK se sem fechamentos",        "Ranking R&S justo entre novos e veteranos"),
            ("Rec_Rank_ADM",         "RANKX(Rec_ADM_MediaMensal, DESC, Dense) — BLANK se sem fechamentos",       "Ranking ADM justo entre novos e veteranos"),
        ],
        col_widths=[3.8*cm, 7.0*cm, 4.9*cm],
    ),
    sp(0.2),
    warn_box("ATENÇÃO — Datas diferentes por tipo: R&S usa DATA DE FECHAMENTO DA VAGA na janela de 3M. "
             "ADM usa DATA DE INICIO PREVISTA (não data de fechamento). Isso garante que a entrada do "
             "colaborador seja o marco de produtividade da admissão, não o fechamento burocrático da vaga."),
    sp(0.1),
    note_box("O uso de meses ativos como denominador garante comparabilidade: um recrutador que entrou no segundo mês "
             "da janela tem apenas 2 meses de dados — dividir por 3 (fixo) penalizaria injustamente. "
             "Ranking é BLANK para consultores sem nenhum fechamento na janela."),
]))
story.append(sp(0.5))

# ─────────────────────────────────────────────────────────────
# SEÇÃO 6 — PROJEÇÃO E VARIAÇÕES
# ─────────────────────────────────────────────────────────────
story.append(section_break("Seção 6 — Projeção e Variações Temporais"))
story.append(sp(0.5))

# RN-17
story.append(KeepTogether([
    rn_header("RN-17", "Projeção de Fechamentos do Mês"),
    sp(0.25),
    p("A <b>projeção</b> extrapola o ritmo atual de fechamentos para estimar o total ao final do mês:"),
    sp(0.2),
    condition_table([
        ("Base",              "Vagas fechadas no mês até hoje  (VagasFechadas_Total_MTD)"),
        ("Dias decorridos",   "Dias úteis (seg–sex) de 1º do mês até hoje"),
        ("Dias totais",       "Dias úteis (seg–sex) de 1º até o último dia do mês"),
        ("Retorna BLANK()",   "Se nenhum dia útil decorreu no mês"),
    ]),
    sp(0.2),
    p("<b>Fórmula:</b>"),
    sp(0.1),
    formula_box([
        "Projeção_Fechamentos_Mês  =",
        "  ROUND( (FechamentosMTD ÷ DiasDecorridos) × DiasNoMes , 0 )",
    ]),
    sp(0.2),
    note_box("A projeção usa dias úteis (não corridos) para evitar distorção de fins de semana. "
             "É uma estimativa linear — acelerações ou desacelerações futuras não são captadas."),
]))
story.append(sp(0.5))

# RN-18
story.append(KeepTogether([
    rn_header("RN-18", "Variações MoM (Month-over-Month)"),
    sp(0.25),
    p("Todas as variações MoM seguem o padrão:"),
    sp(0.1),
    formula_box([
        "MoM_Indicador_%  =  (Valor_Mês_Atual − Valor_Mês_Anterior)  ÷  Valor_Mês_Anterior",
    ]),
    sp(0.2),
    wide_table(
        ["Medida", "Base de comparação", "Interpretação"],
        [
            ("MoM_SLA_R&S_%",              "SLA_R&S_Médio − SLA_R&S_Médio_Mês_Anterior ÷ anterior",          "Negativo = melhora (prazo menor)"),
            ("MoM_SLA_ADM_%",              "SLA_ADM_Médio − SLA_ADM_Médio_Mês_Anterior ÷ anterior",          "Negativo = melhora (prazo menor)"),
            ("MoM_SLA_Total_%",            "SLA_Total − SLA_Total_Mês_Anterior ÷ anterior",                  "Negativo = melhora"),
            ("MoM_MTD_VagasFechadas_%",    "VagasFechadas_Total_MTD − VagasFechadas_Total_MTD_Mês_Anterior ÷ anterior", "Positivo = crescimento"),
            ("Vagas_Abertas_MoM_Estoque_%","Vagas_Abertas_Hoje − Vagas_Abertas_Fim_Mes_Anterior ÷ anterior", "Positivo = fila crescendo"),
        ],
        col_widths=[4.5*cm, 7.0*cm, 4.2*cm],
    ),
    sp(0.2),
    note_box("Atenção à interpretação: para SLA, valores negativos indicam MELHORA (prazo ficou menor). "
             "Para volume de fechamentos, valores positivos indicam CRESCIMENTO. Não confundir as direções."),
]))
story.append(sp(0.5))

# RN-19
story.append(KeepTogether([
    rn_header("RN-19", "Lógica de Calendário e Relações de Data"),
    sp(0.25),
    p("O modelo possui <b>dois calendários</b> para suportar filtros por datas distintas:"),
    sp(0.2),
    wide_table(
        ["Tabela de calendário", "Relação ativa com", "Uso"],
        [
            ("dCalendario",        "Fonte_Sheets[DATA DE FECHAMENTO DA VAGA]",  "Filtros padrão por período de fechamento"),
            ("dCalendarioAbertura","Fonte_Sheets[DATA DE ABERTURA DA VAGA]",    "Filtros por período de abertura"),
        ],
        col_widths=[4.0*cm, 6.5*cm, 5.2*cm],
    ),
    sp(0.2),
    p("A relação <i>dCalendario → DATA DE ABERTURA DA VAGA</i> é <b>inativa</b> (para evitar ambiguidade) "
      "e é ativada pontualmente com USERELATIONSHIP nas medidas que precisam filtrar por data de abertura."),
    sp(0.15),
    p("<b>Impacto prático:</b>"),
    sp(0.1),
    condition_table([
        ("Filtro de Ano/Mês nas abas",    "Age sobre DATA DE FECHAMENTO DA VAGA  (relação ativa padrão)"),
        ("Medidas de vagas abertas",      "Ativam USERELATIONSHIP com DATA DE ABERTURA DA VAGA"),
        ("Aging das vagas abertas",       "REMOVEFILTERS(dCalendario) — sempre calculado em relação a hoje"),
        ("Histórico SLA (linha temporal)","USERELATIONSHIP com DATA DE FECHAMENTO — eixo X = mês de fechamento"),
    ]),
    sp(0.2),
    note_box("Sempre verificar qual relação de data está ativa ao interpretar uma medida. Uma medida pode exibir "
             "valores inesperados se o contexto de filtro do visual não corresponder à relação de data esperada."),
]))
story.append(sp(0.5))

# ─────────────────────────────────────────────────────────────
# GLOSSÁRIO RÁPIDO
# ─────────────────────────────────────────────────────────────
story.append(section_break("Glossário — Termos e Abreviações"))
story.append(sp(0.4))

glossario = [
    ("Ticket",         "Código único que identifica uma vaga no sistema"),
    ("R&S",            "Recrutamento & Seleção — processo de busca e seleção de candidatos externos"),
    ("Admissão",       "Processo de integrar o candidato já aprovado (documentação, cadastro, início)"),
    ("SLA",            "Service Level Agreement — prazo de atendimento acordado para cada etapa"),
    ("Aging",          "Número de dias que uma vaga está aberta sem ser fechada"),
    ("Faixa Aging",    "Categorização do aging em bandas de urgência (0-7, 8-15, 16-30, +30 dias)"),
    ("MTD",            "Month-to-Date — acumulado do início do mês até hoje"),
    ("MoM",            "Month-over-Month — variação em relação ao mesmo período do mês anterior"),
    ("3M",             "Janela dos últimos 3 meses completos (exclui mês atual)"),
    ("Status terminal","Status que indica encerramento definitivo da vaga (FECHADA, CANCELADA, DESISTENTE)"),
    ("Situação",       "Agrupamento macro do status (Em Andamento, Congelada, Cancelada, Fechada)"),
    ("USERELATIONSHIP","Função DAX que ativa uma relação de data inativa pontualmente"),
    ("REMOVEFILTERS",  "Função DAX que remove filtros de uma tabela/coluna do contexto de cálculo"),
    ("EOMONTH",        "Função DAX/Excel que retorna o último dia de um mês N meses à frente ou atrás"),
]
glossario_data = [[p(t, S_TD_BOLD), p(d, S_TD)] for t, d in glossario]
gt = Table(
    [[p("Termo", S_TH), p("Definição", S_TH)]] + glossario_data,
    colWidths=[CONTENT_W * 0.28, CONTENT_W * 0.72]
)
gt.setStyle(TableStyle([
    ("BACKGROUND",     (0, 0), (-1, 0),  C_DARK),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_PALE, C_WHITE]),
    ("GRID",           (0, 0), (-1, -1), 0.4, C_GBORD),
    ("TOPPADDING",     (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
    ("LEFTPADDING",    (0, 0), (-1, -1), 7),
    ("RIGHTPADDING",   (0, 0), (-1, -1), 7),
    ("VALIGN",         (0, 0), (-1, -1), "TOP"),
]))
story.append(gt)
story.append(sp(0.5))

# ─────────────────────────────────────────────────────────────
# BUILD PDF
# ─────────────────────────────────────────────────────────────
OUTPUT = r"C:\Users\marce\Documents\Raíz Educação\Dados P&C\Regras_de_Negocio_Dashboard_PC.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=MARGIN_L,
    rightMargin=MARGIN_R,
    topMargin=MARGIN_T + 0.4*cm,   # extra p/ header band
    bottomMargin=MARGIN_B + 0.4*cm,
    title="Regras de Negócio — Dashboard P&C",
    author="Raíz Educação · Pessoas e Cultura",
    subject="Documentação de regras de negócio do Dashboard Estratégico P&C",
)

doc.build(story, onFirstPage=on_first_page, onLaterPages=on_page)
print(f"PDF gerado: {OUTPUT}")
