import openpyxl
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter
import os

OUTPUT = os.path.join(
    os.environ['USERPROFILE'],
    "Documents", "Raíz Educação", "De-Para",
    "Dicionário de Dados - Dashboard P&C.xlsx"
)

# ─── CORES ────────────────────────────────────────────────────────────────────
COR_PBI_HEADER   = "1F3864"   # Azul escuro Power BI
COR_LS_HEADER    = "E65C00"   # Laranja Looker Studio
COR_DEPARA_HEADER = "2E7D32"  # Verde mapeamento
COR_ALT1         = "D6E4F7"   # Azul claro alternado
COR_ALT2         = "FFF3E0"   # Laranja claro alternado
COR_ALT3         = "E8F5E9"   # Verde claro alternado
COR_TITULO_SHEET = "F5F5F5"
COR_BRANCO       = "FFFFFF"

def header_fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def alt_fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def white_fill():
    return PatternFill("solid", fgColor=COR_BRANCO)

def thin_border():
    s = Side(style="thin", color="BDBDBD")
    return Border(left=s, right=s, top=s, bottom=s)

def header_font(white=True):
    return Font(name="Calibri", bold=True, size=11,
                color="FFFFFF" if white else "212121")

def body_font():
    return Font(name="Calibri", size=10)

def wrap_align(h="left"):
    return Alignment(wrap_text=True, vertical="top", horizontal=h)

def set_col_widths(ws, widths):
    for col_letter, width in widths.items():
        ws.column_dimensions[col_letter].width = width

def write_header_row(ws, row, headers, fill_color, font_white=True):
    for col, text in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col, value=text)
        cell.fill = header_fill(fill_color)
        cell.font = header_font(font_white)
        cell.alignment = Alignment(wrap_text=True, vertical="center",
                                   horizontal="center")
        cell.border = thin_border()

def write_data_row(ws, row, values, fill_hex, bold_first=False):
    for col, val in enumerate(values, 1):
        cell = ws.cell(row=row, column=col, value=val)
        cell.fill = alt_fill(fill_hex) if fill_hex else white_fill()
        f = Font(name="Calibri", size=10,
                 bold=(bold_first and col == 1))
        cell.font = f
        cell.alignment = wrap_align()
        cell.border = thin_border()

# ══════════════════════════════════════════════════════════════════════════════
wb = openpyxl.Workbook()

# ─────────────────────────────── ABA 1: Capa ──────────────────────────────────
ws_capa = wb.active
ws_capa.title = "Capa"
ws_capa.sheet_view.showGridLines = False
ws_capa.column_dimensions["A"].width = 60
ws_capa.row_dimensions[1].height = 20

linhas_capa = [
    ("DICIONÁRIO DE DADOS – DASHBOARD MÉTRICAS P&C", COR_PBI_HEADER, 28, True),
    ("", None, 12, False),
    ("Arquivo Power BI:   Dashboard Métricas P&C.pbix", None, 12, False),
    ("Dashboard Looker:   DASHBOARD RH – 2026", None, 12, False),
    ("Área:               Recursos Humanos – Recrutamento & Seleção", None, 12, False),
    ("Data de referência: Abril / 2026", None, 12, False),
    ("", None, 12, False),
    ("CONTEÚDO DAS ABAS", COR_DEPARA_HEADER, 13, True),
    ("", None, 12, False),
    ("Aba 1 – Capa              │ Esta página", None, 11, False),
    ("Aba 2 – Power BI          │ Dicionário completo das tabelas, colunas e medidas do .pbix", None, 11, False),
    ("Aba 3 – Looker Studio     │ Dicionário dos campos e visuais do dashboard Looker", None, 11, False),
    ("Aba 4 – De-Para           │ Mapeamento campo a campo entre os dois dashboards", None, 11, False),
    ("Aba 5 – Visuais Comparados│ Comparativo visual por visual entre as duas ferramentas", None, 11, False),
]

for i, (texto, cor, fs, bold) in enumerate(linhas_capa, 1):
    cell = ws_capa.cell(row=i, column=1, value=texto)
    if cor:
        cell.fill = PatternFill("solid", fgColor=cor)
        cell.font = Font(name="Calibri", bold=True, size=fs, color="FFFFFF")
    else:
        cell.font = Font(name="Calibri", bold=bold, size=fs, color="212121")
    cell.alignment = Alignment(vertical="center")
    ws_capa.row_dimensions[i].height = fs + 6

# ─────────────────────────── ABA 2: Power BI ──────────────────────────────────
ws_pbi = wb.create_sheet("Power BI")
ws_pbi.sheet_view.showGridLines = False

# Título
ws_pbi.merge_cells("A1:J1")
t = ws_pbi["A1"]
t.value = "DICIONÁRIO DE DADOS – POWER BI  │  Dashboard Métricas P&C.pbix"
t.fill = header_fill(COR_PBI_HEADER)
t.font = Font(name="Calibri", bold=True, size=14, color="FFFFFF")
t.alignment = Alignment(horizontal="center", vertical="center")
ws_pbi.row_dimensions[1].height = 28

# Subtítulo tabelas
ws_pbi.merge_cells("A2:J2")
ts = ws_pbi["A2"]
ts.value = "TABELAS DO MODELO"
ts.fill = header_fill("2C5F9E")
ts.font = Font(name="Calibri", bold=True, size=12, color="FFFFFF")
ts.alignment = Alignment(horizontal="center", vertical="center")
ws_pbi.row_dimensions[2].height = 22

# Headers tabelas
headers_tab = ["Tabela / Entidade", "Tipo", "Descrição", "Fonte de Dados",
               "Atualização", "Observações"]
write_header_row(ws_pbi, 3, headers_tab, "3A73C0")
ws_pbi.row_dimensions[3].height = 20

tabelas = [
    ("Fonte_Sheets",
     "Fato / Transacional",
     "Tabela principal de tickets de R&S. Cada linha representa um ticket "
     "de solicitação de vaga aberto. Contém todas as colunas operacionais "
     "do processo seletivo.",
     "Google Sheets (via conector Power BI)",
     "Atualização programada",
     "Tabela central do modelo. Relaciona-se com dCalendario via DATA DE "
     "FECHAMENTO DA VAGA / DATA DE INICIO PREVISTA."),
    ("R&S_CONTROLE DE VAGAS 2026",
     "Medidas / KPIs calculados",
     "Tabela de medidas DAX calculadas para os KPIs de Recrutamento & Seleção "
     "de 2026. Armazena indicadores consolidados como SLA, vagas fechadas, "
     "percentuais e rankings.",
     "Calculada (DAX no modelo)",
     "Calculada em tempo de consulta",
     "Não possui linhas de dados – apenas medidas. Criada para organizar "
     "os cálculos DAX do processo."),
    ("dCalendario",
     "Dimensão – Calendário",
     "Tabela de datas que habilita o drill-down temporal (Ano > Mês > Dia). "
     "Usada como eixo de tempo em todos os gráficos com comparativo anual.",
     "Calculada (DAX / Power Query)",
     "Calculada automaticamente",
     "Tabela padrão de calendário. Permite filtros por Ano, Mês, Dia e "
     "suporta hierarquia de datas nativa do Power BI."),
]

