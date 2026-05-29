"""
performance.py — Calcula vagas fechadas na semana atual por recrutador.

Filtros aplicados sobre a planilha Fonte_Sheets:
  - STATUS == "FECHADA"
  - NOME COMPLETO not null/empty
  - DATA DE FECHAMENTO DA VAGA not null
  - TIPO DE SOLICITAÇÃO RECEBIDA == "R&S"
  - DATA DE FECHAMENTO DA VAGA >= segunda-feira da semana atual
  - DATA DE FECHAMENTO DA VAGA <= hoje
Contagem por CONSULTOR DE R&S (distinct tickets por nome do consultor).
"""

from datetime import date, timedelta, datetime


def _parse_date_safe(value) -> date | None:
    """Tenta converter string ou objeto para date. Suporta formatos dd/mm/yyyy e yyyy-mm-dd."""
    if not value:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    s = str(value).strip()
    if not s:
        return None
    # Tenta os formatos mais comuns na planilha (incluindo ISO 8601 do Google Sheets)
    for fmt in (
        "%Y-%m-%dT%H:%M:%S.%fZ",  # 2025-12-22T03:00:00.000Z (Google Sheets JSON)
        "%Y-%m-%dT%H:%M:%SZ",     # 2025-12-22T03:00:00Z
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%d/%m/%y",
        "%Y/%m/%d",
    ):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def get_week_start() -> date:
    """Retorna a segunda-feira da semana atual."""
    today = date.today()
    return today - timedelta(days=today.weekday())


def calcular_vagas_semana(records: list[dict], nome_planilha: str) -> int:
    """
    Conta vagas fechadas na semana atual para um recrutador específico.

    Args:
        records: Lista de dicts retornada por sheets_reader.read_sheet()
        nome_planilha: Nome exato do consultor como aparece na coluna
                       'CONSULTOR DE R&S' da planilha.

    Returns:
        Número de vagas fechadas no período (segunda-feira até hoje).
    """
    week_start = get_week_start()
    today = date.today()

    # Descobre o nome exato da coluna de tipo (pode ter acentuação variável)
    col_tipo = next(
        (k for k in (records[0].keys() if records else [])
         if "TIPO" in k.upper() and "SOLIC" in k.upper()),
        "TIPO DE SOLICITAÇÃO RECEBIDA",
    )

    count = 0
    for row in records:
        # Filtro 1: tipo de solicitação == R&S
        tipo = (row.get(col_tipo) or "").strip().upper()
        if tipo != "R&S":
            continue

        # Filtro 2: nome completo preenchido (candidato identificado)
        nome_completo = (row.get("NOME COMPLETO") or "").strip()
        if not nome_completo:
            continue

        # Filtro 3: consultor de R&S bate com o recrutador
        consultor = (row.get("CONSULTOR DE R&S") or "").strip().upper()
        if consultor != nome_planilha.strip().upper():
            continue

        # Filtro 4: data de fechamento preenchida e dentro da semana
        data_fechamento = _parse_date_safe(row.get("DATA DE FECHAMENTO DA VAGA"))
        if data_fechamento is None:
            continue
        if not (week_start <= data_fechamento <= today):
            continue

        count += 1

    return count


def calcular_vagas_mes(records: list[dict], nome_planilha: str) -> int:
    """
    Conta vagas fechadas no mês atual (do dia 1 até hoje) para um recrutador.
    Mesmos filtros de calcular_vagas_semana, exceto pelo período.
    """
    hoje = date.today()
    mes_inicio = hoje.replace(day=1)

    col_tipo = next(
        (k for k in (records[0].keys() if records else [])
         if "TIPO" in k.upper() and "SOLIC" in k.upper()),
        "TIPO DE SOLICITAÇÃO RECEBIDA",
    )

    count = 0
    for row in records:
        tipo = (row.get(col_tipo) or "").strip().upper()
        if tipo != "R&S":
            continue
        nome_completo = (row.get("NOME COMPLETO") or "").strip()
        if not nome_completo:
            continue
        consultor = (row.get("CONSULTOR DE R&S") or "").strip().upper()
        if consultor != nome_planilha.strip().upper():
            continue
        data_fechamento = _parse_date_safe(row.get("DATA DE FECHAMENTO DA VAGA"))
        if data_fechamento is None:
            continue
        if not (mes_inicio <= data_fechamento <= hoje):
            continue
        count += 1

    return count


