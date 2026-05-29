"""
ai_generator.py — Gera texto personalizado para e-mails via Claude API (urllib, sem deps).

Usa claude-haiku-4-5-20251001 para custo baixo e resposta rápida.
Se a API key não estiver configurada ou ocorrer erro, retorna None (usa fallback).
"""

import json
import urllib.request
import urllib.error

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-4-5-20251001"


def _instrucao_tipo(tipo: str, sexta: bool, faltam: int) -> str:
    if tipo == "elogio_top":
        return "Celebre com entusiasmo o feito de bater ou superar a meta. Seja caloroso e genuíno."
    if tipo == "elogio":
        faltam_txt = f"Mencione que faltam {faltam} {'vaga' if faltam == 1 else 'vagas'} para bater a meta e que dá tempo."
        return f"Elogie a boa performance. {faltam_txt}"
    if sexta:
        return "É sexta-feira. Parabenize pela semana, deseje bom descanso e projete uma semana ainda melhor."
    return "É quarta-feira. Motive para os próximos dias. Destaque que ainda há tempo para virar o jogo."


def gerar_texto(api_key: str, contexto: dict) -> str | None:
    """
    Gera corpo do e-mail personalizado via Claude API.

    Args:
        api_key: Chave da API Anthropic (sk-ant-...).
        contexto: Dict com dados do recrutador (veja main.py).

    Returns:
        Texto gerado (2 parágrafos) ou None se falhar.
    """
    if not api_key or api_key.startswith("sk-ant-COLE"):
        return None

    nome         = contexto["primeiro_nome"]
    vagas        = contexto["vagas"]
    meta         = contexto["meta"]
    percentual   = contexto["percentual"]
    dia          = contexto["dia_semana"]
    vagas_ant    = contexto.get("vagas_semana_passada", 0)
    tendencia    = contexto.get("tendencia", "estavel")
    projecao     = contexto.get("projecao", vagas)
    ultima_vaga  = contexto.get("ultima_vaga")
    vagas_mes    = contexto.get("vagas_mes", 0)
    tipo         = contexto["tipo"]
    sexta        = contexto.get("sexta", False)
    faltam       = max(0, meta - vagas)

    tendencia_txt = {
        "alta":   f"{vagas - vagas_ant} vagas a mais que na semana passada — em alta!",
        "queda":  f"{vagas_ant - vagas} vagas a menos que na semana passada.",
        "estavel": "mesmo ritmo da semana passada.",
    }.get(tendencia, "")

    ultima_txt = (
        f"A última vaga fechada foi: {ultima_vaga['cargo']}"
        + (f" na unidade {ultima_vaga['unidade']}" if ultima_vaga.get("unidade") else "")
        + "."
        if ultima_vaga else ""
    )

    instrucao = _instrucao_tipo(tipo, sexta, faltam)

    prompt = f"""Você escreve mensagens de performance para recrutadores da Raíz Educação.

Tom: caloroso, direto, colega próximo. Português BR informal mas profissional. Sem emojis.
Tamanho: exatamente 2 parágrafos curtos (3-4 linhas cada). Sem saudação, sem assinatura.

Dados:
- Nome: {nome}
- Dia: {dia}
- Vagas na semana: {vagas} de {meta} ({percentual}%)
- Semana passada: {vagas_ant} vagas ({tendencia_txt})
- Projeção fim da semana: {projecao} vagas
- {ultima_txt}
- Total no mês: {vagas_mes} vagas
- Tipo: {tipo}

Instrução: {instrucao}

Mencione naturalmente o dia da semana, as vagas fechadas e{' a última vaga específica.' if ultima_vaga else ' o total do mês.'}
Escreva apenas o corpo do e-mail:"""

    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        CLAUDE_API_URL,
        data=payload,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result["content"][0]["text"].strip()
    except Exception:
        return None