row = 4
for i, t in enumerate(tabelas):
    fill = COR_ALT1 if i % 2 == 0 else COR_BRANCO
    write_data_row(ws_pbi, row, t, fill, bold_first=True)
    ws_pbi.row_dimensions[row].height = 50
    row += 1

row += 1  # linha em branco

# ── Colunas da Fonte_Sheets ──
ws_pbi.merge_cells(f"A{row}:J{row}")
sc = ws_pbi.cell(row=row, column=1,
                 value="COLUNAS – Fonte_Sheets  (Tabela de Tickets / Fato)")
sc.fill = header_fill("2C5F9E")
sc.font = Font(name="Calibri", bold=True, size=12, color="FFFFFF")
sc.alignment = Alignment(horizontal="center", vertical="center")
ws_pbi.row_dimensions[row].height = 22
row += 1

headers_col = ["Campo (nome exato no PBI)", "Tipo de Dado",
               "Descrição / Significado", "Valores de Exemplo / Domínio",
               "Equivalente no Looker Studio", "Observações"]
write_header_row(ws_pbi, row, headers_col, "3A73C0")
ws_pbi.row_dimensions[row].height = 20
row += 1

colunas_fonte = [
    ("TICKET",
     "Texto (ID)",
     "Identificador único de cada solicitação de vaga aberta no sistema de R&S. "
     "Código sequencial gerado pelo sistema.",
     "Ex: T-001, T-1500, #3562",
     "Não mapeado diretamente (Looker usa contagem de registros)",
     "Campo-chave da tabela. Usado como COUNT para o KPI 'Total de Tickets'."),
    ("STATUS",
     "Texto (Categórico)",
     "Situação atual do ticket de solicitação de vaga. Indica em qual etapa "
     "do processo seletivo a vaga se encontra.",
     "Aberta, Fechada, Cancelada, Em andamento, Em aprovação",
     "STATUS (filtro no Looker Studio)",
     "Usado como filtro global e no gráfico 'Ticket por Status'. "
     "Dimensão chave para medir taxa de conclusão."),
    ("NOME COMPLETO",
     "Texto",
     "Nome completo do candidato aprovado ou da posição a ser preenchida. "
     "Usado para consultas individuais.",
     "—",
     "Não visível diretamente nos prints analisados",
     "Visível apenas na aba 'Consulta' do Power BI."),
    ("CARGO",
     "Texto (Categórico)",
     "Nome do cargo da vaga solicitada.",
     "Professor, Coordenador, Auxiliar Administrativo, Analista...",
     "Implícito no NÍVEL do Looker Studio",
     "Usado na aba Performance para análise de ticket por cargo."),
    ("NÍVEL",
     "Texto (Categórico)",
     "Nível hierárquico da vaga dentro da organização.",
     "OPERACIONAL, ESTÁGIO, PEDAGÓGICO, ESTRATÉGICO, TÁTICO, JOVEM APRENDIZ",
     "Dimensão 'Tickets por nível' no Looker Studio",
     "Corresponde diretamente ao gráfico 'Tickets por nível' do Looker Studio."),
    ("MARCA",
     "Texto (Categórico)",
     "Marca / rede de ensino à qual a unidade solicitante pertence.",
     "GLOBAL TREE, APOGEU, MATRIZ EDUCAÇÃO, CLV, QI, RAIZ EDUCACAO, "
     "CUBO GLOBAL SCHOOL, AMERICANO, UNIFICADO, SAP, SARAH DAWSEY, "
     "SÁ PEREIRA, UNIÃO, BOM TEMPO",
     "MARCAS (filtro e dimensão em 'Volume de contratação' no Looker)",
     "Usado como filtro principal em ambos os dashboards. Permite segmentar "
     "todos os indicadores por rede."),
    ("UNIDADE / SETOR",
     "Texto (Categórico)",
     "Unidade escolar específica ou setor corporativo que abriu o ticket.",
     "Nomes das escolas/unidades da rede",
     "Implícito dentro de MARCA no Looker Studio",
     "Usado no gráfico 'Ticket por Unidade' do Power BI. Looker agrega "
     "no nível de MARCA."),
    ("DIRETORIA",
     "Texto (Categórico)",
     "Diretoria responsável pela vaga solicitada.",
     "Diretoria Pedagógica, Diretoria Administrativa, Diretoria Comercial...",
     "Não mapeado explicitamente no Looker Studio",
     "Usado no gráfico 'Ticket por Diretoria' da aba Performance do Power BI."),
    ("SEGMENTO DE ATUAÇÃO",
     "Texto (Categórico)",
     "Segmento de atuação da unidade/escola (ex: Educação Básica, "
     "Educação Infantil, Ensino Superior).",
     "Educação Básica, Educação Infantil, EAD, etc.",
     "Não mapeado no Looker Studio",
     "Usado no gráfico 'Ticket por Segmento de Atuação' do Power BI."),
    ("TIPO DE SOLICITAÇÃO RECEBIDA",
     "Texto (Categórico)",
     "Motivo ou natureza da solicitação de abertura da vaga.",
     "SUBSTITUIÇÃO, AUMENTO DE QUADRO, PEJOTIZAÇÃO, Outros",
     "TIPO DE SO... (filtro e dimensão 'Tickets por tipo de solicitação')",
     "Corresponde ao gráfico 'Tickets por tipo de solicitação' do Looker."),
    ("CONSULTOR DE R&S",
     "Texto (Categórico)",
     "Nome do recrutador responsável pelo processo seletivo do ticket.",
     "RAYSSA, VIVIAN, LANNA, LUCAS FRAZAO, VITOR, MAYARA, "
     "CONSULTORIA DE RH, PABLO, AMANDA, ISABELA, BEATRIZ MARCOTULLIO, NATHANY",
     "Dimensão 'Vagas de R&S fechadas por recrutador' no Looker Studio",
     "Corresponde ao gráfico de vagas fechadas por recrutador do Looker."),
    ("GESTOR DA VAGA",
     "Texto",
     "Nome do gestor da área requisitante, responsável por aprovar e "
     "acompanhar o processo seletivo.",
     "—",
     "Não visível nos prints do Looker Studio",
     "Disponível na aba 'Consulta' do Power BI."),
    ("DATA DE FECHAMENTO DA VAGA",
     "Data",
     "Data em que o processo seletivo foi concluído e a vaga oficialmente "
     "fechada/preenchida.",
     "Formato: DD/MM/AAAA",
     "DATA DE FE... (filtro no Looker Studio)",
     "Base para calcular SLA de R&S. Relaciona-se com dCalendario."),
    ("DATA DE INICIO PREVISTA",
     "Data",
     "Data prevista para o início do colaborador contratado.",
     "Formato: DD/MM/AAAA",
     "DATA DE INI... (filtro no Looker Studio)",
     "Usada para planejamento de onboarding. Base para cálculo do SLA ADM."),
    ("REMUNERAÇÃO",
     "Numérico (Monetário)",
     "Faixa salarial ou valor de remuneração previsto para a vaga.",
     "Valor em R$",
     "Não visível nos prints do Looker Studio",
     "Disponível na aba 'Consulta' do Power BI."),
]

