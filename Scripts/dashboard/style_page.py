"""
Estiliza a página 'Qualidade SLA' do Dashboard Métricas P&C.pbix.

INSTRUÇÕES:
  1. Salve e feche o Power BI Desktop (Ctrl+S → feche)
  2. Execute: python style_page.py
  3. Abra Dashboard Métricas P&C_NOVO.pbix
"""
import zipfile, json, io, shutil, os

PBIX   = "Dashboard Métricas P&C .pbix"
BACKUP = "Dashboard Métricas P&C_style.bak"

# ── Paleta ──────────────────────────────────────────────────────────────────
BG_PAGE  = "#F0F4F8"   # fundo da página
BG_CARD  = "#FFFFFF"   # fundo dos visuals
BORDER   = "#D0DCE8"   # borda dos visuals
TEAL     = "#7AC5BF"   # R&S / dentro do prazo
CORAL    = "#E8856A"   # ADM / fora do prazo
TXT      = "#1B2A3B"   # texto

# ── Primitivos JSON ─────────────────────────────────────────────────────────
def lit(v):
    return {"expr": {"Literal": {"Value": v}}}

def clr(hex_color):
    return {"solid": {"color": lit(f"'{hex_color}'")}}

def bg_obj(show=True, color=BG_CARD):
    return [{"properties": {"show": lit("true" if show else "false"), "color": clr(color)}}]

def border_obj(show=True, color=BORDER, radius=8):
    return [{"properties": {
        "show": lit("true" if show else "false"),
        "color": clr(color),
        "radius": lit(f"{radius}D"),
    }}]

def shadow_obj():
    return [{"properties": {"show": lit("true")}}]

def axis_obj(gridline_color="#E8EEF4"):
    return [{"properties": {
        "showAxisTitle": lit("false"),
        "gridlineColor": clr(gridline_color),
    }}]

# ── Aplica estilo no container (vcObjects) ──────────────────────────────────
def style_container(sv, bg=True, border=True, shadow=True, bg_color=BG_CARD):
    vc = sv.get("vcObjects", {})
    vc["background"] = bg_obj(bg, bg_color)
    if border:
        vc["border"] = border_obj()
    if shadow:
        vc["dropShadow"] = shadow_obj()
    # Padroniza título se existir
    if "title" in vc and vc["title"]:
        props = vc["title"][0].get("properties", {})
        props["fontColor"] = clr(TXT)
        props["alignment"] = lit("'center'")
        vc["title"] = [{"properties": props}]
    sv["vcObjects"] = vc
    return sv

# ── Cores dos segmentos do donut (por valor de categoria) ───────────────────
def donut_data_colors(sv, source_alias, status_col="Status"):
    """Aplica teal p/ 'Dentro do prazo' e coral p/ 'Fora do prazo'."""
    def selector(value):
        return {"data": {"expr": {"In": {
            "Expressions": [{"Column": {
                "Expression": {"SourceRef": {"Source": source_alias}},
                "Property": status_col,
            }}],
            "Values": [[{"Literal": {"Value": f"'{value}'"}}]],
        }}}}

    objs = sv.get("objects", {})
    objs["dataPoint"] = [
        {"selector": selector("Dentro do prazo"), "properties": {"fill": clr(TEAL)}},
        {"selector": selector("Fora do prazo"),   "properties": {"fill": clr(CORAL)}},
    ]
    sv["objects"] = objs
    return sv

# ── Cores de linha/série ────────────────────────────────────────────────────
def line_data_colors(sv):
    objs = sv.get("objects", {})
    objs["dataPoint"] = [
        {"id": 0, "properties": {"fill": clr(TEAL)}},
        {"id": 1, "properties": {"fill": clr(CORAL)}},
    ]
    objs["valueAxis"]    = axis_obj()
    objs["categoryAxis"] = [{"properties": {"showAxisTitle": lit("false")}}]
    sv["objects"] = objs
    return sv

# ── Estilo de eixos para barras/colunas ────────────────────────────────────
def column_axes(sv):
    objs = sv.get("objects", {})
    objs["valueAxis"]    = axis_obj()
    objs["categoryAxis"] = [{"properties": {"showAxisTitle": lit("false")}}]
    sv["objects"] = objs
    return sv