def calcular_resumo_mes(records: list[dict], recrutadores: list[dict]) -> list[dict]:
    """
    Retorna lista com vagas do mês de todos os recrutadores, ordenada decrescente.
    Cada item: {'primeiro_nome': str, 'vagas_mes': int}
    """
    resultado = []
    for rec in recrutadores:
        vagas = calcular_vagas_mes(records, rec["nome_planilha"])
        resultado.append({
            "primeiro_nome": rec["primeiro_nome"],
            "vagas_mes": vagas,
        })
    return sorted(resultado, key=lambda x: x["vagas_mes"], reverse=True)


def calcular_percentual(vagas: int, meta: int) -> float:
    """Retorna percentual da meta como float (0.0–1.0+)."""
    if meta <= 0:
        return 0.0
    return vagas / meta


def get_tipo_mensagem(
    vagas: int,
    meta: int,
    threshold_elogio: float,
    threshold_top: float,
) -> str:
    """
    Retorna o tipo de mensagem com base na performance.

    Returns:
        'elogio_top'  — bateu ou superou a meta (>= threshold_top)
        'elogio'      — quase bateu (>= threshold_elogio e < threshold_top)
        'motivacao'   — abaixo do threshold de elogio
    """
    pct = calcular_percentual(vagas, meta)
    if pct >= threshold_top:
        return "elogio_top"
    if pct >= threshold_elogio:
        return "elogio"
    return "motivacao"


def calcular_vagas_semana_passada(records: list[dict], nome_planilha: str) -> int:
    """Conta vagas fechadas na semana anterior (segunda a domingo passados)."""
    hoje = date.today()
    last_monday = hoje - timedelta(days=hoje.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)

    col_tipo = next(
        (k for k in (records[0].keys() if records else [])
         if "TIPO" in k.upper() and "SOLIC" in k.upper()),
        "TIPO DE SOLICITAÇÃO RECEBIDA",
    )

    count = 0
    for row in records:
        if (row.get(col_tipo) or "").strip().upper() != "R&S":
            continue
        if not (row.get("NOME COMPLETO") or "").strip():
            continue
        if (row.get("CONSULTOR DE R&S") or "").strip().upper() != nome_planilha.strip().upper():
            continue
        data = _parse_date_safe(row.get("DATA DE FECHAMENTO DA VAGA"))
        if data is None or not (last_monday <= data <= last_sunday):
            continue
        count += 1
    return count


def calcular_projecao(vagas_semana: int) -> int:
    """Projeta total de vagas no fim da semana com base na média diária até hoje."""
    weekday = date.today().weekday()  # 0=seg, 4=sex
    dias_uteis_passados = min(weekday + 1, 5)
    if dias_uteis_passados == 0:
        return 0
    media_diaria = vagas_semana / dias_uteis_passados
    return round(media_diaria * 5)


def get_tendencia(vagas_atual: int, vagas_anterior: int) -> str:
    """Retorna 'alta', 'queda' ou 'estavel' comparando com semana passada."""
    diff = vagas_atual - vagas_anterior
    if diff > 0:
        return "alta"
    if diff < 0:
        return "queda"
    return "estavel"


def get_ultima_vaga(records: list[dict], nome_planilha: str) -> dict | None:
    """
    Retorna o cargo e unidade da vaga mais recente fechada na semana atual.
    Retorna None se não houver vagas essa semana.
    """
    hoje = date.today()
    week_start = hoje - timedelta(days=hoje.weekday())

    col_tipo = next(
        (k for k in (records[0].keys() if records else [])
         if "TIPO" in k.upper() and "SOLIC" in k.upper()),
        "TIPO DE SOLICITAÇÃO RECEBIDA",
    )

    candidatas = []
    for row in records:
        if (row.get(col_tipo) or "").strip().upper() != "R&S":
            continue
        if not (row.get("NOME COMPLETO") or "").strip():
            continue
        if (row.get("CONSULTOR DE R&S") or "").strip().upper() != nome_planilha.strip().upper():
            continue
        data = _parse_date_safe(row.get("DATA DE FECHAMENTO DA VAGA"))
        if data is None or not (week_start <= data <= hoje):
            continue
        candidatas.append((data, row))

    if not candidatas:
        return None

    candidatas.sort(key=lambda x: x[0], reverse=True)
    row = candidatas[0][1]

    cargo = (row.get("CARGO") or "").strip().title()
    unidade = (row.get("UNIDADE / SETOR") or "").strip().title()

    return {"cargo": cargo, "unidade": unidade} if cargo else None