for i, c in enumerate(colunas_fonte):
    fill = COR_ALT1 if i % 2 == 0 else COR_BRANCO
    write_data_row(ws_pbi, row, c, fill)
    ws_pbi.row_dimensions[row].height = 55
    row += 1

row += 1

# ── Medidas DAX ──
ws_pbi.merge_cells(f"A{row}:J{row}")
sc2 = ws_pbi.cell(row=row, column=1,
                  value="MEDIDAS DAX – R&S_CONTROLE DE VAGAS 2026")
sc2.fill = header_fill("2C5F9E")
sc2.font = Font(name="Calibri", bold=True, size=12, color="FFFFFF")
sc2.alignment = Alignment(horizontal="center", vertical="center")
ws_pbi.row_dimensions[row].height = 22
row += 1

headers_med = ["Medida (nome exato)", "Tipo",
               "Descrição / Lógica de Cálculo",
               "Fórmula DAX (resumida)",
               "Equivalente no Looker Studio",
               "Observações"]
write_header_row(ws_pbi, row, headers_med, "3A73C0")
ws_pbi.row_dimensions[row].height = 20
row += 1

medidas = [
    ("VagasFechadas",
     "Medida – Contagem",
     "Total de vagas com status 'Fechada' no período selecionado. "
     "KPI principal do dashboard.",
     "CALCULATE(COUNTROWS(Fonte_Sheets), "
     "Fonte_Sheets[STATUS] = \"Fechada\")",
     "TOTAL DE VAGAS FECHADAS (card no Looker)",
     "Valor acumulado: 2.761 em 2025+2026. Corresponde ao card "
     "'TOTAL DE VAGAS FECHADAS' do Looker."),
    ("VagasFechadasAdmissão",
     "Medida – Contagem",
     "Vagas fechadas que passaram pelo processo de admissão formal, "
     "ou seja, onde o candidato foi efetivamente admitido.",
     "CALCULATE(COUNTROWS(Fonte_Sheets), "
     "[STATUS] = \"Admitido\" || [STATUS] = \"Fechada/Admitida\")",
     "Não mapeado explicitamente no Looker Studio",
     "Diferencia fechamento R&S do fechamento com admissão formalizada."),
    ("PercentualFechadasR&S",
     "Medida – Percentual",
     "Percentual de vagas fechadas pelo time de R&S em relação ao total "
     "de vagas abertas.",
     "[VagasFechadas] / COUNTROWS(Fonte_Sheets)",
     "Calculado implicitamente no Looker",
     "Exibido no card 'Fechadas R&S' no Power BI como percentual."),
    ("PercentualFechadaAdmissao",
     "Medida – Percentual",
     "Percentual de vagas que geraram admissão em relação às fechadas.",
     "[VagasFechadasAdmissão] / [VagasFechadas]",
     "Não mapeado no Looker Studio",
     "Mede a taxa de conversão de fechamento para admissão efetiva."),
    ("SLA_R&S_Médio",
     "Medida – Prazo (dias)",
     "Tempo médio em dias entre a abertura do ticket e o fechamento da "
     "vaga pelo time de R&S.",
     "AVERAGEX(Fonte_Sheets, "
     "Fonte_Sheets[DATA DE FECHAMENTO DA VAGA] - Fonte_Sheets[Data Abertura])",
     "Não mapeado diretamente no Looker Studio",
     "KPI de eficiência do processo seletivo. Exibido no card 'SLA R&S'."),
    ("SLA_ADM_Médio",
     "Medida – Prazo (dias)",
     "Tempo médio em dias entre o fechamento da vaga e o início previsto "
     "do colaborador (processo de admissão).",
     "AVERAGEX(Fonte_Sheets, "
     "Fonte_Sheets[DATA DE INICIO PREVISTA] - Fonte_Sheets[DATA DE FECHAMENTO DA VAGA])",
     "Não mapeado diretamente no Looker Studio",
     "KPI de eficiência do processo de admissão. Exibido no card 'SLA ADM'."),
    ("VagasFechadas Mês Atual (MTD)",
     "Medida – Contagem MTD",
     "Vagas fechadas no mês corrente (Month-To-Date), do dia 1 até hoje.",
     "CALCULATE([VagasFechadas], DATESMTD(dCalendario[Date]))",
     "Não mapeado explicitamente no Looker Studio",
     "Exibido no card 'Vagas Fechadas MTD' na aba Performance."),
    ("VagasFechadas Semana Atual (WTD)",
     "Medida – Contagem WTD",
     "Vagas fechadas na semana corrente (Week-To-Date).",
     "CALCULATE([VagasFechadas], "
     "FILTER(dCalendario, dCalendario[SemanaAno] = [SemanaAtual]))",
     "Não mapeado explicitamente no Looker Studio",
     "Exibido no card 'Vagas Fechadas WTD' na aba Performance."),
    ("Qtd_CadastGupy",
     "Medida – Contagem",
     "Quantidade de candidatos cadastrados na plataforma Gupy "
     "no período filtrado.",
     "COUNTROWS(FILTER(Fonte_Sheets, [Etapa] = \"Cadastro Gupy\"))",
     "Não mapeado no Looker Studio",
     "Indicador de funil de recrutamento. Exibido no card 'Cadastro Gupy'."),
    ("Qtd_EntrevistaLiderança",
     "Medida – Contagem",
     "Quantidade de candidatos que chegaram à etapa de entrevista "
     "com o líder/gestor.",
     "COUNTROWS(FILTER(Fonte_Sheets, [Etapa] = \"Entrevista Liderança\"))",
     "Não mapeado no Looker Studio",
     "Indicador de funil de recrutamento. Exibido no card 'Entrevista'."),
    ("% Acumulado Vagas Fechadas",
     "Medida – Percentual acumulado",
     "Percentual acumulado de vagas fechadas por recrutador em relação "
     "ao total do time, para ranking.",
     "DIVIDE([VagasFechadas], CALCULATE([VagasFechadas], ALL(Fonte_Sheets[CONSULTOR DE R&S])))",
     "Não mapeado no Looker Studio",
     "Usado na tabela de ranking de recrutadores na aba Performance."),
    ("Rank Especialista Ajustado",
     "Medida – Ranking",
     "Posição do recrutador no ranking de vagas fechadas, ajustada por "
     "critérios de desempate.",
     "RANKX(ALL(Fonte_Sheets[CONSULTOR DE R&S]), [VagasFechadas], , DESC)",
     "Não mapeado no Looker Studio",
     "Exibido como primeira coluna da tabela de recrutadores."),
]

