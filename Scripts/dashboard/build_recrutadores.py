"""
Cria/substitui a aba "Recrutadores" no Dashboard Métricas P&C.

Layout (1280 x 720):
  Linha 0 — Slicer MARCA (y=2, h=50)
  Linha 1 — 4 KPI cards (y=60, h=90):
              Média R&S/mês | Média ADM/mês | R&S Mês Atual | ADM Mês Atual
  Linha 2 — Ranking dual (y=158, h=270):
              Barras R&S (Rec_RS_MediaMensal) | Barras ADM (Rec_ADM_MediaMensal)
  Linha 3 — Volume 3M (y=436, h=272):
              Barras agrupadas: Rec_RS_3M × Rec_ADM_3M por consultor

INSTRUÇÕES:
  1. No Power BI Desktop → Ctrl+S → Fechar
  2. python build_recrutadores.py
  3. Abrir o arquivo gerado: Dashboard Métricas P&C_RECRUTADORES.pbix
"""

import zipfile, json, uuid, io, shutil, random, os

PBIX   = "Dashboard Métricas P&C .pbix"
OUT    = "Dashboard Métricas P&C_RECRUTADORES.pbix"
BACKUP = "Dashboard Métricas P&C .pbix.bak_rec"

TABLE_RS   = "R&S_CONTROLE DE VAGAS 2026"
TABLE_FS   = "Fonte_Sheets"
ALIAS_RS   = "r"
ALIAS_FS   = "f"
COLOR_TEAL  = "#7AC5BF"
COLOR_CORAL = "#E8856A"

PBI_EXTRA = bytes.fromhex("20a2180028a014000000000000000000000000000000000000000000")


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def nid():
    return uuid.uuid4().hex[:20]

def m_select(alias, table, prop):
    return {
        "Measure": {"Expression": {"SourceRef": {"Source": alias}}, "Property": prop},
        "Name": f"{table}.{prop}",
        "NativeReferenceName": prop,
    }

def c_select(alias, table, prop):
    return {
        "Column": {"Expression": {"SourceRef": {"Source": alias}}, "Property": prop},
        "Name": f"{table}.{prop}",
        "NativeReferenceName": prop,
    }

def layouts(x, y, z, w, h):
    return [
        {"id": 0, "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z}},
        {"id": 1, "position": {"x": 0, "y": 0, "z": z, "width": 324, "height": 180, "tabOrder": z}},
    ]

def vc(cfg, x, y, z, w, h):
    return {
        "id": random.randint(10_000_000_000, 99_999_999_999),
        "x": x, "y": y, "z": z,
        "width": w, "height": h,
        "tabOrder": z,
        "config": json.dumps(cfg, ensure_ascii=False),
        "filters": "[]",
    }


# ─────────────────────────────────────────────────────────────────────────────
# VISUAL BUILDERS
# ─────────────────────────────────────────────────────────────────────────────
def card(x, y, z, w, h, measures):
    """Card com uma ou mais medidas."""
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
    cfg = {"name": nid(), "layouts": layouts(x, y, z, w, h), "singleVisual": sv}
    return vc(cfg, x, y, z, w, h)


def slicer(x, y, z, w, h, alias, table, prop, label, mode="Dropdown"):
    from_list = [{"Name": alias, "Entity": table, "Type": 0}]
    sv = {
        "visualType": "slicer",
        "projections": {"Values": [{"queryRef": f"{table}.{prop}", "active": True}]},
        "prototypeQuery": {
            "Version": 2,
            "From": from_list,
            "Select": [c_select(alias, table, prop)],
        },
        "drillFilterOtherVisuals": True,
        "objects": {
            "data": [{"properties": {"mode": {"expr": {"Literal": {"Value": f"'{mode}'"}}}}}],
            "header": [{"properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "text": {"expr": {"Literal": {"Value": f"'{label}'"}}},
            }}],
        },
        "vcObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
        },
    }
    cfg = {"name": nid(), "layouts": layouts(x, y, z, w, h), "singleVisual": sv}
    return vc(cfg, x, y, z, w, h)


