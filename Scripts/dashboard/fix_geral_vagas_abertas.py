"""
Corrige os gráficos "Vagas Abertas por Cargo" e "Vagas Abertas por Marca"
na aba Geral do Dashboard Métricas P&C.pbix.

Problema: os visuais usavam CountNonNull(TICKET) — agregação bruta sem
lógica de "vaga aberta". Por isso ficavam em branco em maio/26 (nenhum
ticket com DATA DE ABERTURA em maio).

Correção: substituir pelo medida Vagas_Abertas_Acumulado_Periodo, que conta
vagas que estiveram abertas em qualquer dia do período selecionado.

INSTRUÇÕES:
  1. No Power BI Desktop, salve (Ctrl+S)
  2. Feche o Power BI Desktop
  3. Execute: python fix_geral_vagas_abertas.py
  4. Abra o arquivo gerado: Dashboard Métricas P&C_CORRIGIDO.pbix
"""

import zipfile, json, io, shutil

PBIX   = "Dashboard Métricas P&C .pbix"
OUT    = "Dashboard Métricas P&C_CORRIGIDO.pbix"
BACKUP = "Dashboard Métricas P&C .pbix.bak2"

TABLE_RS  = "R&S_CONTROLE DE VAGAS 2026"
TABLE_FS  = "Fonte_Sheets"
ALIAS_RS  = "r"
ALIAS_FS  = "f"
MEASURE   = "Vagas_Abertas_Acumulado_Periodo"

# Campo extra proprietário do PBI (deve ser preservado em todos os ZipInfo)
PBI_EXTRA = bytes.fromhex("20a2180028a014000000000000000000000000000000000000000000")


def build_measure_select(alias, table, prop):
    return {
        "Measure": {
            "Expression": {"SourceRef": {"Source": alias}},
            "Property": prop,
        },
        "Name": f"{table}.{prop}",
        "NativeReferenceName": prop,
    }


def build_measure_orderby(alias, prop):
    return {
        "Direction": 2,
        "Expression": {
            "Measure": {
                "Expression": {"SourceRef": {"Source": alias}},
                "Property": prop,
            }
        },
    }


def patch_visual(cfg_str, cat_col):
    """
    Substitui a agregação bruta de TICKET pela medida Vagas_Abertas_Acumulado_Periodo.
    cat_col: 'CARGO' ou 'MARCA'
    """
    cfg = json.loads(cfg_str)
    sv  = cfg["singleVisual"]
    q   = sv["prototypeQuery"]

    # ── From: garante que a tabela de medidas está presente ──────────────────
    from_names = {f["Name"] for f in q["From"]}
    if ALIAS_RS not in from_names:
        q["From"].append({"Name": ALIAS_RS, "Entity": TABLE_RS, "Type": 0})

    # ── Select: remove a Aggregation de TICKET, mantém a Column do cat_col ──
    new_select = []
    for s in q["Select"]:
        if "Aggregation" in s:
            continue          # descarta CountNonNull / Count de TICKET
        if "Column" in s and s["Column"]["Property"] == cat_col:
            new_select.append(s)  # mantém a coluna de categoria

    # Adiciona a medida
    new_select.append(build_measure_select(ALIAS_RS, TABLE_RS, MEASURE))
    q["Select"] = new_select

    # ── Projections: atualiza o queryRef da série Y ───────────────────────────
    sv["projections"]["Y"] = [{"queryRef": f"{TABLE_RS}.{MEASURE}"}]

    # ── OrderBy: substitui pela medida ───────────────────────────────────────
    q["OrderBy"] = [build_measure_orderby(ALIAS_RS, MEASURE)]

    # ── columnProperties: remove chave antiga (evita warning no PBI) ─────────
    sv.pop("columnProperties", None)

    return json.dumps(cfg, ensure_ascii=False, separators=(",", ":"))


def main():
    print(f"Backup → {BACKUP}")
    shutil.copy2(PBIX, BACKUP)

    with zipfile.ZipFile(PBIX, "r") as z:
        infos  = {info.filename: info for info in z.infolist()}
        names  = z.namelist()
        files  = {n: z.read(n) for n in names}

    layout_raw = files["Report/Layout"].decode("utf-16-le")
    layout     = json.loads(layout_raw)

    # ── Localiza a aba Geral ─────────────────────────────────────────────────
    geral = next(s for s in layout["sections"] if s.get("displayName") == "Geral")
    patched = 0

    for vc in geral["visualContainers"]:
        cfg_str = vc.get("config", "{}")
        cfg     = json.loads(cfg_str)
        sv      = cfg.get("singleVisual", {})
        title_nodes = (
            sv.get("vcObjects", {})
              .get("title", [{}])[0]
              .get("properties", {})
              .get("text", {})
              .get("expr", {})
              .get("Literal", {})
              .get("Value", "")
        )
        title = title_nodes.strip("'")

        if title == "Vagas Abertas por Cargo":
            vc["config"] = patch_visual(cfg_str, "CARGO")
            print(f"  ✔ Corrigido: '{title}'  →  medida {MEASURE}")
            patched += 1

        elif title == "Vagas Abertas por Marca":
            vc["config"] = patch_visual(cfg_str, "MARCA")
            print(f"  ✔ Corrigido: '{title}'  →  medida {MEASURE}")
            patched += 1

    if patched == 0:
        print("ATENÇÃO: Nenhum visual encontrado pelo título. Verifique os títulos dos gráficos.")
        return

    # ── Re-serializa layout ──────────────────────────────────────────────────
    new_layout = json.dumps(layout, ensure_ascii=False, separators=(",", ":")).encode("utf-16-le")
    files["Report/Layout"] = new_layout

    # ── Reconstrói o .pbix preservando metadados ─────────────────────────────
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zout:
        for name in names:
            orig  = infos[name]
            data  = new_layout if name == "Report/Layout" else files[name]
            info  = zipfile.ZipInfo(orig.filename)
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

    print(f"\nArquivo gerado: {OUT}")
    print("Abra-o no Power BI Desktop e teste o filtro de maio/26.")


if __name__ == "__main__":
    main()
