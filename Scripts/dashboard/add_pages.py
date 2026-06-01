"""
Adiciona duas novas páginas ao Dashboard Métricas P&C.pbix:
  - Qualidade & SLA
  - Visão Estratégica

INSTRUÇÕES:
  1. No Power BI Desktop, salve o arquivo (Ctrl+S)
  2. Feche o Power BI Desktop
  3. Execute este script: python add_pages.py
  4. Reabra o .pbix
"""

import zipfile, json, uuid, io, os, shutil
from copy import deepcopy

PBIX = "Dashboard Métricas P&C.pbix"
BACKUP = "Dashboard Métricas P&C.pbix.bak"
TABLE_RS   = "R&S_CONTROLE DE VAGAS 2026"
TABLE_FS   = "Fonte_Sheets"
TABLE_CAL  = "dCalendario"
ALIAS_RS   = "r"
ALIAS_FS   = "f"
ALIAS_CAL  = "d"
COLOR_TEAL = "#7AC5BF"
COLOR_CORAL= "#E8856A"
COLOR_BLUE = "#4472C4"

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def nid():
    return uuid.uuid4().hex[:20]

def pos(x, y, z, w, h):
    return {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z}

def layouts(x, y, z, w, h, phone_y=0, phone_w=324, phone_h=180):
    return [
        {"id": 0, "position": pos(x, y, z, w, h)},
        {"id": 1, "position": pos(0, phone_y, z, phone_w, phone_h)},
    ]

def m_select(alias, table, prop):
    """Measure select entry"""
    return {
        "Measure": {"Expression": {"SourceRef": {"Source": alias}}, "Property": prop},
        "Name": f"{table}.{prop}",
        "NativeReferenceName": prop,
    }

def c_select(alias, table, prop):
    """Column select entry"""
    return {
        "Column": {"Expression": {"SourceRef": {"Source": alias}}, "Property": prop},
        "Name": f"{table}.{prop}",
        "NativeReferenceName": prop,
    }

def cal_level_select(alias, table, level):
    """Calendar hierarchy level select"""
    return {
        "HierarchyLevel": {
            "Expression": {
                "Hierarchy": {
                    "Expression": {
                        "PropertyVariationSource": {
                            "Expression": {"SourceRef": {"Source": alias}},
                            "Name": "Variation",
                            "Property": "Date",
                        }
                    },
                    "Hierarchy": "Hierarquia de datas",
                }
            },
            "Level": level,
        },
        "Name": f"{table}.Date.Variation.Hierarquia de datas.{level}",
        "NativeReferenceName": f"Date {level}",
    }

def vc(cfg, x, y, z, w, h):
    """Wrap config dict into a visualContainer"""
    import random
    return {
        "id": random.randint(10_000_000_000, 99_999_999_999),
        "x": x, "y": y, "z": z,
        "width": w, "height": h,
        "tabOrder": z,
        "config": json.dumps(cfg, ensure_ascii=False),
        "filters": "[]",
    }

# ─────────────────────────────────────────────
# VISUAL BUILDERS
# ─────────────────────────────────────────────
def card(x, y, z, w, h, measures, col_props=None):
    """
    measures: list of (alias, table, prop)
    col_props: dict {full_name: formatString}
    """
    from_map = {}
    selects, projs = [], []
    for alias, table, prop in measures:
        if alias not in from_map:
            from_map[alias] = table
        selects.append(m_select(alias, table, prop))
        projs.append({"queryRef": f"{table}.{prop}"})

    from_list = [{"Name": k, "Entity": v, "Type": 0} for k, v in from_map.items()]

    sv = {
        "visualType": "cardVisual",
        "projections": {"Data": projs},
        "prototypeQuery": {"Version": 2, "From": from_list, "Select": selects},
        "drillFilterOtherVisuals": True,
        "hasDefaultSort": True,
    }
    if col_props:
        sv["columnProperties"] = {k: {"formatString": v} for k, v in col_props.items()}

    cfg = {"name": nid(), "layouts": layouts(x, y, z, w, h), "singleVisual": sv}
    return vc(cfg, x, y, z, w, h)


def slicer(x, y, z, w, h, alias, table, prop, label, mode="Dropdown"):
    selects = [c_select(alias, table, prop)]
    from_list = [{"Name": alias, "Entity": table, "Type": 0}]

    sv = {
        "visualType": "slicer",
        "projections": {"Values": [{"queryRef": f"{table}.{prop}", "active": True}]},
        "prototypeQuery": {"Version": 2, "From": from_list, "Select": selects},
        "drillFilterOtherVisuals": True,
        "objects": {
            "data": [{"properties": {"mode": {"expr": {"Literal": {"Value": f"'{mode}'"}}}}}],
            "header": [{"properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "text": {"expr": {"Literal": {"Value": f"'{label}'"}}},
            }}],
        },
        "vcObjects": {"background": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]},
    }
    cfg = {"name": nid(), "layouts": layouts(x, y, z, w, h), "singleVisual": sv}
    return vc(cfg, x, y, z, w, h)


