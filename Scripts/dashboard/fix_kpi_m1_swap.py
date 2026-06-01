"""
Corrige o KPI "Fechamento de Vagas (M-1)" na página Recrutadores:
troca Indicator (Rec_RS_MediaMensal) <-> Goal (Rec_RS_MesAnterior)
para que o valor principal seja o M-1 e a meta seja a média trimestral.
"""
import zipfile, json, os, shutil

PBIX = os.path.join(os.path.dirname(__file__), "..", "Dashboard Métricas P&C .pbix")
PBIX = os.path.normpath(PBIX)
TMP  = PBIX + ".patch_tmp"

def patch_layout(raw: str) -> str:
    layout = json.loads(raw)
    fixed = False

    for page in layout.get("sections", []):
        if "Recrutador" not in page.get("displayName", ""):
            continue
        for vc in page.get("visualContainers", []):
            cfg = json.loads(vc.get("config", "{}"))
            sv  = cfg.get("singleVisual", {})
            if sv.get("visualType") != "kpi":
                continue

            # Identifica pelo título
            title_obj  = sv.get("vcObjects", {}).get("title", [{}])
            title_text = ""
            if title_obj:
                tp = title_obj[0].get("properties", {}).get("text", {})
                title_text = tp.get("expr", {}).get("Literal", {}).get("Value", "")

            if "M-1" not in title_text or "Vagas" not in title_text:
                continue

            projs = sv.get("projections", {})
            ind   = projs.get("Indicator", [])
            goal  = projs.get("Goal", [])

            print(f"  Antes  → Indicator: {ind}  |  Goal: {goal}")
            projs["Indicator"] = goal
            projs["Goal"]      = ind
            print(f"  Depois → Indicator: {projs['Indicator']}  |  Goal: {projs['Goal']}")

            vc["config"] = json.dumps(cfg, ensure_ascii=False)
            fixed = True

    if not fixed:
        raise RuntimeError("KPI 'Fechamento de Vagas (M-1)' não encontrado — verifique o nome da página/título.")

    return json.dumps(layout, ensure_ascii=False)


def main():
    print(f"Arquivo: {PBIX}")

    with zipfile.ZipFile(PBIX, "r") as zin:
        with zipfile.ZipFile(TMP, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "Report/Layout":
                    raw      = data.decode("utf-16-le")
                    patched  = patch_layout(raw)
                    data     = patched.encode("utf-16-le")
                    print("Layout corrigido.")
                zout.writestr(item, data)

    os.replace(TMP, PBIX)
    print("✓ Arquivo salvo com sucesso.")


if __name__ == "__main__":
    main()