for i, m in enumerate(medidas):
    fill = COR_ALT1 if i % 2 == 0 else COR_BRANCO
    write_data_row(ws_pbi, row, m, fill, bold_first=True)
    ws_pbi.row_dimensions[row].height = 60
    row += 1

# Larguras Power BI
set_col_widths(ws_pbi, {
    "A": 35, "B": 22, "C": 55, "D": 50, "E": 40, "F": 50
})

# ─────────────────────── ABA 3: Looker Studio ─────────────────────────────────
ws_ls = wb.create_sheet("Looker Studio")
ws_ls.sheet_view.showGridLines = False

ws_ls.merge_cells("A1:G1")
t2 = ws_ls["A1"]
t2.value = "DICIONÁRIO DE DADOS – LOOKER STUDIO  │  DASHBOARD RH – 2026"
t2.fill = header_fill(COR_LS_HEADER)
t2.font = Font(name="Calibri", bold=True, size=14, color="FFFFFF")
t2.alignment = Alignment(horizontal="center", vertical="center")
ws_ls.row_dimensions[1].height = 28

# Seção: Filtros globais
row_ls = 2
ws_ls.merge_cells(f"A{row_ls}:G{row_ls}")
sf = ws_ls.cell(row=row_ls, column=1, value="FILTROS GLOBAIS – Aba: Recrutamento & Seleção")
sf.fill = header_fill("BF360C")
sf.font = Font(name="Calibri", bold=True, size=12, color="FFFFFF")
sf.alignment = Alignment(horizontal="center", vertical="center")
ws_ls.row_dimensions[row_ls].height = 22
row_ls += 1

headers_filtros = ["Filtro (label no Looker)", "Campo Subjacente",
                   "Tipo", "Descrição", "Valores Possíveis",
                   "Equivalente Power BI", "Observações"]
write_header_row(ws_ls, row_ls, headers_filtros, "D84315")
ws_ls.row_dimensions[row_ls].height = 20
row_ls += 1

filtros_ls = [
    ("STATUS",
     "STATUS",
     "Filtro de seleção múltipla",
     "Filtra todos os visuais da página pelo status atual do ticket de vaga.",
     "Aberta, Fechada, Cancelada, Em andamento",
     "Slicer STATUS (Power BI)",
     "Filtro global que afeta todos os gráficos da página."),
    ("TIPO DE SO... (Tipo de Solicitação)",
     "TIPO DE SOLICITAÇÃO RECEBIDA",
     "Filtro de seleção múltipla",
     "Filtra por tipo de solicitação: substituição, aumento de quadro ou pejotização.",
     "SUBSTITUIÇÃO, AUMENTO DE QUADRO, PEJOTIZAÇÃO, Outros",
     "Slicer / campo TIPO DE SOLICITAÇÃO RECEBIDA (Power BI)",
     "Label truncado no Looker. Nome completo: Tipo de Solicitação Recebida."),
    ("MARCAS",
     "MARCA",
     "Filtro de seleção múltipla",
     "Filtra por rede/marca de ensino. Permite análise por grupo.",
     "GLOBAL TREE, APOGEU, MATRIZ EDUCAÇÃO, CLV, QI, RAIZ EDUCACAO, "
     "CUBO GLOBAL SCHOOL, AMERICANO, UNIFICADO, SAP, SARAH DAWSEY, "
     "SÁ PEREIRA, UNIÃO, BOM TEMPO",
     "Slicer MARCA (Power BI)",
     "Campo idêntico nos dois dashboards."),
    ("DATA DE FE... (Data de Fechamento)",
     "DATA DE FECHAMENTO DA VAGA",
     "Filtro de período (intervalo de datas)",
     "Filtra pelos registros dentro do período de fechamento da vaga.",
     "Intervalo de datas (DD/MM/AAAA)",
     "Slicer dCalendario + campo DATA DE FECHAMENTO (Power BI)",
     "Label truncado no Looker. Nome completo: Data de Fechamento da Vaga."),
    ("DATA DE INI... (Data de Início)",
     "DATA DE INICIO PREVISTA",
     "Filtro de período (intervalo de datas)",
     "Filtra pelos registros dentro do período de início previsto do colaborador.",
     "Intervalo de datas (DD/MM/AAAA)",
     "Slicer dCalendario + campo DATA DE INICIO PREVISTA (Power BI)",
     "Label truncado no Looker. Nome completo: Data de Início Prevista."),
]

for i, f in enumerate(filtros_ls):
    fill = COR_ALT2 if i % 2 == 0 else COR_BRANCO
    write_data_row(ws_ls, row_ls, f, fill)
    ws_ls.row_dimensions[row_ls].height = 50
    row_ls += 1

row_ls += 1

# Seção: KPIs
ws_ls.merge_cells(f"A{row_ls}:G{row_ls}")
sk = ws_ls.cell(row=row_ls, column=1, value="KPIs (CARDS) – Aba: Recrutamento & Seleção")
sk.fill = header_fill("BF360C")
sk.font = Font(name="Calibri", bold=True, size=12, color="FFFFFF")
sk.alignment = Alignment(horizontal="center", vertical="center")
ws_ls.row_dimensions[row_ls].height = 22
row_ls += 1

write_header_row(ws_ls, row_ls, headers_filtros, "D84315")
ws_ls.row_dimensions[row_ls].height = 20
row_ls += 1

kpis_ls = [
    ("TOTAL DE TICKETS",
     "TICKET (COUNT)",
     "Número inteiro – Contagem",
     "Total de tickets (solicitações de vaga) cadastrados, independente do status. "
     "Reflete todo o volume de demanda do período.",
     "3.562 (valor exibido)",
     "Medida Contagem de TICKET (Power BI)",
     "Engloba tickets de todos os status e anos visíveis no filtro atual."),
    ("TOTAL DE VAGAS FECHADAS",
     "STATUS = Fechada (COUNT)",
     "Número inteiro – Contagem",
     "Total de vagas com processo seletivo encerrado (status Fechada), "
     "independente do ano.",
     "2.761 (valor exibido: soma 2025+2026)",
     "Medida VagasFechadas (Power BI)",
     "Soma de vagas fechadas em todos os períodos. É a soma de 2.120 + 641."),
    ("VAGAS FECHADAS – 2025",
     "STATUS = Fechada AND Ano = 2025",
     "Número inteiro – Contagem com filtro de ano",
     "Total de vagas fechadas especificamente no ano de 2025.",
     "2.120 (valor exibido)",
     "Medida VagasFechadas com filtro ano 2025 (Power BI)",
     "Calculado com filtro implícito de ano = 2025."),
    ("VAGAS FECHADAS – 2026",
     "STATUS = Fechada AND Ano = 2026",
     "Número inteiro – Contagem com filtro de ano",
     "Total de vagas fechadas especificamente no ano de 2026 (acumulado YTD).",
     "641 (valor exibido, acumulado até abril/2026)",
     "Medida VagasFechadas com filtro ano 2026 (Power BI)",
     "Valor YTD (Year-To-Date). Aumenta conforme o ano avança."),
]