def bar_chart(x, y, z, w, h, cat_alias, cat_table, cat_prop,
              measure_alias, measure_table, measure_prop,
              title="", color=COLOR_TEAL, horizontal=True):
    """Single-measure bar/column chart"""
    chart_type = "clusteredBarChart" if horizontal else "columnChart"

    from_list = [
        {"Name": cat_alias, "Entity": cat_table, "Type": 0},
        {"Name": measure_alias, "Entity": measure_table, "Type": 0},
    ]
    if cat_alias == measure_alias:
        from_list = [{"Name": cat_alias, "Entity": cat_table, "Type": 0}]

    cat_sel = c_select(cat_alias, cat_table, cat_prop)
    m_sel   = m_select(measure_alias, measure_table, measure_prop)

    sv = {
        "visualType": chart_type,
        "projections": {
            "Category": [{"queryRef": f"{cat_table}.{cat_prop}", "active": True}],
            "Y":        [{"queryRef": f"{measure_table}.{measure_prop}"}],
        },
        "prototypeQuery": {
            "Version": 2,
            "From": from_list,
            "Select": [cat_sel, m_sel],
            "OrderBy": [{"Direction": 2, "Expression": {
                "Measure": {"Expression": {"SourceRef": {"Source": measure_alias}},
                            "Property": measure_prop}
            }}],
        },
        "drillFilterOtherVisuals": True,
        "hasDefaultSort": True,
        "objects": {
            "dataPoint": [{"properties": {"fill": {"solid": {"color": {
                "expr": {"Literal": {"Value": f"'{color}'"}}
            }}}}}],
            "valueAxis": [{"properties": {
                "showAxisTitle": {"expr": {"Literal": {"Value": "false"}}}
            }}],
            "categoryAxis": [{"properties": {
                "showAxisTitle": {"expr": {"Literal": {"Value": "false"}}}
            }}],
        },
    }
    if title:
        sv["vcObjects"] = {"title": [{"properties": {
            "text": {"expr": {"Literal": {"Value": f"'{title}'"}}},
            "alignment": {"expr": {"Literal": {"Value": "'center'"}}},
        }}]}

    cfg = {"name": nid(), "layouts": layouts(x, y, z, w, h), "singleVisual": sv}
    return vc(cfg, x, y, z, w, h)


def combo_chart(x, y, z, w, h,
                col_alias, col_table, col_prop,
                line_alias, line_table, line_prop,
                cal_alias=ALIAS_CAL, cal_table=TABLE_CAL,
                title=""):
    """Line + Column combo chart with date hierarchy on X axis"""
    from_list = [
        {"Name": cal_alias, "Entity": cal_table, "Type": 0},
        {"Name": col_alias, "Entity": col_table, "Type": 0},
    ]
    if col_alias != line_alias:
        from_list.append({"Name": line_alias, "Entity": line_table, "Type": 0})

    year_sel  = cal_level_select(cal_alias, cal_table, "Ano")
    month_sel = cal_level_select(cal_alias, cal_table, "Mês")
    col_sel   = m_select(col_alias,  col_table,  col_prop)
    line_sel  = m_select(line_alias, line_table, line_prop)

    sv = {
        "visualType": "lineClusteredColumnComboChart",
        "projections": {
            "Category": [
                {"queryRef": f"{cal_table}.Date.Variation.Hierarquia de datas.Ano"},
                {"queryRef": f"{cal_table}.Date.Variation.Hierarquia de datas.Mês", "active": True},
            ],
            "Y":  [{"queryRef": f"{col_table}.{col_prop}"}],
            "Y2": [{"queryRef": f"{line_table}.{line_prop}"}],
        },
        "prototypeQuery": {
            "Version": 2,
            "From": from_list,
            "Select": [year_sel, month_sel, col_sel, line_sel],
        },
        "drillFilterOtherVisuals": True,
        "hasDefaultSort": False,
        "objects": {
            "dataPoint": [{"properties": {"fill": {"solid": {"color": {
                "expr": {"Literal": {"Value": f"'{COLOR_TEAL}'"}}
            }}}}}],
            "valueAxis": [{"properties": {
                "showAxisTitle": {"expr": {"Literal": {"Value": "false"}}}
            }}],
        },
    }
    if title:
        sv["vcObjects"] = {"title": [{"properties": {
            "text": {"expr": {"Literal": {"Value": f"'{title}'"}}},
            "alignment": {"expr": {"Literal": {"Value": "'center'"}}},
        }}]}

    cfg = {"name": nid(), "layouts": layouts(x, y, z, w, h), "singleVisual": sv}
    return vc(cfg, x, y, z, w, h)