def bar_single(x, y, z, w, h, cat_alias, cat_table, cat_prop,
               m_alias, m_table, m_prop, title="", color=COLOR_TEAL):
    """Barra horizontal com uma medida, ordenada decrescente (ranking)."""
    from_list = [{"Name": cat_alias, "Entity": cat_table, "Type": 0}]
    if m_alias != cat_alias:
        from_list.append({"Name": m_alias, "Entity": m_table, "Type": 0})

    sv = {
        "visualType": "clusteredBarChart",
        "projections": {
            "Category": [{"queryRef": f"{cat_table}.{cat_prop}", "active": True}],
            "Y":        [{"queryRef": f"{m_table}.{m_prop}"}],
        },
        "prototypeQuery": {
            "Version": 2,
            "From": from_list,
            "Select": [
                c_select(cat_alias, cat_table, cat_prop),
                m_select(m_alias, m_table, m_prop),
            ],
            "OrderBy": [{"Direction": 2, "Expression": {
                "Measure": {"Expression": {"SourceRef": {"Source": m_alias}}, "Property": m_prop}
            }}],
        },
        "drillFilterOtherVisuals": True,
        "hasDefaultSort": True,
        "objects": {
            "dataPoint": [{"properties": {"fill": {"solid": {"color": {
                "expr": {"Literal": {"Value": f"'{color}'"}}
            }}}}}],
            "valueAxis":    [{"properties": {"showAxisTitle": {"expr": {"Literal": {"Value": "false"}}}}}],
            "categoryAxis": [{"properties": {"showAxisTitle": {"expr": {"Literal": {"Value": "false"}}}}}],
        },
        "vcObjects": {"title": [{"properties": {
            "text":      {"expr": {"Literal": {"Value": f"'{title}'"}}},
            "alignment": {"expr": {"Literal": {"Value": "'center'"}}},
        }}]},
    }
    cfg = {"name": nid(), "layouts": layouts(x, y, z, w, h), "singleVisual": sv}
    return vc(cfg, x, y, z, w, h)


def bar_dual(x, y, z, w, h, cat_alias, cat_table, cat_prop,
             m1_alias, m1_table, m1_prop,
             m2_alias, m2_table, m2_prop,
             title=""):
    """Barra horizontal agrupada com DUAS medidas (R&S × ADM) por categoria."""
    from_set = {}
    for a, t in [(cat_alias, cat_table), (m1_alias, m1_table), (m2_alias, m2_table)]:
        if a not in from_set:
            from_set[a] = t
    from_list = [{"Name": k, "Entity": v, "Type": 0} for k, v in from_set.items()]

    sv = {
        "visualType": "clusteredBarChart",
        "projections": {
            "Category": [{"queryRef": f"{cat_table}.{cat_prop}", "active": True}],
            "Y": [
                {"queryRef": f"{m1_table}.{m1_prop}"},
                {"queryRef": f"{m2_table}.{m2_prop}"},
            ],
        },
        "prototypeQuery": {
            "Version": 2,
            "From": from_list,
            "Select": [
                c_select(cat_alias, cat_table, cat_prop),
                m_select(m1_alias, m1_table, m1_prop),
                m_select(m2_alias, m2_table, m2_prop),
            ],
            "OrderBy": [{"Direction": 2, "Expression": {
                "Measure": {"Expression": {"SourceRef": {"Source": m1_alias}}, "Property": m1_prop}
            }}],
        },
        "drillFilterOtherVisuals": True,
        "hasDefaultSort": True,
        "objects": {
            "valueAxis":    [{"properties": {"showAxisTitle": {"expr": {"Literal": {"Value": "false"}}}}}],
            "categoryAxis": [{"properties": {"showAxisTitle": {"expr": {"Literal": {"Value": "false"}}}}}],
        },
        "vcObjects": {"title": [{"properties": {
            "text":      {"expr": {"Literal": {"Value": f"'{title}'"}}},
            "alignment": {"expr": {"Literal": {"Value": "'center'"}}},
        }}]},
    }
    cfg = {"name": nid(), "layouts": layouts(x, y, z, w, h), "singleVisual": sv}
    return vc(cfg, x, y, z, w, h)