for i, k in enumerate(kpis_ls):
    fill = COR_ALT2 if i % 2 == 0 else COR_BRANCO
    write_data_row(ws_ls, row_ls, k, fill, bold_first=True)
    ws_ls.row_dimensions[row_ls].height = 55
    row_ls += 1

row_ls += 1

# Seção: Gráficos
ws_ls.merge_cells(f"A{row_ls}:G{row_ls}")
sg = ws_ls.cell(row=row_ls, column=1, value="GRÁFICOS / VISUAIS – Aba: Recrutamento & Seleção")
sg.fill = header_fill("BF360C")
sg.font = Font(name="Calibri", bold=True, size=12, color="FFFFFF")
sg.alignment = Alignment(horizontal="center", vertical="center")
ws_ls.row_dimensions[row_ls].height = 22
row_ls += 1

headers_graf = ["Título do Visual", "Tipo de Gráfico",
                "Dimensão (Eixo X / Categoria)", "Métrica (Eixo Y / Valor)",
                "Legenda / Séries", "Equivalente Power BI", "Observações"]
write_header_row(ws_ls, row_ls, headers_graf, "D84315")
ws_ls.row_dimensions[row_ls].height = 20
row_ls += 1

graficos_ls = [
    ("Volume de contratação",
     "Gráfico de colunas agrupadas",
     "MARCA (rede de ensino)",
     "COUNT(TICKET) onde STATUS = Fechada",
     "Ano (2025 = azul, 2026 = laranja)",
     "Sem equivalente direto na aba Geral do PBI (agrupa por marca). "
     "Similar ao 'Ticket por Unidade' parcialmente.",
     "Exibe comparativo de vagas fechadas por marca entre 2025 e 2026. "
     "Marcas: GLOBAL TREE, APOGEU, MATRIZ EDUCAÇÃO, CLV, QI, RAIZ EDUCACAO, "
     "CUBO GLOBAL SCHOOL, AMERICANO, UNIFICADO, SAP, SARAH DAWSEY, "
     "SÁ PEREIRA, UNIÃO, BOM TEMPO."),
    ("Tickets por tipo de solicitação",
     "Gráfico de barras horizontais agrupadas",
     "TIPO DE SOLICITAÇÃO RECEBIDA",
     "COUNT(TICKET)",
     "Ano (2025 = azul, 2026 = laranja)",
     "Não há visual equivalente direto no PBI (dado está na tabela de consulta)",
     "Valores 2025: SUBSTITUIÇÃO=1.851, AUMENTO DE QUADRO=978, PEJOTIZAÇÃO=4. "
     "Valores 2026: SUBSTITUIÇÃO=510, AUMENTO DE QUADRO=155, Outros=1."),
    ("Tickets por nível",
     "Gráfico de barras horizontais agrupadas",
     "NÍVEL",
     "COUNT(TICKET)",
     "Ano (2025 = azul, 2026 = laranja)",
     "Parcialmente equivalente ao 'Ticket por Cargo' na aba Performance do PBI",
     "Níveis: OPERACIONAL (933/179), ESTÁGIO (866/228), PEDAGÓGICO (769/272), "
     "ESTRATÉGICO (130/22), TÁTICO (86/12), JOVEM APRENDIZ (51/6+8)."),
    ("Vagas de R&S fechadas por recrutador",
     "Gráfico de colunas agrupadas",
     "CONSULTOR DE R&S",
     "COUNT(TICKET) onde STATUS = Fechada",
     "Ano (2025 = azul, 2026 = laranja)",
     "Tabela de ranking de recrutadores na aba Performance do Power BI",
     "Recrutadores: RAYSSA (214/73), VIVIAN (191/72), LANNA (183/18), "
     "LUCAS FRAZAO (107/21), VITOR (51/-), MAYARA (8/-), "
     "CONSULTORIA DE RH (7/-), PABLO (3/-), AMANDA (2/-), "
     "ISABELA (1/-), BEATRIZ MARCOTULLIO (1/-), NATHANY (-/0)."),
]

for i, g in enumerate(graficos_ls):
    fill = COR_ALT2 if i % 2 == 0 else COR_BRANCO
    write_data_row(ws_ls, row_ls, g, fill, bold_first=True)
    ws_ls.row_dimensions[row_ls].height = 65
    row_ls += 1

set_col_widths(ws_ls, {
    "A": 32, "B": 28, "C": 30, "D": 30, "E": 28, "F": 38, "G": 52
})

# ─────────────────────────── ABA 4: De-Para ───────────────────────────────────
ws_dp = wb.create_sheet("De-Para")
ws_dp.sheet_view.showGridLines = False

ws_dp.merge_cells("A1:I1")
t3 = ws_dp["A1"]
t3.value = "MAPEAMENTO DE-PARA  │  Power BI  ↔  Looker Studio"
t3.fill = header_fill(COR_DEPARA_HEADER)
t3.font = Font(name="Calibri", bold=True, size=14, color="FFFFFF")
t3.alignment = Alignment(horizontal="center", vertical="center")
ws_dp.row_dimensions[1].height = 28

ws_dp.merge_cells("A2:I2")
ts2 = ws_dp["A2"]
ts2.value = ("Legenda de status:  ✅ Mapeado (mesmo campo)   "
             "⚠️ Parcial (nome diferente / nível diferente)   "
             "❌ Sem equivalente   ➕ Exclusivo de um lado")
ts2.fill = header_fill("4CAF50")
ts2.font = Font(name="Calibri", bold=True, size=11, color="FFFFFF")
ts2.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
ws_dp.row_dimensions[2].height = 28

row_dp = 3
headers_dp = [
    "Categoria",
    "Campo / Métrica no Power BI",
    "Tabela PBI",
    "Campo / Métrica no Looker Studio",
    "Status",
    "Diferenças / Observações",
    "Impacto na Migração",
    "Prioridade",
    "Ação Recomendada"
]
write_header_row(ws_dp, row_dp, headers_dp, COR_DEPARA_HEADER)
ws_dp.row_dimensions[row_dp].height = 20
row_dp += 1