def combo_chart_2lines(x, y, z, w, h,
                       col_alias, col_table, col_prop,
                       line1_alias, line1_table, line1_prop,
                       line2_alias, line2_table, line2_prop,
                       cal_alias=ALIAS_CAL, cal_table=TABLE_CAL,
                       title=""):
    """Column + 2 lines combo chart"""
    from_set = {}
    for a, t in [(cal_alias, cal_table), (col_alias, col_table),
                 (line1_alias, line1_table), (line2_alias, line2_table)]:
        if a not in from_set:
            from_set[a] = t
    from_list = [{"Name": k, "Entity": v, "Type": 0} for k, v in from_set.items()]

    sv = {
        "visualType": "lineClusteredColumnComboChart",
        "projections": {
            "Category": [
                {"queryRef": f"{cal_table}.Date.Variation.Hierarquia de datas.Ano"},
                {"queryRef": f"{cal_table}.Date.Variation.Hierarquia de datas.Mês", "active": True},
            ],
            "Y":  [{"queryRef": f"{col_table}.{col_prop}"}],
            "Y2": [
                {"queryRef": f"{line1_table}.{line1_prop}"},
                {"queryRef": f"{line2_table}.{line2_prop}"},
            ],
        },
        "prototypeQuery": {
            "Version": 2,
            "From": from_list,
            "Select": [
                cal_level_select(cal_alias, cal_table, "Ano"),
                cal_level_select(cal_alias, cal_table, "Mês"),
                m_select(col_alias,   col_table,   col_prop),
                m_select(line1_alias, line1_table, line1_prop),
                m_select(line2_alias, line2_table, line2_prop),
            ],
        },
        "drillFilterOtherVisuals": True,
        "hasDefaultSort": False,
    }
    if title:
        sv["vcObjects"] = {"title": [{"properties": {
            "text": {"expr": {"Literal": {"Value": f"'{title}'"}}},
            "alignment": {"expr": {"Literal": {"Value": "'center'"}}},
        }}]}

    cfg = {"name": nid(), "layouts": layouts(x, y, z, w, h), "singleVisual": sv}
    return vc(cfg, x, y, z, w, h)


# ─────────────────────────────────────────────
# PAGE BUILDER
# ─────────────────────────────────────────────
def make_page(name, display_name, ordinal, visuals, page_id=None):
    import uuid, random
    return {
        "id": page_id if page_id else random.randint(489993540, 499999999),
        "name": name,
        "objectId": str(uuid.uuid4()),
        "displayName": display_name,
        "displayOption": 1,
        "ordinal": ordinal,
        "width": 1280,
        "height": 720,
        "visualContainers": visuals,
        "config": json.dumps({"objects": {}}, ensure_ascii=False),
        "filters": "[]",
    }


# ─────────────────────────────────────────────
# PAGE 1: QUALIDADE & SLA
# ─────────────────────────────────────────────
# Layout canvas 1280 x 720
# Row 0 (slicers):    y=2,  h=66
# Row 1 (cards KPI):  y=82, h=110
# Row 2 (charts):     y=208, h=237
# Row 3 (charts):     y=461, h=250