# ── Detecta alias da tabela Status Prazo no From do visual ─────────────────
def get_status_alias(sv):
    frm = sv.get("prototypeQuery", {}).get("From", [])
    for entry in frm:
        if "Status Prazo" in entry.get("Entity", ""):
            return entry.get("Name", "s")
    return "s"

# ── Processa a página ───────────────────────────────────────────────────────
def process_sections(sections):
    page = None
    for s in sections:
        if "Qualidade" in s.get("displayName", "") or "SLA" in s.get("displayName", ""):
            page = s
            break
    if not page:
        print("⚠ Página Qualidade SLA não encontrada!")
        return sections

    # Fundo da página
    pcfg = json.loads(page.get("config", "{}"))
    pcfg.setdefault("objects", {})
    pcfg["objects"]["background"] = [{"properties": {
        "show": lit("true"),
        "color": clr(BG_PAGE),
        "transparency": lit("0D"),
    }}]
    page["config"] = json.dumps(pcfg, ensure_ascii=False)

    for vc in page.get("visualContainers", []):
        cfg = json.loads(vc.get("config", "{}"))
        sv  = cfg.get("singleVisual", {})
        vt  = sv.get("visualType", "")

        if vt == "donutChart":
            alias = get_status_alias(sv)
            sv = donut_data_colors(sv, alias)
            sv = style_container(sv, bg=True, border=True, shadow=True)

        elif vt in ("lineChart", "lineClusteredColumnComboChart"):
            sv = line_data_colors(sv)
            sv = style_container(sv, bg=True, border=True, shadow=True)

        elif vt in ("columnChart", "clusteredBarChart", "clusteredColumnChart", "barChart"):
            sv = column_axes(sv)
            sv = style_container(sv, bg=True, border=True, shadow=True)

        elif vt == "cardVisual":
            sv = style_container(sv, bg=True, border=True, shadow=False)

        elif vt == "slicer":
            sv = style_container(sv, bg=True, border=True, shadow=False, bg_color="#FFFFFF")

        elif vt == "actionButton":
            pass  # preserva botões de navegação

        else:
            sv = style_container(sv, bg=True, border=False, shadow=False)

        cfg["singleVisual"] = sv
        vc["config"] = json.dumps(cfg, ensure_ascii=False)

    print(f"OK: Pagina '{page['displayName']}' estilizada - {len(page['visualContainers'])} visuais processados")
    return sections

# ── Main ────────────────────────────────────────────────────────────────────
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pbix = os.path.join(script_dir, PBIX)
    bak  = os.path.join(script_dir, BACKUP)
    out  = pbix.replace(".pbix", "_NOVO.pbix")

    if not os.path.exists(pbix):
        print(f"ERRO: Arquivo nao encontrado: {pbix}")
        return

    print(f"Backup: {bak}")
    shutil.copy2(pbix, bak)

    with zipfile.ZipFile(pbix, "r") as z:
        infos = {i.filename: i for i in z.infolist()}
        names = z.namelist()
        files = {n: z.read(n) for n in names}

    layout = json.loads(files["Report/Layout"].decode("utf-16-le"))
    layout["sections"] = process_sections(layout["sections"])

    new_layout = json.dumps(layout, ensure_ascii=False, separators=(',', ':')).encode("utf-16-le")
    files["Report/Layout"] = new_layout

    PBI_EXTRA = bytes.fromhex("20a2180028a014000000000000000000000000000000000000000000")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zout:
        for name in names:
            orig = infos[name]
            data = new_layout if name == "Report/Layout" else files[name]
            ni = zipfile.ZipInfo(orig.filename)
            ni.compress_type   = orig.compress_type
            ni.create_system   = orig.create_system
            ni.create_version  = orig.create_version
            ni.extract_version = orig.extract_version
            ni.external_attr   = orig.external_attr
            ni.flag_bits       = orig.flag_bits & ~0x08
            ni.extra           = PBI_EXTRA
            zout.writestr(ni, data)

    with open(out, "wb") as f:
        f.write(buf.getvalue())

    print(f"Gerado: {out}")
    print("Abra o _NOVO.pbix no Power BI Desktop")

if __name__ == "__main__":
    main()