depara = [
    # FILTROS
    ("Filtro",
     "Slicer: MARCA",
     "Fonte_Sheets",
     "Filtro: MARCAS",
     "✅ Mapeado",
     "Mesmo campo (MARCA), nomes de valor idênticos em ambos.",
     "Nenhum",
     "Alta",
     "Manter nomenclatura MARCA. Verificar se todos os 14 valores estão presentes nos dois sistemas."),
    ("Filtro",
     "Slicer: STATUS",
     "Fonte_Sheets",
     "Filtro: STATUS",
     "✅ Mapeado",
     "Mesmo campo. Verificar se os domínios de valores são idênticos.",
     "Verificar domínio",
     "Alta",
     "Mapear todos os valores possíveis de STATUS em ambas as fontes e confirmar equivalência."),
    ("Filtro",
     "Slicer: TIPO DE SOLICITAÇÃO RECEBIDA",
     "Fonte_Sheets",
     "Filtro: TIPO DE SO...",
     "✅ Mapeado",
     "Mesmo campo. Label truncado no Looker ('TIPO DE SO...').",
     "Renomear label no Looker",
     "Média",
     "Expandir label no Looker Studio para o nome completo para melhor UX."),
    ("Filtro",
     "Slicer: dCalendario → DATA DE FECHAMENTO DA VAGA",
     "Fonte_Sheets / dCalendario",
     "Filtro: DATA DE FE...",
     "✅ Mapeado",
     "Mesmo campo. Label truncado no Looker.",
     "Renomear label no Looker",
     "Baixa",
     "Expandir label no Looker Studio."),
    ("Filtro",
     "Slicer: dCalendario → DATA DE INICIO PREVISTA",
     "Fonte_Sheets / dCalendario",
     "Filtro: DATA DE INI...",
     "✅ Mapeado",
     "Mesmo campo. Label truncado no Looker.",
     "Renomear label no Looker",
     "Baixa",
     "Expandir label no Looker Studio."),
    # KPIs
    ("KPI",
     "Contagem de TICKET (Total de Tickets)",
     "Fonte_Sheets",
     "TOTAL DE TICKETS = 3.562",
     "✅ Mapeado",
     "Mesmo cálculo: COUNT de registros da tabela de tickets. "
     "Ambos exibem o mesmo valor total.",
     "Nenhum",
     "Alta",
     "Confirmar que os filtros de período aplicados retornam o mesmo universo de registros."),
    ("KPI",
     "VagasFechadas (Total de Vagas Fechadas)",
     "R&S_CONTROLE DE VAGAS 2026",
     "TOTAL DE VAGAS FECHADAS = 2.761",
     "✅ Mapeado",
     "Mesma lógica: COUNT de tickets com STATUS = Fechada. "
     "Valores coincidem (2.761).",
     "Nenhum",
     "Alta",
     "Garantir que o critério de STATUS = Fechada seja idêntico nas duas ferramentas."),
    ("KPI",
     "VagasFechadas [filtro ano=2025]",
     "R&S_CONTROLE DE VAGAS 2026",
     "VAGAS FECHADAS – 2025 = 2.120",
     "✅ Mapeado",
     "Mesmo cálculo com filtro de ano. Valores coincidem.",
     "Nenhum",
     "Alta",
     "Validar que a dimensão de data utilizada é a mesma nos dois sistemas."),
    ("KPI",
     "VagasFechadas [filtro ano=2026]",
     "R&S_CONTROLE DE VAGAS 2026",
     "VAGAS FECHADAS – 2026 = 641",
     "✅ Mapeado",
     "Mesmo cálculo com filtro de ano 2026. Valores coincidem.",
     "Nenhum",
     "Alta",
     "Monitorar atualização incremental."),
    ("KPI",
     "SLA_R&S_Médio",
     "R&S_CONTROLE DE VAGAS 2026",
     "❌ Não existe no Looker Studio",
     "❌ Sem equivalente",
     "SLA R&S é exclusivo do Power BI. Looker não exibe este indicador.",
     "Criar no Looker ou documentar como gap",
     "Alta",
     "Criar campo calculado no Looker Studio: DATEDIFF(data_abertura, data_fechamento, DAY). "
     "Exibir como scorecard na aba R&S."),
    ("KPI",
     "SLA_ADM_Médio",
     "R&S_CONTROLE DE VAGAS 2026",
     "❌ Não existe no Looker Studio",
     "❌ Sem equivalente",
     "SLA ADM é exclusivo do Power BI. Looker não exibe este indicador.",
     "Criar no Looker ou documentar como gap",
     "Alta",
     "Criar campo calculado: DATEDIFF(data_fechamento, data_inicio_prevista, DAY). "
     "Exibir como scorecard."),
    ("KPI",
     "VagasFechadasAdmissão",
     "R&S_CONTROLE DE VAGAS 2026",
     "❌ Não existe no Looker Studio",
     "❌ Sem equivalente",
     "Vagas fechadas com admissão é exclusivo do PBI.",
     "Criar no Looker ou documentar",
     "Média",
     "Avaliar se é necessário no Looker. Criar campo calculado se confirmado."),
    ("KPI",
     "VagasFechadas MTD",
     "R&S_CONTROLE DE VAGAS 2026",
     "❌ Não existe no Looker Studio",
     "❌ Sem equivalente",
     "Indicador de mês atual exclusivo do Power BI (aba Performance).",
     "Criar no Looker",
     "Média",
     "Usar filtro de período relativo no Looker (mês atual) para replicar."),
    ("KPI",
     "VagasFechadas WTD",
     "R&S_CONTROLE DE VAGAS 2026",
     "❌ Não existe no Looker Studio",
     "❌ Sem equivalente",
     "Indicador de semana atual exclusivo do Power BI (aba Performance).",
     "Criar no Looker",
     "Média",
     "Usar filtro de período relativo (semana atual) no Looker para replicar."),
    # GRÁFICOS
    ("Gráfico",
     "Movimentações Ticket (colunas por período)",
     "Fonte_Sheets + dCalendario",
     "❌ Não mapeado na aba R&S do Looker",
     "⚠️ Parcial",
     "Power BI tem gráfico de volume ao longo do tempo. "
     "Looker mostra comparativo por dimensão estática.",
     "Criar visual de série temporal no Looker",
     "Alta",
     "Adicionar gráfico de linhas/colunas por mês no Looker Studio, "
     "com comparativo 2025 vs 2026."),
    ("Gráfico",
     "Ticket por Status (barras horizontais)",
     "Fonte_Sheets",
     "❌ Não mapeado explicitamente",
     "⚠️ Parcial",
     "Power BI tem gráfico dedicado. Looker usa STATUS como filtro, "
     "sem gráfico de distribuição.",
     "Criar visual no Looker",
     "Média",
     "Adicionar gráfico de pizza ou barras de STATUS no Looker Studio."),
    ("Gráfico",
     "Ticket por Unidade / Setor (barras horizontais)",
     "Fonte_Sheets",
     "Volume de contratação por MARCA",
     "⚠️ Parcial",
     "Power BI usa UNIDADE/SETOR (nível mais granular). "
     "Looker usa MARCA (nível agregado).",
     "Definir granularidade desejada",
     "Alta",
     "Decidir se Looker deve exibir por UNIDADE (mais granular) ou manter MARCA. "
     "Adicionar drill-down se necessário."),
    ("Gráfico",
     "Ticket por Segmento de Atuação",
     "Fonte_Sheets",
     "❌ Não existe no Looker Studio",
     "❌ Sem equivalente",
     "Segmento de Atuação é dimensão exclusiva do Power BI.",
     "Criar no Looker ou documentar como gap",
     "Baixa",
     "Avaliar relevância. Se necessário, adicionar campo SEGMENTO ao dataset do Looker."),
    ("Gráfico",
     "Ticket por Diretoria",
     "Fonte_Sheets",
     "❌ Não existe no Looker Studio",
     "❌ Sem equivalente",
     "DIRETORIA é dimensão exclusiva do Power BI (aba Performance).",
     "Criar no Looker ou documentar",
     "Média",
     "Adicionar campo DIRETORIA ao dataset do Looker se disponível na fonte."),
    ("Gráfico",
     "Ticket por Cargo",
     "Fonte_Sheets",
     "Tickets por nível (aproximado)",
     "⚠️ Parcial",
     "Power BI usa CARGO (nome do cargo). Looker usa NÍVEL (categoria hierárquica). "
     "São granularidades diferentes.",
     "Alinhar nível de detalhe",
     "Alta",
     "Definir se análise deve ser por CARGO ou por NÍVEL. "
     "Ambos existem na fonte – escolher o correto para cada ferramenta."),
    ("Gráfico",
     "❌ Não existe no Power BI (aba R&S)",
     "—",
     "Tickets por tipo de solicitação",
     "➕ Exclusivo do Looker",
     "Gráfico de Tipo de Solicitação existe no Looker mas não como "
     "visual dedicado na aba Geral do PBI (disponível em tabela).",
     "Adicionar ao Power BI se necessário",
     "Média",
     "Avaliar se é necessário criar visual equivalente na aba Geral/Performance do Power BI."),
    ("Tabela",
     "Tabela de Ranking de Recrutadores (aba Performance)",
     "R&S_CONTROLE DE VAGAS 2026 + Fonte_Sheets",
     "Vagas de R&S fechadas por recrutador (gráfico de colunas)",
     "⚠️ Parcial",
     "PBI usa tabela com Rank, WTD, MTD, Total, % acumulado, SLA R&S, SLA ADM. "
     "Looker usa gráfico simples de barras por recrutador.",
     "Enriquecer o Looker com mais métricas",
     "Alta",
     "Criar tabela detalhada no Looker Studio com: recrutador, vagas MTD, "
     "vagas total, SLA médio. Ou manter gráfico e adicionar tooltip."),
    ("Tabela",
     "Tabela de Consulta (aba Consulta)",
     "Fonte_Sheets",
     "❌ Não existe no Looker Studio",
     "❌ Sem equivalente",
     "Aba de consulta individual de tickets é exclusiva do Power BI.",
     "Criar aba de consulta no Looker",
     "Alta",
     "Criar página 'Consulta' no Looker Studio com tabela filtrável por "
     "MARCA, ANO e NOME, exibindo STATUS, TICKET, NÍVEL, CARGO, CONSULTOR, "
     "GESTOR, DATAS e REMUNERAÇÃO."),
    ("Tabela",
     "Tabela Extração de Bases (aba Extração)",
     "Fonte_Sheets",
     "❌ Não existe no Looker Studio",
     "❌ Sem equivalente",
     "Aba de extração para exportação CSV/Excel exclusiva do Power BI.",
     "Avaliar necessidade",
     "Média",
     "Looker Studio permite exportar dados de tabelas. Criar página equivalente "
     "se necessário ou orientar usuários a usar a exportação nativa."),
    # DIMENSÕES SEM EQUIVALENTE
    ("Dimensão",
     "NÍVEL",
     "Fonte_Sheets",
     "Dimensão: Tickets por nível",
     "✅ Mapeado",
     "Campo NÍVEL existe em ambos com os mesmos valores.",
     "Nenhum",
     "Alta",
     "Garantir que os valores de NÍVEL estão padronizados na fonte de dados."),
    ("Dimensão",
     "CONSULTOR DE R&S",
     "Fonte_Sheets",
     "CONSULTOR DE R&S (gráfico por recrutador)",
     "✅ Mapeado",
     "Mesmo campo. Valores de nomes podem variar por digitação.",
     "Padronizar nomes",
     "Alta",
     "Criar tabela de-para de nomes de recrutadores para garantir consistência."),
    ("Dimensão",
     "TIPO DE SOLICITAÇÃO RECEBIDA",
     "Fonte_Sheets",
     "TIPO DE SOLICITAÇÃO RECEBIDA",
     "✅ Mapeado",
     "Campo idêntico. Valores: SUBSTITUIÇÃO, AUMENTO DE QUADRO, PEJOTIZAÇÃO.",
     "Nenhum",
     "Alta",
     "Verificar se existe categoria 'Outros' e como é tratada em cada sistema."),
    ("Dimensão",
     "REMUNERAÇÃO",
     "Fonte_Sheets",
     "❌ Não visível no Looker Studio",
     "❌ Sem equivalente visual",
     "Campo disponível no PBI (aba Consulta) mas não exibido no Looker.",
     "Avaliar se deve ser exposto",
     "Baixa",
     "Verificar restrições de acesso/confidencialidade antes de expor no Looker."),
    ("Dimensão",
     "GESTOR DA VAGA",
     "Fonte_Sheets",
     "❌ Não visível no Looker Studio",
     "❌ Sem equivalente visual",
     "Campo disponível no PBI mas não exibido no Looker.",
     "Adicionar ao Looker se necessário",
     "Baixa",
     "Incluir na página Consulta do Looker, se criada."),
]