def build_page_qualidade_sla(ordinal):
    # ── Medidas ──────────────────────────────────────────────────────────────
    R = ALIAS_RS; T = TABLE_RS
    F = ALIAS_FS; TF = TABLE_FS

    # Card widths: 3 cards across 84..1194 = 1110 pts / (3 cards + 2 gaps=8)
    # w = (1110 - 16) / 3 = 364.6 ~ 364
    cw = 364
    cg = 9   # gap between cards
    cx1 = 84
    cx2 = cx1 + cw + cg   # 457
    cx3 = cx2 + cw + cg   # 830
    cy_cards = 82
    ch = 110

    # Chart widths: 2 charts, each ~579, gap ~10
    bw = 579; bh = 237; bg = 10
    bx1 = 84; bx2 = bx1 + bw + bg   # 673
    by1 = 207
    by2 = by1 + bh + 8  # 452

    visuals = []

    # ── Slicers ──────────────────────────────────────────────────────────────
    visuals.append(slicer(670, 2, 1000, 255, 66, F, TF, "MARCA", "Marca"))
    visuals.append(slicer(930, 2, 1100, 255, 66, F, TF, "CONSULTOR DE R&S", "Consultor"))

    # ── KPI Cards ────────────────────────────────────────────────────────────
    visuals.append(card(cx1, cy_cards, 2000, cw, ch,
        [(R, T, "SLA_R&S_Médio"), (R, T, "MoM_SLA_R&S_%")],
        col_props={f"{T}.MoM_SLA_R&S_%": "0.0%;-0.0%;0.0%"}
    ))
    visuals.append(card(cx2, cy_cards, 3000, cw, ch,
        [(R, T, "SLA_ADM_Médio"), (R, T, "MoM_SLA_ADM_%")],
        col_props={f"{T}.MoM_SLA_ADM_%": "0.0%;-0.0%;0.0%"}
    ))
    visuals.append(card(cx3, cy_cards, 4000, cw, ch,
        [(R, T, "Aging_Médio_Vagas_Abertas"), (R, T, "Vagas_Críticas_30d")],
    ))

    # ── Charts Row 1 ─────────────────────────────────────────────────────────
    visuals.append(bar_chart(
        bx1, by1, 5000, bw, bh,
        cat_alias=F, cat_table=TF, cat_prop="CONSULTOR DE R&S",
        measure_alias=R, measure_table=T, measure_prop="SLA_R&S_Médio",
        title=" SLA R&S Médio por Consultor (dias)",
        color=COLOR_TEAL, horizontal=True
    ))
    visuals.append(bar_chart(
        bx2, by1, 6000, bw, bh,
        cat_alias=F, cat_table=TF, cat_prop="MARCA",
        measure_alias=R, measure_table=T, measure_prop="SLA_ADM_Médio",
        title=" SLA ADM Médio por Marca (dias)",
        color=COLOR_CORAL, horizontal=True
    ))

    # ── Charts Row 2 ─────────────────────────────────────────────────────────
    visuals.append(combo_chart(
        bx1, by2, 7000, bw, bh,
        col_alias=R, col_table=T, col_prop="VagasFechadaR&S",
        line_alias=R, line_table=T, line_prop="SLA_R&S_Médio",
        title=" Fechamentos R&S × SLA R&S (por Mês)",
    ))
    visuals.append(combo_chart(
        bx2, by2, 8000, bw, bh,
        col_alias=R, col_table=T, col_prop="VagasFechadasAdmissão",
        line_alias=R, line_table=T, line_prop="SLA_ADM_Médio",
        title=" Fechamentos ADM × SLA ADM (por Mês)",
    ))

    return make_page(nid(), "Qualidade & SLA", ordinal, visuals)


# ─────────────────────────────────────────────
# PAGE 2: VISÃO ESTRATÉGICA
# ─────────────────────────────────────────────
def build_page_estrategica(ordinal):
    R = ALIAS_RS; T = TABLE_RS
    F = ALIAS_FS; TF = TABLE_FS

    # Row 0 (slicers):   y=2,  h=66
    # Row 1 (2 cards):   y=82, h=110  (2 wide cards)
    # Row 2 (wide combo):y=208, h=237 (full width)
    # Row 3 (3 items):   y=461, h=250 (2 bar charts + 1 small cards col)

    wide_w = 1175  # near full width
    cw_half = 579  # half-width card
    cg = 10

    cx1 = 84; cx2 = cx1 + cw_half + cg   # 673
    cy1 = 82; ch1 = 110
    by_wide = 207; bh_wide = 237
    by3 = 460; bh3 = 250

    bw3 = 370  # bottom row chart width
    cx3a = 84; cx3b = cx3a + bw3 + cg; cx3c = cx3b + bw3 + cg  # ~84, 464, 844

    visuals = []

    # ── Slicer ───────────────────────────────────────────────────────────────
    visuals.append(slicer(930, 2, 1000, 255, 66, F, TF, "MARCA", "Marca"))

    # ── KPI Cards Row 1 ──────────────────────────────────────────────────────
    visuals.append(card(cx1, cy1, 2000, cw_half, ch1,
        [(R, T, "Vagas_Abertas_Hoje"), (R, T, "Vagas_Abertas_MoM_Estoque_%_Card")],
    ))
    visuals.append(card(cx2, cy1, 3000, cw_half, ch1,
        [(R, T, "VagasFechadas_Total_MTD"),
         (R, T, "Projeção_Fechamentos_Mês"),
         (R, T, "MoM_MTD_VagasFechadas_%")],
        col_props={f"{T}.MoM_MTD_VagasFechadas_%": "0.0%;-0.0%;0.0%"}
    ))

    # ── Wide Combo Chart ─────────────────────────────────────────────────────
    visuals.append(combo_chart(
        cx1, by_wide, 4000, wide_w, bh_wide,
        col_alias=R, col_table=T, col_prop="VagasFechadas_Total",
        line_alias=R, line_table=T, line_prop="Vagas_Abertas_Acumulado_Periodo",
        title=" Vagas Fechadas × Estoque de Vagas Abertas (por Mês)",
    ))

    # ── Bottom Row: 3 charts ─────────────────────────────────────────────────
    # Small cards (pipeline) left
    visuals.append(card(cx3a, by3, 5000, bw3, 115,
        [(R, T, "Vagas_Congeladas"), (R, T, "Vagas_Em_Processo_Admissão"),
         (R, T, "Taxa_Cancelamento_%")],
        col_props={f"{T}.Taxa_Cancelamento_%": "0.0%;-0.0%;0.0%"}
    ))

    visuals.append(bar_chart(
        cx3b, by3, 6000, bw3, bh3,
        cat_alias=F, cat_table=TF, cat_prop="MARCA",
        measure_alias=R, measure_table=T, measure_prop="VagasFechadas_Total",
        title=" Vagas Fechadas por Marca",
        color=COLOR_TEAL, horizontal=True
    ))
    visuals.append(bar_chart(
        cx3c, by3, 7000, bw3, bh3,
        cat_alias=F, cat_table=TF, cat_prop="TIPO DE SOLICITAÇÃO RECEBIDA",
        measure_alias=R, measure_table=T, measure_prop="VagasFechadas_Total",
        title=" Vagas Fechadas por Tipo",
        color=COLOR_BLUE, horizontal=False
    ))

    return make_page(nid(), "Visão Estratégica", ordinal, visuals)


