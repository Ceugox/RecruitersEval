import zipfile, json

PBIX = "Dashboard Métricas P&C .pbix"

with zipfile.ZipFile(PBIX, "r") as z:
    layout_raw = z.read("Report/Layout").decode("utf-16-le")

layout = json.loads(layout_raw)
geral = next(s for s in layout["sections"] if s.get("displayName") == "Geral")

# Inspeciona visuais 5 (CARGO) e 6 (MARCA) em detalhe
for i in [5, 6]:
    vc = geral["visualContainers"][i]
    cfg = json.loads(vc.get("config", "{}"))
    print(f"\n=== Visual [{i}] ===")
    print(json.dumps(cfg, indent=2, ensure_ascii=False))