def make_page(name, display_name, ordinal, visuals):
    return {
        "id": random.randint(489993540, 499999999),
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


# ─────────────────────────────────────────────────────────────────────────────
# PÁGINA RECRUTADORES
# ─────────────────────────────────────────────────────────────────────────────
def build_page_recrutadores(ordinal):
    R = ALIAS_RS;  T = TABLE_RS
    F = ALIAS_FS;  TF = TABLE_FS

    # ── Coordenadas ──────────────────────────────────────────────────────────
    CX_L    = 84      # margem esquerda
    CX_R    = 664     # início coluna direita
    CW_HALF = 572     # largura meia-tela
    CW_FULL = 1175    # largura tela cheia

    # Linhas verticais
    Y_SL    = 2;   H_SL  = 50    # slicer
    Y_KPI   = 60;  H_KPI = 90    # cards KPI
    Y_RANK  = 158; H_RANK= 270   # rankings
    Y_BOT   = 436; H_BOT = 272   # volume 3M

    # Cards: 4 cartas distribuídas entre x=84 e x=1185
    # w = (1185-84-3*10)/4 = (1101-30)/4 = 267
    CW_CARD = 267
    CG_CARD = 10
    cx_cards = [CX_L + i * (CW_CARD + CG_CARD) for i in range(4)]

    visuals = []

    # ── Slicer MARCA ─────────────────────────────────────────────────────────
    visuals.append(slicer(
        930, Y_SL, 500, 255, H_SL,
        F, TF, "MARCA", "Marca", mode="Dropdown"
    ))

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    # Card 1: Média R&S/mês + total 3M
    visuals.append(card(cx_cards[0], Y_KPI, 1000, CW_CARD, H_KPI, [
        (R, T, "Rec_RS_MediaMensal"),
        (R, T, "Rec_RS_3M"),
    ]))
    # Card 2: Média ADM/mês + total 3M
    visuals.append(card(cx_cards[1], Y_KPI, 1100, CW_CARD, H_KPI, [
        (R, T, "Rec_ADM_MediaMensal"),
        (R, T, "Rec_ADM_3M"),
    ]))
    # Card 3: R&S mês atual + mês anterior
    visuals.append(card(cx_cards[2], Y_KPI, 1200, CW_CARD, H_KPI, [
        (R, T, "Rec_RS_MesAtual"),
        (R, T, "Rec_RS_MesAnterior"),
    ]))
    # Card 4: ADM mês atual + mês anterior
    visuals.append(card(cx_cards[3], Y_KPI, 1300, CW_CARD, H_KPI, [
        (R, T, "Rec_ADM_MesAtual"),
        (R, T, "Rec_ADM_MesAnterior"),
    ]))

    # ── Rankings (barra horizontal, ordenada por média mensal) ───────────────
    visuals.append(bar_single(
        CX_L, Y_RANK, 2000, CW_HALF, H_RANK,
        cat_alias=F, cat_table=TF, cat_prop="CONSULTOR DE R&S",
        m_alias=R, m_table=T, m_prop="Rec_RS_MediaMensal",
        title=" Ranking R&S — Média Mensal (3M)",
        color=COLOR_TEAL,
    ))
    visuals.append(bar_single(
        CX_R, Y_RANK, 3000, CW_HALF, H_RANK,
        cat_alias=F, cat_table=TF, cat_prop="CONSULTOR DE R&S",
        m_alias=R, m_table=T, m_prop="Rec_ADM_MediaMensal",
        title=" Ranking ADM — Média Mensal (3M)",
        color=COLOR_CORAL,
    ))

    # ── Volume 3M: R&S × ADM por consultor (barras agrupadas) ────────────────
    visuals.append(bar_dual(
        CX_L, Y_BOT, 4000, CW_FULL, H_BOT,
        cat_alias=F, cat_table=TF, cat_prop="CONSULTOR DE R&S",
        m1_alias=R, m1_table=T, m1_prop="Rec_RS_3M",
        m2_alias=R, m2_table=T, m2_prop="Rec_ADM_3M",
        title=" Volume Total — Últimos 3 Meses Completos (R&S × ADM)",
    ))

    return make_page(nid(), "Recrutadores", ordinal, visuals)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print(f"Lendo: {PBIX}")
    print(f"Backup -> {BACKUP}")
    shutil.copy2(PBIX, BACKUP)

    with zipfile.ZipFile(PBIX, "r") as z:
        infos = {info.filename: info for info in z.infolist()}
        names = z.namelist()
        files = {n: z.read(n) for n in names}

    layout_raw = files["Report/Layout"].decode("utf-16-le")
    layout = json.loads(layout_raw)

    # Verifica se página já existe (salva pelo PBI Desktop)
    rec_existing = next(
        (s for s in layout["sections"] if "ecrutar" in s.get("displayName", "")),
        None
    )

    if rec_existing:
        ordinal = rec_existing["ordinal"]
        print(f"Página 'Recrutadores' encontrada (ordinal={ordinal}). Substituindo visuais...")
        rec_page = build_page_recrutadores(ordinal)
        # Preserva name/objectId/ordinal originais para não quebrar referências
        rec_page["name"]      = rec_existing["name"]
        rec_page["objectId"]  = rec_existing.get("objectId", rec_page["objectId"])
        rec_page["ordinal"]   = ordinal
        layout["sections"] = [
            rec_page if s is rec_existing else s
            for s in layout["sections"]
        ]
    else:
        max_ord = max(s["ordinal"] for s in layout["sections"])
        ordinal = max_ord + 1
        print(f"Página 'Recrutadores' não encontrada. Criando como ordinal={ordinal}...")
        layout["sections"].append(build_page_recrutadores(ordinal))

    # Re-serializa e salva
    new_layout = json.dumps(layout, ensure_ascii=False, separators=(",", ":")).encode("utf-16-le")
    files["Report/Layout"] = new_layout

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zout:
        for name in names:
            orig = infos[name]
            data = new_layout if name == "Report/Layout" else files[name]
            info = zipfile.ZipInfo(orig.filename)
            info.compress_type   = orig.compress_type
            info.create_system   = orig.create_system
            info.create_version  = orig.create_version
            info.extract_version = orig.extract_version
            info.external_attr   = orig.external_attr
            info.flag_bits       = orig.flag_bits & ~0x08
            info.extra           = PBI_EXTRA
            zout.writestr(info, data)

    with open(OUT, "wb") as f:
        f.write(buf.getvalue())

    print(f"\nOK! Arquivo gerado: {OUT}")
    print(f"  Visuais criados: 1 slicer + 4 cards + 2 rankings + 1 volume 3M")
    print(f"\n  Feche o Power BI Desktop e abra o arquivo acima.")


if __name__ == "__main__":
    main()