# ─────────────────────────────────────────────
# MAIN: read → patch → write
# ─────────────────────────────────────────────
def main():
    print(f"Fazendo backup: {BACKUP}")
    shutil.copy2(PBIX, BACKUP)

    # Read current layout
    with zipfile.ZipFile(PBIX, "r") as z:
        infos = {info.filename: info for info in z.infolist()}
        names = z.namelist()
        files = {n: z.read(n) for n in names}

    layout_raw = files["Report/Layout"].decode("utf-16-le")
    layout = json.loads(layout_raw)

    # Remove stale pages (ordinal 5 and 6 are duplicates/hidden)
    keep_ordinals = {0, 1, 2, 3, 4}
    sections = [s for s in layout["sections"] if s.get("ordinal") in keep_ordinals]

    # Add new pages
    max_ord = max(s["ordinal"] for s in sections)
    sections.append(build_page_qualidade_sla(max_ord + 1))
    sections.append(build_page_estrategica(max_ord + 2))

    layout["sections"] = sections

    # Re-encode
    # Compact JSON sem espaços extras — igual ao formato original do PBI
    new_layout = json.dumps(layout, ensure_ascii=False, separators=(',', ':')).encode("utf-16-le")
    files["Report/Layout"] = new_layout

    # Campo 'extra' presente em todos local file headers do original (lido via inspeção binária)
    # Header ID 0xA220 (28 bytes) — campo proprietário Power BI / OPC que deve ser preservado
    PBI_EXTRA = bytes.fromhex("20a2180028a014000000000000000000000000000000000000000000")

    # Write back preservando todos os metadados incluindo o campo extra
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zout:
        for name in names:
            orig_info = infos[name]
            data = new_layout if name == "Report/Layout" else files[name]
            new_info = zipfile.ZipInfo(orig_info.filename)
            new_info.compress_type   = orig_info.compress_type
            new_info.create_system   = orig_info.create_system
            new_info.create_version  = orig_info.create_version
            new_info.extract_version = orig_info.extract_version
            new_info.external_attr   = orig_info.external_attr
            new_info.flag_bits       = orig_info.flag_bits & ~0x08
            new_info.extra           = PBI_EXTRA  # campo proprietário obrigatório
            zout.writestr(new_info, data)

    out = PBIX.replace(".pbix", "_NOVO.pbix")
    with open(out, "wb") as f:
        f.write(buf.getvalue())

    print(f"OK! Arquivo gerado: {out}")
    print(f"  Paginas removidas: Geral- Omitida e Duplicata de Geral")
    print(f"  Paginas adicionadas: Qualidade & SLA e Visao Estrategica")
    print(f"\n  Feche o Power BI Desktop e abra o arquivo _NOVO.pbix")

if __name__ == "__main__":
    main()
