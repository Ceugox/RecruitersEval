"""
Gerador da Apresentação Estratégica de P&C para Diretoria
Raíz Educação — 20 slides, python-pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Paleta ──────────────────────────────────────────────────
def rgb(r,g,b): return RGBColor(r,g,b)

C_DARK   = rgb(22,  67,  42)
C_MID    = rgb(31, 107,  64)
C_LIGHT  = rgb(42, 157,  92)
C_PALE   = rgb(228,244,236)
C_GOLD   = rgb(232,160, 32)
C_GOLDLT = rgb(254,243,216)
C_WHITE  = rgb(255,255,255)
C_TXTD   = rgb( 17, 24, 39)
C_TXTM   = rgb( 55, 65, 81)
C_TXTMU  = rgb(107,114,128)
C_RED    = rgb(220, 38, 38)
C_AMBER  = rgb(217,119,  6)
C_GRAY   = rgb(243,244,246)
C_GBORD  = rgb(209,213,219)
C_RED_BG = rgb(254,242,242)

W = Inches(13.333)
H = Inches(7.5)

# ── Primitivos ───────────────────────────────────────────────
def box(slide, x, y, w, h, fill, line=None, lw=0.5):
    s = slide.shapes.add_shape(1, x, y, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line:
        s.line.color.rgb = line; s.line.width = Pt(lw)
    else:
        s.line.fill.background()
    return s

def oval(slide, x, y, w, h, fill):
    s = slide.shapes.add_shape(9, x, y, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fill; s.line.fill.background()
    return s

def tx(slide, text, x, y, w, h, fs=11, color=None, bold=False, align=PP_ALIGN.LEFT, wrap=True):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tb.word_wrap = wrap
    tf = tb.text_frame; tf.word_wrap = wrap
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = str(text)
    r.font.size = Pt(fs); r.font.bold = bold
    r.font.name = "Segoe UI"
    if color: r.font.color.rgb = color
    return tb

def multiline_tx(slide, lines, x, y, w, h, fs=10, color=None, bold_first=False):
    """lines = list of (text, bold, color) or just strings"""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tb.word_wrap = True
    tf = tb.text_frame; tf.word_wrap = True
    first = True
    for item in lines:
        if isinstance(item, str):
            text, bld, col = item, False, color
        else:
            text, bld, col = item[0], item[1], item[2] if len(item)>2 else color
        if first:
            p = tf.paragraphs[0]; first = False
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(3)
        r = p.add_run(); r.text = text
        r.font.size = Pt(fs); r.font.bold = bld
        r.font.name = "Segoe UI"
        if col: r.font.color.rgb = col

def header(slide, tag, title, subtitle="", bg=None):
    bg = bg or C_DARK
    box(slide, 0, 0, W, Inches(1.38), bg)
    box(slide, 0, Inches(1.38), W, Inches(0.04), C_GOLD)
    # tag pill
    box(slide, Inches(0.55), Inches(0.2), Inches(2.4), Inches(0.3), C_GOLD)
    tx(slide, tag, Inches(0.57), Inches(0.22), Inches(2.36), Inches(0.28),
       fs=8, color=C_DARK, bold=True)
    tx(slide, title, Inches(0.55), Inches(0.55), Inches(12.3), Inches(0.62),
       fs=22, color=C_WHITE, bold=True)
    if subtitle:
        tx(slide, subtitle, Inches(0.55), Inches(1.1), Inches(11), Inches(0.3),
           fs=11, color=rgb(180,220,200))

def footer(slide, pg, total=20):
    box(slide, 0, Inches(7.05), W, Inches(0.45), C_PALE)
    box(slide, 0, Inches(7.05), W, Inches(0.025), C_LIGHT)
    tx(slide, "Raíz Educação · P&C Analytics · Confidencial",
       Inches(0.55), Inches(7.1), Inches(9), Inches(0.32), fs=9, color=C_TXTMU)
    tx(slide, f"{pg} / {total}", Inches(12.0), Inches(7.1), Inches(1.2), Inches(0.32),
       fs=9, color=C_MID, bold=True, align=PP_ALIGN.RIGHT)

def ss_placeholder(slide, x, y, w, h, name, hint="Inserir screenshot aqui"):
    s = slide.shapes.add_shape(1, x, y, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = rgb(248,250,252)
    s.line.color.rgb = rgb(156,163,175); s.line.width = Pt(1.5)
    tf = s.text_frame; tf.word_wrap = True
    p1 = tf.paragraphs[0]; p1.alignment = PP_ALIGN.CENTER
    r1 = p1.add_run(); r1.text = "[ INSERIR PRINT ]"
    r1.font.size = Pt(10); r1.font.bold = True; r1.font.name = "Segoe UI"
    r1.font.color.rgb = rgb(156,163,175)
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run(); r2.text = name
    r2.font.size = Pt(12); r2.font.bold = True; r2.font.name = "Segoe UI"
    r2.font.color.rgb = C_MID
    p3 = tf.add_paragraph(); p3.alignment = PP_ALIGN.CENTER
    r3 = p3.add_run(); r3.text = hint
    r3.font.size = Pt(9); r3.font.name = "Segoe UI"; r3.font.color.rgb = rgb(156,163,175)

def card(slide, x, y, w, h, title, body, acc=None, bg=None, body_fs=10):
    acc = acc or C_MID; bg = bg or C_WHITE
    box(slide, x, y, w, h, bg, C_GBORD, 0.5)
    box(slide, x, y, Inches(0.05), h, acc)
    tx(slide, title, x+Inches(0.12), y+Inches(0.1), w-Inches(0.2), Inches(0.3),
       fs=11, color=C_DARK, bold=True)
    tx(slide, body, x+Inches(0.12), y+Inches(0.42), w-Inches(0.2), h-Inches(0.52),
       fs=body_fs, color=C_TXTM, wrap=True)

def metric_row(slide, x, y, w, h, name, why, meta=""):
    box(slide, x, y, w, h, C_GRAY)
    box(slide, x, y, Inches(0.05), h, C_MID)
    tx(slide, name, x+Inches(0.12), y+Inches(0.08), w-Inches(0.2), Inches(0.3),
       fs=11, color=C_DARK, bold=True)
    tx(slide, why, x+Inches(0.12), y+Inches(0.4), w-Inches(0.2), h-Inches(0.62),
       fs=10, color=C_TXTM, wrap=True)
    if meta:
        tx(slide, meta, x+Inches(0.12), y+h-Inches(0.22), w-Inches(0.2), Inches(0.2),
           fs=8, color=C_TXTMU)

def callout(slide, x, y, w, h, text, bg=None, border=None):
    bg = bg or C_PALE; border = border or C_LIGHT
    box(slide, x, y, w, h, bg, border, 1)
    tx(slide, text, x+Inches(0.15), y+Inches(0.1), w-Inches(0.25), h-Inches(0.15),
       fs=10, color=C_TXTM, wrap=True)

def kpi_pill(slide, x, y, w, h, val, lbl, bg=None):
    bg = bg or C_DARK
    box(slide, x, y, w, h, bg)
    tx(slide, val, x, y+Inches(0.08), w, Inches(0.45),
       fs=26, color=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    tx(slide, lbl, x, y+Inches(0.52), w, Inches(0.35),
       fs=9, color=rgb(200,230,215), align=PP_ALIGN.CENTER)

def divider(slide, y):
    box(slide, Inches(0.55), y, Inches(12.23), Inches(0.04), C_LIGHT)

# ── Criar apresentação ───────────────────────────────────────
prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
blank = prs.slide_layouts[6]

def new_slide():
    return prs.slides.add_slide(blank)

# ════════════════════════════════════════════════════════════════
# SLIDE 1 — CAPA
# ════════════════════════════════════════════════════════════════
s = new_slide()
box(s, 0, 0, W, H, C_DARK)
oval(s, Inches(9.0), Inches(3.0), Inches(6.5), Inches(6.5), rgb(27,80,50))
box(s, 0, 0, W, Inches(0.07), C_GOLD)

tx(s, "RAÍZ EDUCAÇÃO · PEOPLE & CULTURE", Inches(0.8), Inches(0.22),
   Inches(8), Inches(0.35), fs=10, color=C_GOLD, bold=True)
box(s, Inches(0.8), Inches(0.62), Inches(4.5), Inches(0.02), rgb(60,100,80))

pill = s.shapes.add_shape(1, Inches(0.8), Inches(0.78), Inches(2.8), Inches(0.35))
pill.fill.solid(); pill.fill.fore_color.rgb = C_GOLD; pill.line.fill.background()
tx(s, "APRESENTAÇÃO PARA DIRETORIA", Inches(0.82), Inches(0.8), Inches(2.76), Inches(0.32),
   fs=8, color=C_DARK, bold=True)

tx(s, "Dashboard", Inches(0.8), Inches(1.35), Inches(9), Inches(0.85),
   fs=50, color=C_WHITE, bold=True)
tx(s, "Estratégico de P&C", Inches(0.8), Inches(2.12), Inches(10), Inches(0.75),
   fs=42, color=C_GOLD, bold=True)
tx(s, "Visão, métricas e defesa de cada indicador\ndo painel de Recrutamento & Seleção",
   Inches(0.8), Inches(3.05), Inches(8.5), Inches(0.85),
   fs=16, color=rgb(180,220,200))

meta = [
    ("Data", "Maio · 2026", 0.8),
    ("Área", "People & Culture", 3.2),
    ("Plataforma", "Microsoft Power BI", 5.6),
    ("Abrangência", "7 marcas · todas as unidades", 8.2),
]
for lbl, val, xi in meta:
    tx(s, lbl, Inches(xi), Inches(4.35), Inches(2.3), Inches(0.28),
       fs=8, color=rgb(100,150,120))
    tx(s, val, Inches(xi), Inches(4.65), Inches(2.5), Inches(0.35),
       fs=13, color=C_WHITE, bold=True)

box(s, 0, H-Inches(0.06), W, Inches(0.06), C_GOLD)

# ════════════════════════════════════════════════════════════════
# SLIDE 2 — AGENDA
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s, "Agenda", "O que vamos apresentar hoje",
       "Estrutura da apresentação em 7 blocos temáticos")
footer(s, 2)

agenda = [
    ("1","Contexto e Problema","Por que precisamos de um dashboard de P&C?"),
    ("2","Visão da Solução","Arquitetura, dados e 5 perspectivas integradas"),
    ("3","Aba Geral — Volume & SLA","KPIs de fechamento, abertura e prazo de atendimento"),
    ("4","Aba Detalhamento","Análise por unidade, nível, regime e motivo"),
    ("5","Aba Aging — Gestão de Risco","Distribuição temporal e tendência histórica de SLA"),
    ("6","Abas Operacionais","Update em tempo real e rastreabilidade por consulta"),
    ("7","Performance & Impacto Estratégico","Métricas individuais, defesa dos indicadores e próximos passos"),
]
for i,(num,tit,desc) in enumerate(agenda):
    ci = 0 if i < 4 else 1
    ri = i if i < 4 else i-4
    cx = Inches(0.55 + ci*6.45)
    cy = Inches(1.62) + ri*Inches(1.32)
    cw = Inches(6.1)
    if i == 6: cx = Inches(0.55); cw = Inches(12.23)
    box(s, cx, cy, cw, Inches(1.15), C_GRAY, C_GBORD, 0.5)
    circ = s.shapes.add_shape(9, cx+Inches(0.14), cy+Inches(0.27), Inches(0.58), Inches(0.58))
    circ.fill.solid(); circ.fill.fore_color.rgb = C_DARK; circ.line.fill.background()
    tx(s, num, cx+Inches(0.14), cy+Inches(0.27), Inches(0.58), Inches(0.58),
       fs=14, color=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    tx(s, tit, cx+Inches(0.88), cy+Inches(0.2), cw-Inches(1.05), Inches(0.35),
       fs=13, color=C_TXTD, bold=True)
    tx(s, desc, cx+Inches(0.88), cy+Inches(0.6), cw-Inches(1.05), Inches(0.45),
       fs=10, color=C_TXTMU)

# ════════════════════════════════════════════════════════════════
# SLIDE 3 — CONTEXTO / PROBLEMA
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s, "Bloco 1 · Contexto", "O Problema que motivou o dashboard",
       "Gerenciar vagas sem dados é navegar no escuro")
footer(s, 3)

problems = [
    ("⚠️ Sem visibilidade de prazo",
     "Vagas ficavam abertas por meses sem que ninguém percebesse o risco — a descoberta acontecia só quando o gestor já estava sem o profissional."),
    ("🔀 Informação dispersa",
     "Dados de R&S e Admissão viviam em planilhas distintas, sem cruzamento, impossibilitando uma visão unificada do ciclo completo de contratação."),
    ("📊 Decisões por feeling",
     "A gestão de prioridade dos recrutadores era subjetiva. Quem estava 'sobrecarregado' dependia da percepção do gestor, não de dados concretos."),
    ("🏢 Falta de visão por marca",
     "Com 7 marcas ativas, não havia como comparar automaticamente a eficiência de recrutamento entre unidades de forma padronizada e consistente."),
]
for i,(tit,body) in enumerate(problems):
    card(s, Inches(0.55), Inches(1.62)+i*Inches(1.32), Inches(6.0), Inches(1.18),
         tit, body, acc=C_RED, bg=C_RED_BG)

box(s, Inches(6.9), Inches(1.62), Inches(6.05), Inches(5.38), C_DARK)
tx(s,"A PERGUNTA CENTRAL", Inches(7.1), Inches(1.82), Inches(5.6), Inches(0.3),
   fs=9, color=C_GOLD, bold=True)
tx(s,'"Como garantir que o ciclo de\ncontratação acontece dentro do\nprazo, com qualidade, para\ntodas as marcas?"',
   Inches(7.1), Inches(2.2), Inches(5.65), Inches(1.7), fs=18, color=C_WHITE, bold=True)
box(s, Inches(7.0), Inches(4.05), Inches(5.85), Inches(0.025), rgb(60,100,80))
tx(s,"A resposta requer visibilidade sobre:",Inches(7.1),Inches(4.15),Inches(5.6),Inches(0.3),
   fs=10, color=rgb(180,220,200))
for i,a in enumerate([
    "Volume de vagas por fase do processo",
    "Tempo médio de cada etapa (SLA)",
    "Vagas em risco de vencer o prazo",
    "Performance individual de cada recrutador",
    "Causa raiz da demanda: substituição vs. crescimento",
]):
    tx(s,"▸  "+a, Inches(7.1), Inches(4.5)+i*Inches(0.43),Inches(5.65),Inches(0.4),
       fs=10.5, color=rgb(220,245,232))

# ════════════════════════════════════════════════════════════════
# SLIDE 4 — VISÃO DA SOLUÇÃO
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 2 · Solução","Visão Geral da Solução",
       "Um ecossistema de dados integrado para P&C")
footer(s, 4)

sol_cards = [
    ("📥 Fontes de Dados",
     "Google Sheets (live): Movimentação de pessoal + Controle de Vagas 2025, conectados em tempo real.\n\nPower BI Dataflow: R&S 2026 via Excel — pipeline estruturado.\n\nAtualização automática: sem exportações manuais."),
    ("⚙️ Motor Analítico",
     "Power BI (nível 1600) com modelo semântico robusto:\n· 90 medidas DAX calculadas\n· 21+ relacionamentos entre tabelas\n· Calendários dedicados por tipo de data\n· Lógica MoM e MTD nativa"),
    ("🏢 Abrangência",
     "7 interfaces de marca: Apogeu, Matriz, QI, Global, CLV, Cubo, Sá Pereira — cada uma com visão específica.\n\nDashboard central P&C: visão consolidada para toda a diretoria da área."),
]
for i,(tit,body) in enumerate(sol_cards):
    xi = Inches(0.55)+i*Inches(4.28)
    box(s, xi, Inches(1.62), Inches(4.0), Inches(2.5), C_PALE, C_LIGHT, 1)
    box(s, xi, Inches(1.62), Inches(4.0), Inches(0.05), C_MID)
    tx(s, tit, xi+Inches(0.15), Inches(1.75), Inches(3.7), Inches(0.35),
       fs=12, color=C_DARK, bold=True)
    tx(s, body, xi+Inches(0.15), Inches(2.15), Inches(3.7), Inches(1.9),
       fs=10, color=C_TXTM, wrap=True)

divider(s, Inches(4.3))

# Flow pipeline
box(s, Inches(0.55), Inches(4.45), Inches(9.6), Inches(1.85), C_DARK)
tx(s,"CICLO DE DADOS",Inches(0.75),Inches(4.58),Inches(3),Inches(0.3),fs=8,color=C_GOLD,bold=True)
flow = [
    ("Google\nSheets","Fonte viva"),
    ("Power BI","Modelagem"),
    ("90 Medidas\nDAX","Calculadas"),
    ("5 Abas\nTemáticas","Visuais"),
    ("Decisão\nbaseada\nem dado",""),
]
for i,(nm,sub) in enumerate(flow):
    xi = Inches(0.75)+i*Inches(1.85)
    bg_f = C_GOLD if i==4 else rgb(40,90,60)
    box(s, xi, Inches(4.9), Inches(1.6), Inches(1.2), bg_f)
    fc = C_DARK if i==4 else C_WHITE
    tx(s,nm, xi, Inches(4.98), Inches(1.6), Inches(0.55), fs=10, color=fc, bold=True, align=PP_ALIGN.CENTER)
    if sub:
        tx(s,sub, xi, Inches(5.5), Inches(1.6), Inches(0.28), fs=8,
           color=C_DARK if i==4 else rgb(200,230,215), align=PP_ALIGN.CENTER)
    if i<4:
        tx(s,"→", xi+Inches(1.65), Inches(5.1), Inches(0.18), Inches(0.4),
           fs=18, color=C_GOLD, bold=True)

# Stat badges
for i,(val,lbl,bg) in enumerate([
    ("90","Medidas DAX",C_PALE),
    ("7","Interfaces de marca",C_GOLDLT),
    ("5","Abas temáticas",C_PALE),
]):
    yi = Inches(4.45)+i*Inches(0.63)
    box(s, Inches(10.45), yi, Inches(2.5), Inches(0.55), bg)
    tx(s,val, Inches(10.55), yi+Inches(0.06), Inches(0.55), Inches(0.42), fs=24, color=C_DARK, bold=True)
    tx(s,lbl, Inches(11.18), yi+Inches(0.15), Inches(1.65), Inches(0.28), fs=10, color=C_TXTM)

# ════════════════════════════════════════════════════════════════
# SLIDE 5 — 5 PERSPECTIVAS
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 2 · Solução","5 Perspectivas Integradas",
       "Cada aba responde a uma pergunta estratégica diferente")
footer(s, 5)

tabs = [
    (C_DARK,          "📊","GERAL",        '"Como está o mês agora?"',                C_GOLD),
    (rgb(31,79,122),  "🔍","DETALHAMENTO", '"De onde vem a demanda?"',                 rgb(125,211,252)),
    (rgb(124,45,18),  "⏱️","AGING",         '"Quais vagas estão em risco?"',            rgb(254,215,170)),
    (rgb(74,29,150),  "🔎","CONSULTA",      '"Onde está essa vaga específica?"',        rgb(221,214,254)),
    (rgb(6,78,59),    "🔄","UPDATE",        '"O que está em andamento agora?"',         rgb(110,231,183)),
]
for i,(bg,icon,nm,q,acc) in enumerate(tabs):
    xi = Inches(0.55)+i*Inches(2.57)
    box(s, xi, Inches(1.72), Inches(2.35), Inches(4.1), bg)
    tx(s,icon, xi, Inches(2.05), Inches(2.35), Inches(0.75), fs=32, align=PP_ALIGN.CENTER)
    tx(s,nm, xi, Inches(2.85), Inches(2.35), Inches(0.45), fs=13, color=acc, bold=True, align=PP_ALIGN.CENTER)
    tx(s,q, xi+Inches(0.1), Inches(3.38), Inches(2.15), Inches(0.8),
       fs=11, color=rgb(220,240,230), align=PP_ALIGN.CENTER)

callout(s, Inches(0.55), Inches(6.0), Inches(12.23), Inches(0.9),
        "💡  Lógica de navegação: as abas seguem um fluxo do macro ao micro. Começa-se pelo Geral para o panorama; ao identificar uma anomalia, desce-se para o Detalhamento; se houver risco de prazo, acessa-se o Aging; para entender o andamento, vai-se ao Update; para localizar qualquer vaga, usa-se a Consulta.",
        bg=C_GOLDLT, border=C_GOLD)

# ════════════════════════════════════════════════════════════════
# SLIDE 6 — ABA GERAL (overview)
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 3 · Aba Geral","Aba Geral — Visão Estratégica do Mês",
       "O painel de controle da operação de P&C em tempo real")
footer(s, 6)

ss_placeholder(s, Inches(0.55), Inches(1.65), Inches(8.2), Inches(5.08),
               "Aba Geral — Print completo",
               "Capturar a tela da aba 'Geral' do dashboard com todos os visuals visíveis")
card(s, Inches(9.1), Inches(1.65), Inches(3.88), Inches(1.5),
     "🎯 Propósito estratégico",
     "É a primeira tela que qualquer gestor ou diretor deve ver. Em 30 segundos ela responde: fechamos? estamos no prazo? quantas vagas novas chegaram?",
     acc=C_GOLD, bg=C_GOLDLT)
card(s, Inches(9.1), Inches(3.22), Inches(3.88), Inches(1.2),
     "📅 Filtro Ano / Mês",
     "Permite comparar qualquer período histórico com um clique, sem criar relatórios extras. A diretoria pode revisitar qualquer mês.")
card(s, Inches(9.1), Inches(4.5), Inches(3.88), Inches(1.55),
     "📈 Composição visual",
     "2 cards com KPIs centrais (Volume + SLA)\nGráfico de colunas diário por tipo\nRanking de cargos com mais demanda\nDistribuição por status do processo")

# ════════════════════════════════════════════════════════════════
# SLIDE 7 — KPIs DE VOLUME
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 3 · Aba Geral",'KPIs de Volume — Card "Vagas Mês Atual"',
       "Três números que resumem o ritmo da operação")
footer(s, 7)

ss_placeholder(s, Inches(0.55), Inches(1.65), Inches(5.8), Inches(2.5),
               'Card "Vagas Mês Atual" — zoom',
               "Print focado nos 3 KPIs do card principal da aba Geral")
for i,(val,lbl) in enumerate([("—","Vagas Fechadas"),("—","Abertas no Período"),("—","Abertas Esta Semana")]):
    kpi_pill(s, Inches(0.55)+i*Inches(1.98), Inches(4.28), Inches(1.85), Inches(1.1), val, lbl)

for i,(nm,why,meta) in enumerate([
    ("Vagas Fechadas — R&S + Admissão",
     "Medida central de produtividade. Representa a entrega concreta do time — um candidato contratado e integrado. A soma de R&S e Admissão evita dupla contagem e reflete o volume real entregue ao negócio.",
     "Fórmula: VagasFechadasAdmissão + VagasFechadaR&S · Granularidade: TICKET + NOME COMPLETO"),
    ("Vagas Abertas no Período — Demanda acumulada",
     "Mede a pressão sobre o time. Quando abertas crescem mais rápido que fechadas, a fila cresce — sinal de capacidade insuficiente ou demanda repentina. Permite antecipar necessidade de reforço.",
     "Exclui status terminais: CANCELADA, DESISTENTE, CONGELADA, FECHADA"),
    ("Abertas Esta Semana — Pulso semanal",
     "Indicador de velocidade da demanda atual. Identifica se houve uma onda de novas requisições na semana, útil para redistribuição imediata de carga entre recrutadores antes que vire problema.",
     "Janela: segunda a domingo da semana corrente"),
]):
    metric_row(s, Inches(6.65), Inches(1.65)+i*Inches(1.58), Inches(6.3), Inches(1.4), nm, why, meta)

# ════════════════════════════════════════════════════════════════
# SLIDE 8 — KPIs DE SLA
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 3 · Aba Geral","KPIs de SLA — Prazo de Atendimento",
       "O contrato de serviço do P&C com o negócio, traduzido em dias")
footer(s, 8)

ss_placeholder(s, Inches(0.55), Inches(1.65), Inches(5.5), Inches(2.2),
               'Card "SLA" — zoom',
               "Print focado nos 3 indicadores de SLA da aba Geral")
box(s, Inches(0.55), Inches(4.0), Inches(5.5), Inches(2.65), C_DARK)
tx(s,"METAS DEFINIDAS",Inches(0.85),Inches(4.15),Inches(5),Inches(0.3),fs=9,color=C_GOLD,bold=True)
for i,(val,lbl) in enumerate([("15","dias · meta R&S"),("10","dias · meta ADM")]):
    xi = Inches(0.85)+i*Inches(2.75)
    box(s, xi, Inches(4.52), Inches(2.5), Inches(1.85), rgb(40,90,60))
    tx(s,val, xi, Inches(4.62), Inches(2.5), Inches(0.85), fs=48, color=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    tx(s,lbl, xi, Inches(5.45), Inches(2.5), Inches(0.35), fs=11, color=rgb(180,220,200), align=PP_ALIGN.CENTER)

for i,(nm,why,meta) in enumerate([
    ("SLA R&S — Meta: ≤ 15 dias",
     "Mede o tempo médio entre a abertura da vaga e a conclusão do recrutamento. Manter abaixo de 15 dias garante agilidade no ciclo de recrutamento e evita que vagas fiquem sem candidato por mais de duas semanas.",
     "AVERAGE(SLA R&S) · contexto: vagas fechadas no período selecionado"),
    ("SLA ADM — Meta: ≤ 10 dias",
     "Após a aprovação do candidato, há a etapa de documentação e integração. 10 dias é o prazo esperado — acima disso, há risco de o candidato desistir ou a unidade ficar descoberta por período inaceitável.",
     "AVERAGE(SLA ADM) · contexto: vagas fechadas no período selecionado"),
    ("SLA Total — Visão consolidada",
     "Média geral do processo completo (R&S + ADM). Usada em reuniões de diretoria para uma única resposta: 'quanto tempo leva, do zero à contratação?'. Permite comparar eficiência entre meses.",
     "AVERAGE(SLA TOTAL) · inclui ambos os processos"),
]):
    metric_row(s, Inches(6.45), Inches(1.65)+i*Inches(1.58), Inches(6.5), Inches(1.4), nm, why, meta)

# ════════════════════════════════════════════════════════════════
# SLIDE 9 — GRÁFICOS ABA GERAL
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 3 · Aba Geral","Gráficos — Tickets Diários, por Cargo e por Status",
       "Três lentes complementares sobre o fluxo de vagas")
footer(s, 9)

graphs = [
    ("Tickets Diários por Tipo","Colunas agrupadas · por dia",
     "Revela o ritmo de abertura de vagas. Picos isolados indicam campanhas de contratação; picos sustentados revelam crescimento estrutural. A separação por tipo (R&S vs. Admissão) mostra qual processo está mais demandado.",
     "Séries temporais diárias são as únicas capazes de identificar sazonalidade de curto prazo. Barras (vs. linhas) facilitam a leitura de volume absoluto."),
    ("Tickets por Cargo","Barras horizontais · ranking",
     "Responde: 'qual posição mais pressiona o time?'. Cargos recorrentes no topo indicam alta rotatividade ou expansão sistemática — devem receber atenção especial (banco de talentos, triagem automatizada).",
     "Nomes de cargos são longos. Barras horizontais acomodam o label sem truncamento e favorecem a leitura natural de rankings de cima para baixo."),
    ("Tickets por Status","Barras horizontais · distribuição",
     "Mapeia gargalos do processo. Se um status acumula muito volume (ex: 'Aguardando Gestor'), há uma etapa travada que não depende do recrutador — é um sinal para ação de gestão.",
     "Permite ver onde as vagas estão 'paradas' em tempo real — algo impossível em relatórios estáticos. Integrado ao filtro de período, é uma fotografia instantânea do processo."),
]
for i,(nm,sub,body,why) in enumerate(graphs):
    xi = Inches(0.55)+i*Inches(4.28)
    ss_placeholder(s, xi, Inches(1.65), Inches(4.0), Inches(1.9), nm, "Inserir screenshot aqui")
    card(s, xi, Inches(3.62), Inches(4.0), Inches(1.52), sub, body)
    box(s, xi, Inches(5.2), Inches(4.0), Inches(1.68), C_PALE, None)
    tx(s,"Por que esse visual?", xi+Inches(0.12), Inches(5.28), Inches(3.8), Inches(0.3),
       fs=10, color=C_DARK, bold=True)
    tx(s,why, xi+Inches(0.12), Inches(5.6), Inches(3.8), Inches(1.2),
       fs=9.5, color=C_TXTM, wrap=True)

# ════════════════════════════════════════════════════════════════
# SLIDE 10 — ABA DETALHAMENTO
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 4 · Aba Detalhamento","Aba Detalhamento — Análise Multidimensional",
       "De onde vem a demanda? Quatro perspectivas simultâneas")
footer(s, 10)

ss_placeholder(s, Inches(0.55), Inches(1.65), Inches(7.8), Inches(5.08),
               "Aba Detalhamento — Print completo",
               "Capturar os 4 gráficos: Unidade, Nível, Regime Trabalhista e Motivo de Abertura")

det = [
    ("🏢 Por Unidade",
     "Identifica quais unidades concentram a demanda. Essencial para planejamento de capacidade: se uma unidade tem demanda 3x maior, pode ser necessário um recrutador dedicado.",
     C_MID, C_WHITE),
    ("📊 Por Nível Hierárquico",
     "Detalha se a demanda é operacional (auxiliar, assistente) ou estratégica (coordenador, gerente). Cargos sênior têm SLA naturalmente maior — saber a composição evita falsas comparações.",
     C_MID, C_WHITE),
    ("📋 Por Regime Trabalhista",
     "CLT, PJ, estágio — cada regime tem processo de admissão diferente. Concentração em PJ pode indicar estratégia de contenção de custos a ser monitorada pela diretoria.",
     C_MID, C_WHITE),
    ("🔍 Por Motivo de Abertura",
     "O indicador mais estratégico desta aba. Alta concentração em 'Substituição' sinaliza problema de retenção. 'Expansão' confirma crescimento real. Informa decisões de RH muito além do recrutamento.",
     C_GOLD, C_GOLDLT),
]
for i,(tit,body,acc,bg) in enumerate(det):
    card(s, Inches(8.7), Inches(1.65)+i*Inches(1.28), Inches(4.28), Inches(1.15), tit, body, acc=acc, bg=bg, body_fs=9.5)

# ════════════════════════════════════════════════════════════════
# SLIDE 11 — DEFESA DETALHAMENTO
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 4 · Aba Detalhamento","Por que analisar 4 dimensões ao mesmo tempo?",
       "O cruzamento entre dimensões gera insights impossíveis de obter isoladamente")
footer(s, 11)

callout(s,Inches(0.55),Inches(1.65),Inches(5.95),Inches(1.4),
        "💡 Exemplo prático: 'Alta demanda na Unidade X por cargos de nível Auxiliar, com motivo Substituição' = a unidade X tem turnover elevado em posições operacionais. Isso não apareceria se cada dimensão fosse analisada separadamente.",
        bg=C_PALE, border=C_LIGHT)
callout(s,Inches(6.7),Inches(1.65),Inches(5.95),Inches(1.4),
        "⚡ Cross-filter nativo: clicar em uma barra de 'Unidade' filtra automaticamente os outros 3 gráficos. Elimina a necessidade de dezenas de relatórios segmentados — um único dashboard responde a qualquer recorte em segundos.",
        bg=C_GOLDLT, border=C_GOLD)

divider(s, Inches(3.2))

dims = [
    ("🏢","Unidade","Responde: 'onde está a maior pressão de contratação?'", C_PALE),
    ("📊","Nível","Responde: 'a demanda é operacional ou estratégica?'", C_PALE),
    ("📋","Regime","Responde: 'qual perfil contratual está sendo priorizado?'", C_PALE),
    ("🔍","Motivo","Substituição vs. Crescimento — qual narrativa prevalece?", C_GOLDLT),
]
for i,(icon,nm,q,bg) in enumerate(dims):
    xi = Inches(0.55)+i*Inches(3.12)
    box(s, xi, Inches(3.35), Inches(2.95), Inches(2.1), bg, C_GBORD, 0.5)
    tx(s,icon, xi, Inches(3.45), Inches(2.95), Inches(0.55), fs=28, align=PP_ALIGN.CENTER)
    tx(s,nm, xi, Inches(4.0), Inches(2.95), Inches(0.38), fs=14, color=C_DARK, bold=True, align=PP_ALIGN.CENTER)
    tx(s,q, xi+Inches(0.1), Inches(4.45), Inches(2.75), Inches(0.75), fs=10, color=C_TXTMU, align=PP_ALIGN.CENTER)

box(s, Inches(0.55), Inches(5.62), Inches(12.23), Inches(1.25), C_PALE)
tx(s,"📋 Decisões habilitadas por essa aba:",Inches(0.75),Inches(5.72),Inches(12),Inches(0.3),fs=11,color=C_DARK,bold=True)
tx(s,"Definir prioridades de atribuição de vagas · Identificar unidades que precisam de processo seletivo contínuo · Sinalizar áreas com alta rotatividade para o BP de RH · Planejar a capacidade do time P&C no trimestre seguinte",
   Inches(0.75),Inches(6.05),Inches(12),Inches(0.75),fs=10,color=C_TXTM,wrap=True)

# ════════════════════════════════════════════════════════════════
# SLIDE 12 — ABA AGING (overview)
# ════════════════════════════════════════════════════════════════
s = new_slide()
C_RED_DARK = rgb(124,45,18)
header(s,"Bloco 5 · Aba Aging","Aba Aging — O Radar de Risco de Prazo",
       "A aba mais crítica para evitar que vagas virem problema para o negócio", bg=C_RED_DARK)
footer(s, 12)

ss_placeholder(s, Inches(0.55), Inches(1.65), Inches(8.0), Inches(5.08),
               "Aba Aging — Print completo",
               "Capturar: card Insight SLA, gráfico de distribuição por faixa e tabela de vagas críticas")

aging_side = [
    ("⚠️ Por que essa aba é prioritária?",
     "Uma vaga aberta é um custo oculto: perda de produtividade, sobrecarga na equipe, risco de meta. Identificar vagas em risco ANTES do vencimento do SLA permite intervenção proativa — não reativa.",
     C_RED, C_RED_BG),
    ("🤖 Card 'Insight SLA'",
     "Texto automático que classifica a saúde atual do SLA como saudável, em alerta ou crítico. É a primeira leitura ao entrar na aba — direciona a atenção para o ponto mais urgente sem precisar interpretar gráficos.",
     C_MID, C_WHITE),
    ("📋 Tabela de Vagas Críticas",
     "Lista nominal de cada vaga acima de 30 dias com: ticket, cargo, marca, recrutador responsável, gestor solicitante e aging em dias. Permite ação direta — ligar para o recrutador, escalar o caso.",
     C_MID, C_WHITE),
]
for i,(tit,body,acc,bg) in enumerate(aging_side):
    card(s, Inches(8.85), Inches(1.65)+i*Inches(1.68), Inches(4.1), Inches(1.52), tit, body, acc=acc, bg=bg, body_fs=9.5)

# ════════════════════════════════════════════════════════════════
# SLIDE 13 — DISTRIBUIÇÃO AGING
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 5 · Aba Aging","Gráfico de Distribuição de Aging",
       "A 'pirâmide de urgência' das vagas abertas — do saudável ao crítico", bg=C_RED_DARK)
footer(s, 13)

ss_placeholder(s, Inches(0.55), Inches(1.65), Inches(5.5), Inches(2.5),
               "Gráfico de Aging — Distribuição por faixa","Inserir screenshot aqui")

faixas = [
    ("0–7 dias",  "Saudável",                  rgb(22,163,74),  "Dentro das metas de R&S (≤15d) e ADM (≤10d). Fluxo normal — nenhuma ação adicional necessária."),
    ("8–15 dias", "Atenção — ADM acima do SLA", rgb(101,163,13), "Vagas ADM já ultrapassaram a meta de 10 dias. Vagas R&S estão no limite. Verificar andamento e cobrar atualização."),
    ("16–30 dias","Risco — ambos os SLAs vencidos", rgb(217,119,6), "Tanto o SLA de R&S (>15d) quanto o de ADM (>10d) foram ultrapassados. Requer intervenção imediata do responsável."),
    ("+30 dias",  "CRÍTICAS — intervenção obrigatória", rgb(220,38,38), "Threshold crítico superado. Escalonamento para liderança e revisão das condições da vaga (salário, requisitos, processo)."),
]
for i,(faixa,status,color,desc) in enumerate(faixas):
    yi = Inches(4.28)+i*Inches(0.5)
    tx(s,faixa, Inches(0.55), yi, Inches(1.3), Inches(0.42), fs=10, color=C_TXTM, bold=True, align=PP_ALIGN.RIGHT)
    bw = Inches(max(0.8, 2.0-i*0.25))
    box(s, Inches(2.0), yi+Inches(0.06), bw, Inches(0.32), color)
    tx(s,status, Inches(2.0)+bw+Inches(0.12), yi, Inches(3.2), Inches(0.4), fs=10, color=C_TXTM, bold=False)

for i,(faixa,status,color,desc) in enumerate(faixas):
    y = Inches(1.65)+i*Inches(1.05)
    box(s, Inches(6.3), y, Inches(6.68), Inches(0.92), C_GRAY)
    box(s, Inches(6.3), y, Inches(0.06), Inches(0.92), color)
    tx(s,faixa+" — "+status, Inches(6.48), y+Inches(0.09), Inches(6.35), Inches(0.3), fs=11, color=C_TXTD, bold=True)
    tx(s,desc, Inches(6.48), y+Inches(0.43), Inches(6.35), Inches(0.44), fs=9.5, color=C_TXTM, wrap=True)

# ════════════════════════════════════════════════════════════════
# SLIDE 14 — HISTÓRICO SLA
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 5 · Aba Aging","Gráfico de Linhas — SLA Histórico Mensal",
       "A evolução do tempo médio de fechamento ao longo dos meses", bg=C_RED_DARK)
footer(s, 14)

ss_placeholder(s, Inches(0.55), Inches(1.65), Inches(5.8), Inches(3.1),
               "Linha Histórica SLA R&S vs. ADM",
               "Capturar o gráfico de linhas com 2 séries: Aging Médio R&S e Aging Médio ADM ao longo dos meses")
for i,(nm,lbl,bg,fc) in enumerate([
    ("Linha R&S","Meta: ≤ 15 dias",rgb(220,252,231),rgb(21,128,61)),
    ("Linha ADM","Meta: ≤ 10 dias",rgb(255,247,237),rgb(194,65,12)),
]):
    xi = Inches(0.55)+i*Inches(2.95)
    box(s, xi, Inches(4.9), Inches(2.7), Inches(0.72), bg)
    tx(s,nm, xi, Inches(4.97), Inches(2.7), Inches(0.3), fs=11, color=fc, bold=True, align=PP_ALIGN.CENTER)
    tx(s,lbl, xi, Inches(5.27), Inches(2.7), Inches(0.28), fs=9, color=C_TXTMU, align=PP_ALIGN.CENTER)

sla_args = [
    ("📈 Por que gráfico de linhas?",
     "Linhas são o visual ideal para tendências temporais. Conectam os pontos no tempo e tornam visível se o SLA está subindo (piora) ou descendo (melhora) mês a mês — algo impossível de ver em barras de período único.",
     C_GOLD, C_GOLDLT),
    ("🔍 O que monitorar no gráfico",
     "▸ Tendência de alta: processo desacelerando — investigar causa\n▸ Tendência de baixa: processo melhorando — documentar e replicar\n▸ R&S acima de ADM: atípico, indica problema na seleção\n▸ Picos isolados: meses com vagas muito complexas",
     C_MID, C_WHITE),
    ("📊 Por que duas séries separadas?",
     "R&S e ADM têm naturezas distintas e responsáveis diferentes. Uma linha consolidada mascara qual parte do processo gerou o desvio. Duas linhas permitem diagnóstico preciso: é na seleção ou na admissão?",
     C_MID, C_WHITE),
    ("📌 Medidas técnicas utilizadas",
     "Aging_Médio_Hist_RS e Aging_Médio_Hist_ADM: calculam a média de SLA das vagas FECHADAS no período, usando USERELATIONSHIP para garantir que a data de fechamento (não de abertura) é o eixo temporal correto.",
     C_LIGHT, C_PALE),
]
for i,(tit,body,acc,bg) in enumerate(sla_args):
    card(s, Inches(6.65), Inches(1.65)+i*Inches(1.38), Inches(6.3), Inches(1.22), tit, body, acc=acc, bg=bg, body_fs=9.5)

# ════════════════════════════════════════════════════════════════
# SLIDE 15 — ABA UPDATE
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 6 · Abas Operacionais","Aba Update — Gestão Operacional em Tempo Real",
       "O painel do dia a dia do recrutador e do gestor de P&C")
footer(s, 15)

ss_placeholder(s, Inches(0.55), Inches(1.65), Inches(8.0), Inches(5.08),
               "Aba Update — Print da tabela",
               "Capturar a tabela UPDATE com: status, ticket, tipo de solicitação, cargo e histórico do processo")

upd = [
    ("🎯 Para que serve",
     "Substitui o uso de planilhas e e-mails de acompanhamento. Qualquer gestor pode ver em que etapa está a vaga dele — sem precisar ligar para o P&C.",
     C_GOLD, C_GOLDLT),
    ("🗂️ Coluna 'Histórico do Processo'",
     "Registro textual de todas as atualizações da vaga. O gestor lê o histórico completo sem consultar outras fontes — reduz interrupções no time e aumenta a autonomia do solicitante.",
     C_MID, C_WHITE),
    ("🔧 5 Filtros combinados",
     "Período · Tipo de Solicitação · Ticket · Situação · Status. Cada filtro é independente e combinável — qualquer vaga é encontrada em segundos, mesmo em meses de alto volume.",
     C_MID, C_WHITE),
    ("📌 Diferencial técnico",
     "A aba exclui automaticamente vagas fechadas. O gestor sempre vê apenas o que está EM ANDAMENTO, sem ruído de histórico finalizado. Não há risco de confundir o status atual.",
     C_LIGHT, C_PALE),
]
for i,(tit,body,acc,bg) in enumerate(upd):
    card(s, Inches(8.85), Inches(1.65)+i*Inches(1.3), Inches(4.1), Inches(1.15), tit, body, acc=acc, bg=bg, body_fs=9.5)

# ════════════════════════════════════════════════════════════════
# SLIDE 16 — ABA CONSULTA
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 6 · Abas Operacionais","Aba Consulta — Rastreabilidade Total",
       "Encontre qualquer vaga, de qualquer período, em segundos")
footer(s, 16)

ss_placeholder(s, Inches(0.55), Inches(1.65), Inches(5.8), Inches(3.2),
               "Aba Consulta — tabela e filtros","Inserir screenshot aqui")
callout(s,Inches(0.55),Inches(5.0),Inches(5.8),Inches(1.68),
        "💡 Caso de uso típico: 'Preciso saber quando o João foi contratado e qual era o salário previsto.' → Filtrar pelo nome na aba Consulta e ver todas as informações em uma tabela estruturada, sem precisar abrir planilhas ou ligar para o P&C.",
        bg=C_GOLDLT, border=C_GOLD)

cons = [
    ("📅 Filtro por Data de Fechamento",
     "Permite recuperar vagas de qualquer período histórico. A Consulta é um arquivo vivo — tudo que já aconteceu está acessível por recorte temporal, sem limitações."),
    ("👤 Filtro por Candidato",
     "Localiza todas as vagas associadas a um candidato. Útil para auditoria, confirmação de histórico de contratação e verificação de candidaturas anteriores na empresa."),
    ("🗂️ Tabela Geral — 12 colunas",
     "Status · Ticket · Nível · Cargo · Marca · Candidato · Recrutador · Gestor · Data Abertura · Data Fechamento · Data Início Prevista · Remuneração. Cobre 100% das necessidades de auditoria."),
    ("⚖️ Valor para a diretoria",
     "Em auditorias ou questionamentos jurídicos, todas as informações estão centralizadas, rastreáveis e exportáveis — eliminando a dependência de planilhas locais dos recrutadores."),
]
for i,(tit,body) in enumerate(cons):
    card(s, Inches(6.65), Inches(1.65)+i*Inches(1.38), Inches(6.3), Inches(1.22), tit, body, body_fs=9.5)

# ════════════════════════════════════════════════════════════════
# SLIDE 17 — PERFORMANCE RECRUTADORES
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 7 · Performance","Performance de Recrutadores — Janela de 3 Meses",
       "Avaliação justa, baseada em dados e com contexto temporal adequado")
footer(s, 17)

ss_placeholder(s, Inches(0.55), Inches(1.65), Inches(5.8), Inches(2.6),
               "Tabela de Recrutadores — 3M","Inserir screenshot aqui")
for i,(val,lbl,bg) in enumerate([
    ("20","Meta mensal\n(fechamentos)",C_DARK),
    ("3M","Janela de\navaliação",C_MID),
    ("Ativo","Meses como\ndenominador",C_MID),
]):
    kpi_pill(s, Inches(0.55)+i*Inches(1.98), Inches(4.38), Inches(1.85), Inches(1.3), val, lbl, bg=bg)

rec_m = [
    ("Rec_Total_3M — Produção real",
     "Total de vagas fechadas nos últimos 3 meses completos (exclui mês atual). A janela de 3 meses suaviza variações pontuais — um mês ruim por férias não distorce o resultado do consultor.",
     "Janela: EDATE(InicioMesAtual,-3) até InicioMesAtual-1"),
    ("Rec_Total_3M_Média_Mensal — Comparabilidade",
     "Média mensal ajustada pelos meses em que o consultor esteve ativo. Permite comparar consultores que entraram em datas diferentes de forma justa, sem penalizar quem é mais recente.",
     "Fórmula: Total_3M ÷ MesesAtivos_RS_3M"),
    ("% Cumprimento_Meta_3M — Aderência à meta",
     "Percentual do total fechado em relação à meta de 20 vagas/mês × meses ativos. Identifica quem está acima, na meta ou abaixo. É o indicador final de desempenho individual.",
     "Fórmula: Total_3M ÷ Meta_3M · Meta_3M = MesesAtivos × 20"),
    ("Por que excluir o mês atual?",
     "O mês em curso ainda está incompleto — incluí-lo distorceria a média para baixo. A janela de 3 meses fechados garante que a avaliação é sempre baseada em dados completos e comparáveis.",
     "Critério de integridade: apenas meses com dados 100% fechados entram na janela"),
]
for i,(nm,why,meta) in enumerate(rec_m):
    metric_row(s, Inches(6.38), Inches(1.65)+i*Inches(1.4), Inches(6.58), Inches(1.25), nm, why, meta)

# ════════════════════════════════════════════════════════════════
# SLIDE 18 — DEFESA INDICADORES (tabela)
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 7 · Performance","Defesa dos Indicadores — Por que essas métricas?",
       "Cada indicador foi escolhido por sua capacidade de habilitar uma decisão específica")
footer(s, 18)

# Header da tabela
col_xs  = [Inches(0.55), Inches(3.05), Inches(4.35), Inches(8.98)]
col_ws  = [Inches(2.45), Inches(1.25), Inches(4.58), Inches(4.0)]
hdr_row = ["Indicador","Tipo","Decisão que habilita","O que acontece sem ele"]
hdr_y = Inches(1.62); hdr_h = Inches(0.4)
for hdr,xi,wi in zip(hdr_row,col_xs,col_ws):
    box(s, xi, hdr_y, wi, hdr_h, C_DARK)
    tx(s,hdr, xi+Inches(0.08), hdr_y+Inches(0.07), wi-Inches(0.1), hdr_h,
       fs=10, color=C_WHITE, bold=True)

rows_data = [
    ("Vagas Fechadas MTD","Volume","Avaliar ritmo de entrega do time no mês corrente","Não se sabe se o time está no caminho certo até o fim do mês"),
    ("SLA R&S (≤15d) / ADM (≤10d)","Qualidade","Avaliar se os contratos de prazo com o negócio estão sendo cumpridos","Gestores reclamam de demora sem dados para confirmar ou refutar"),
    ("MoM SLA %","Tendência","Identificar se o processo está melhorando ou piorando mês a mês","Melhoras ou pioras graduais passam despercebidas por meses"),
    ("Aging por Faixa","Risco","Priorizar intervenção nas vagas com maior risco de vencer o SLA","Vagas críticas são descobertas só quando já estão vencidas"),
    ("Taxa de Cancelamento","Qualidade","Detectar solicitações mal planejadas que não foram concluídas","Trabalho desperdiçado é invisível para a gestão"),
    ("% Meta 3M (Recrutador)","Individual","Avaliar performance individual com justiça e contexto temporal adequado","Avaliação subjetiva gera conflitos baseados em percepção"),
    ("Motivo de Abertura","Estratégico","Distinguir demanda de reposição vs. crescimento — insumo para RH","Turnover elevado em unidades específicas passa despercebido"),
]
tag_style = {
    "Volume":    (C_PALE,              C_DARK),
    "Qualidade": (C_PALE,              C_DARK),
    "Tendência": (C_GOLDLT,            rgb(124,79,0)),
    "Risco":     (rgb(254,226,226),    rgb(185,28,28)),
    "Individual":(C_PALE,              C_DARK),
    "Estratégico":(C_GOLDLT,           rgb(124,79,0)),
}
rh = Inches(0.63)
for r,(ind,tipo,dec,sem) in enumerate(rows_data):
    ry = hdr_y + hdr_h + r*rh
    bg_r = C_GRAY if r%2==0 else C_WHITE
    for ci,(xi,wi) in enumerate(zip(col_xs,col_ws)):
        box(s, xi, ry, wi, rh, bg_r)
        vals = [ind,tipo,dec,sem]
        if ci == 1:
            tb,tc = tag_style.get(tipo,(C_GRAY,C_TXTM))
            box(s, xi+Inches(0.08), ry+Inches(0.17), wi-Inches(0.16), Inches(0.28), tb)
            tx(s,tipo, xi+Inches(0.08), ry+Inches(0.17), wi-Inches(0.16), Inches(0.28),
               fs=9, color=tc, bold=True, align=PP_ALIGN.CENTER)
        else:
            tx(s,vals[ci], xi+Inches(0.08), ry+Inches(0.1), wi-Inches(0.12), rh-Inches(0.15),
               fs=9.5 if ci==0 else 9.5, color=C_TXTD if ci==0 else C_TXTM,
               bold=(ci==0), wrap=True)

# ════════════════════════════════════════════════════════════════
# SLIDE 19 — IMPACTO ESTRATÉGICO
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Bloco 7 · Impacto","Impacto Estratégico do Dashboard",
       "O que muda na organização com esse nível de visibilidade")
footer(s, 19)

impacts = [
    ("⚡","Velocidade de Decisão",
     "Reuniões que antes exigiam preparação prévia partem diretamente do dashboard. A resposta de 'como está o recrutamento?' sai em 30 segundos — com dados, não com impressões."),
    ("🎯","Gestão Proativa de Risco",
     "O Aging muda o paradigma: de 'apagar incêndios' para 'prevenir'. Vagas em risco são identificadas com 7–14 dias de antecedência antes do vencimento do SLA."),
    ("🤝","Transparência com o Negócio",
     "Gestores acompanham suas vagas sem acionar o P&C. Reduz interrupções, aumenta a confiança na área e posiciona o P&C como parceiro estratégico — não apenas executor."),
]
for i,(icon,tit,body) in enumerate(impacts):
    xi = Inches(0.55)+i*Inches(4.28)
    box(s, xi, Inches(1.62), Inches(4.0), Inches(2.65), C_DARK)
    tx(s,icon, xi, Inches(1.72), Inches(4.0), Inches(0.65), fs=32, align=PP_ALIGN.CENTER)
    tx(s,tit, xi, Inches(2.4), Inches(4.0), Inches(0.45), fs=15, color=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    tx(s,body, xi+Inches(0.15), Inches(2.9), Inches(3.7), Inches(1.22), fs=10.5, color=rgb(210,240,225), wrap=True)

divider(s, Inches(4.42))

callouts_b = [
    (C_PALE,   C_LIGHT, "📈 Planejamento de capacidade:", "Com dados históricos de volume por período e marca, é possível prever os meses de maior demanda e planejar reforços no time com antecedência."),
    (C_GOLDLT, C_GOLD,  "🏢 Visão por marca:",            "7 interfaces independentes permitem que cada marca acompanhe sua operação, enquanto o dashboard central mantém a visão consolidada para a diretoria."),
    (C_PALE,   C_LIGHT, "⚖️ Performance justa:",          "O modelo 3M com meses ativos como denominador elimina distorções para consultores novos ou de licença — avaliação baseada em dados, não em percepção."),
    (C_GOLDLT, C_GOLD,  "🔗 Integração com fontes vivas:","Dados conectados ao Google Sheets e Dataflow garantem que o dashboard reflete o que está acontecendo agora — sem defasagem de atualização manual."),
]
for i,(bg,border,tit,body) in enumerate(callouts_b):
    xi = Inches(0.55)+(i%2)*Inches(6.45)
    yi = Inches(4.58)+(i//2)*Inches(1.12)
    callout(s, xi, yi, Inches(6.1), Inches(1.0), tit+"  "+body, bg=bg, border=border)

# ════════════════════════════════════════════════════════════════
# SLIDE 20 — PRÓXIMOS PASSOS
# ════════════════════════════════════════════════════════════════
s = new_slide()
header(s,"Encerramento","Próximos Passos & Evolução do Dashboard",
       "O que está planejado para ampliar o valor analítico da área")
# Custom footer for last slide
box(s, 0, Inches(7.05), W, Inches(0.45), C_DARK)
box(s, 0, Inches(7.05), W, Inches(0.025), C_GOLD)
tx(s,"Raíz Educação · P&C Analytics · Confidencial",
   Inches(0.55),Inches(7.1),Inches(7),Inches(0.32),fs=9,color=rgb(120,160,140))
tx(s,"Obrigado(a) · Dúvidas e perguntas?",
   Inches(5.0),Inches(7.1),Inches(5),Inches(0.32),fs=11,color=C_GOLD,bold=True,align=PP_ALIGN.CENTER)
tx(s,"20 / 20",Inches(12.0),Inches(7.1),Inches(1.2),Inches(0.32),fs=9,color=C_GOLD,bold=True,align=PP_ALIGN.RIGHT)

tx(s,"Curto Prazo", Inches(0.55), Inches(1.62), Inches(5.8), Inches(0.38), fs=14, color=C_DARK, bold=True)
short = [
    ("✅ Treinamento do time de P&C",
     "Capacitar recrutadores e BP de RH para uso pleno das 5 abas — especialmente Aging e Update, de maior impacto no dia a dia operacional."),
    ("✅ Rotina semanal com o dashboard",
     "Institucionalizar o uso do Aging às segundas-feiras e do Geral nas reuniões de equipe — transformando o dashboard em artefato padrão de gestão."),
    ("✅ Inserção dos prints nesta apresentação",
     "Capturar os screenshots do Power BI e substituir os placeholders pelas imagens reais, aumentando o impacto visual nas próximas apresentações."),
]
for i,(tit,body) in enumerate(short):
    card(s, Inches(0.55), Inches(2.05)+i*Inches(1.55), Inches(5.8), Inches(1.38), tit, body, acc=C_MID, bg=C_PALE, body_fs=9.5)

tx(s,"Médio Prazo", Inches(7.0), Inches(1.62), Inches(5.8), Inches(0.38), fs=14, color=C_DARK, bold=True)
med = [
    ("🔭 RLS por recrutador",
     "Implementar Row-Level Security para que cada recrutador veja apenas suas vagas — mantendo a visão consolidada apenas para gestores e diretoria."),
    ("🔭 Integração com dados de desligamentos",
     "Cruzar o volume de Substituições com dados de demissões por marca para identificar cargos com turnover estrutural — não apenas pontual."),
    ("🔭 Alerta automático por e-mail",
     "Configurar alertas do Power BI Service para notificar automaticamente quando uma vaga entra na faixa de 16–30 dias — antes que vire risco real."),
]
for i,(tit,body) in enumerate(med):
    card(s, Inches(7.0), Inches(2.05)+i*Inches(1.55), Inches(5.95), Inches(1.38), tit, body, acc=C_GOLD, bg=C_GOLDLT, body_fs=9.5)

# ════════════════════════════════════════════════════════════════
# SALVAR
# ════════════════════════════════════════════════════════════════
OUTPUT = r"C:\Users\marce\Documents\Raíz Educação\Dados P&C\Apresentacao_Dashboard_Diretoria.pptx"
prs.save(OUTPUT)
print(f"Salvo: {OUTPUT}")
print(f"Total de slides: {len(prs.slides)}")
