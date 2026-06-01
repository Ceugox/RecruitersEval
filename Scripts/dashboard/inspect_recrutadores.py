import zipfile, json, os

for PBIX in ["Dashboard Métricas P&C .pbix",
             "Dashboard Métricas P&C_NOVO.pbix",
             "Dashboard Métricas P&C - Copia.pbix",
             "Dashboard Métricas P&C_CORRIGIDO.pbix"]:
    if not os.path.exists(PBIX):
        continue
    try:
        with zipfile.ZipFile(PBIX, "r") as z:
            layout_raw = z.read("Report/Layout").decode("utf-16-le")
        layout = json.loads(layout_raw)
        pages = [(s["ordinal"], s["displayName"], len(s["visualContainers"])) for s in layout["sections"]]
        print(f"\n=== {PBIX} ===")
        for ord_, name, nv in sorted(pages):
            marker = " <<<" if "ecrutar" in name else ""
            print(f"  {ord_}: {name} ({nv} visuais){marker}")
    except Exception as e:
        print(f"  ERRO: {e}")