for i, d in enumerate(depara):
    if d[4] == "✅ Mapeado":
        fill = COR_ALT3
    elif d[4] in ("⚠️ Parcial", "➕ Exclusivo do Looker"):
        fill = COR_ALT2
    else:
        fill = "FCE4EC"  # vermelho claro
    # Alterna entre a cor temática e branco
    if i % 2 != 0:
        fill = COR_BRANCO
    write_data_row(ws_dp, row_dp, d, fill)
    ws_dp.row_dimensions[row_dp].height = 55
    row_dp += 1

set_col_widths(ws_dp, {
    "A": 14, "B": 38, "C": 28, "D": 38, "E": 16,
    "F": 55, "G": 35, "H": 14, "I": 55
})

# ────────────── ABA 5: Visuais Comparados ─────────────────────────────────────
ws_vc = wb.create_sheet("Visuais Comparados")
ws_vc.sheet_view.showGridLines = False

ws_vc.merge_cells("A1:G1")
t4 = ws_vc["A1"]
t4.value = "COMPARATIVO DE VISUAIS  │  Power BI vs. Looker Studio"
t4.fill = header_fill("37474F")
t4.font = Font(name="Calibri", bold=True, size=14, color="FFFFFF")
t4.alignment = Alignment(horizontal="center", vertical="center")
ws_vc.row_dimensions[1].height = 28

headers_vc = [
    "Visual no Power BI", "Aba (PBI)", "Tipo (PBI)",
    "Visual equivalente no Looker Studio", "Aba (Looker)", "Tipo (Looker)",
    "Status de Equivalência"
]
write_header_row(ws_vc, 2, headers_vc, "546E7A")
ws_vc.row_dimensions[2].height = 20

visuais = [
    # Página Capa
    ("Capa animada / Iniciar",
     "Capa",
     "Imagem + Botão de navegação",
     "❌ Não existe",
     "—",
     "—",
     "❌ Sem equivalente"),
    # Página Geral
    ("Filtro: Slicer de Data (Ano/Mês/Dia)",
     "Geral",
     "Slicer hierárquico (PBI nativo)",
     "Filtros: DATA DE FE... / DATA DE INI...",
     "R&S",
     "Filtro de controle de período",
     "⚠️ Parcial – Looker usa 2 filtros separados"),
    ("Filtro: Slicer de MARCA",
     "Geral",
     "Slicer de lista",
     "Filtro: MARCAS",
     "R&S",
     "Filtro de controle de seleção múltipla",
     "✅ Equivalente"),
    ("Movimentações Ticket (colunas por tempo)",
     "Geral",
     "Gráfico de colunas com hierarquia temporal",
     "❌ Não mapeado na aba R&S",
     "—",
     "—",
     "❌ Sem equivalente na aba R&S"),
    ("Ticket por Status",
     "Geral",
     "Gráfico de barras horizontais agrupadas",
     "Filtro STATUS (não há gráfico dedicado)",
     "R&S",
     "Filtro de lista",
     "⚠️ Parcial – STATUS existe mas sem visual dedicado"),
    ("Ticket por Unidade / Setor",
     "Geral",
     "Gráfico de barras horizontais",
     "Volume de contratação (por MARCA)",
     "R&S",
     "Gráfico de colunas agrupadas",
     "⚠️ Parcial – PBI: nível UNIDADE; Looker: nível MARCA"),
    ("Ticket por Segmento de Atuação",
     "Geral",
     "Gráfico de barras horizontais",
     "❌ Não existe",
     "—",
     "—",
     "❌ Sem equivalente"),
    ("Card: Fechadas R&S + %",
     "Geral",
     "Card visual duplo",
     "TOTAL DE VAGAS FECHADAS + VAGAS FECHADAS 2026",
     "R&S",
     "Cards de scorecard",
     "⚠️ Parcial – Looker separa por ano; PBI consolida"),
    ("Card: Fechadas Admissão + %",
     "Geral",
     "Card visual duplo",
     "❌ Não existe",
     "—",
     "—",
     "❌ Sem equivalente"),
    ("Card: SLA R&S Médio",
     "Geral",
     "Card visual",
     "❌ Não existe",
     "—",
     "—",
     "❌ Sem equivalente"),
    ("Card: SLA ADM Médio",
     "Geral",
     "Card visual",
     "❌ Não existe",
     "—",
     "—",
     "❌ Sem equivalente"),
    # Página Performance
    ("Card: Vagas Fechadas MTD",
     "Performance",
     "Card visual",
     "❌ Não existe",
     "—",
     "—",
     "❌ Sem equivalente"),
    ("Card: Vagas Fechadas WTD",
     "Performance",
     "Card visual",
     "❌ Não existe",
     "—",
     "—",
     "❌ Sem equivalente"),
    ("Card: Cadastro Gupy",
     "Performance",
     "Card visual",
     "❌ Não existe",
     "—",
     "—",
     "❌ Sem equivalente"),
    ("Card: Entrevista Liderança",
     "Performance",
     "Card visual",
     "❌ Não existe",
     "—",
     "—",
     "❌ Sem equivalente"),
    ("Ticket por Diretoria",
     "Performance",
     "Gráfico de barras horizontais",
     "❌ Não existe",
     "—",
     "—",
     "❌ Sem equivalente"),
    ("Ticket por Cargo",
     "Performance",
     "Gráfico de barras horizontais",
     "Tickets por nível",
     "R&S",
     "Gráfico de barras horizontais agrupadas",
     "⚠️ Parcial – CARGO vs NÍVEL (granularidades diferentes)"),
    ("Tabela de Ranking de Recrutadores",
     "Performance",
     "Tabela com múltiplas métricas",
     "Vagas de R&S fechadas por recrutador",
     "R&S",
     "Gráfico de colunas agrupadas",
     "⚠️ Parcial – PBI tem tabela rica; Looker só tem gráfico"),
    # Página Consulta
    ("Tabela de Consulta de Tickets",
     "Consulta",
     "Tabela interativa com 12 colunas",
     "❌ Não existe",
     "—",
     "—",
     "❌ Sem equivalente"),
    # Página Extração
    ("Tabela de Extração de Bases",
     "Extração de Bases",
     "Tabela exportável com 6 colunas",
     "❌ Não existe (exportação via gráficos)",
     "—",
     "Exportação nativa do Looker",
     "⚠️ Parcial – Looker permite export mas sem página dedicada"),
    # Exclusivo Looker
    ("❌ Não existe no PBI",
     "—",
     "—",
     "Tickets por tipo de solicitação",
     "R&S",
     "Gráfico de barras horizontais agrupadas",
     "➕ Exclusivo do Looker Studio"),
    ("❌ Não existe na aba R&S do PBI",
     "—",
     "—",
     "TOTAL DE TICKETS (card)",
     "R&S",
     "Scorecard",
     "✅ Equivalente ao Contagem de TICKET no PBI"),
    ("❌ Não existe na aba R&S do PBI",
     "—",
     "—",
     "VAGAS FECHADAS 2025 (card separado)",
     "R&S",
     "Scorecard",
     "⚠️ Parcial – PBI consolida num único card com filtro"),
]

row_vc = 3
for i, v in enumerate(visuais):
    status = v[6]
    if "✅" in status:
        fill = COR_ALT3
    elif "⚠️" in status or "➕" in status:
        fill = COR_ALT2
    else:
        fill = "FCE4EC"
    if i % 2 != 0:
        fill = COR_BRANCO
    write_data_row(ws_vc, row_vc, v, fill)
    ws_vc.row_dimensions[row_vc].height = 45
    row_vc += 1

set_col_widths(ws_vc, {
    "A": 38, "B": 18, "C": 32, "D": 38, "E": 18, "F": 32, "G": 22
})

# ══════════════════════════════════════════════════════════════════════════════
wb.save(OUTPUT)
print(f"Arquivo salvo em:\n{OUTPUT}")
