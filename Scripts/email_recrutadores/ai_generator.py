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
    if sexta:
        # Sexta: conclusao da semana util + bom descanso
        # A semana JA ACABOU — nunca diga que ainda da tempo nessa semana
        base = ("E sexta-feira — a semana util acabou. "
                "Faca a conclusao da semana: como foi o desempenho, o que se destacou. "
                "Termine desejando um bom descanso no final de semana e projete energia positiva para a proxima semana. "
                "NAO sugira fechar mais vagas nessa semana. NAO mencione segunda como continuacao desta semana.")
        if tipo == "elogio_top":
            return base + " Tom: muito celebrativo — meta batida, semana excelente."
        if tipo == "elogio":
            return base + f" Tom: positivo — boa semana, quase bateu a meta, proxima semana chega la."
        return base + " Tom: encorajador — semana desafiadora, mas reconheca o esforco e projete melhora."
    else:
        # Quarta: incentivo + ritmo atual + projecao
        # NUNCA mencionar queda, comparacao negativa ou cobranca — so incentivo
        base = ("E quarta-feira — metade da semana. "
                "Foque no momento atual e no que ainda e possivel: use a projecao para mostrar o potencial ate sexta. "
                "Termine com incentivo forte — ainda ha 2 dias uteis. "
                "PROIBIDO: nunca mencione queda de ritmo, comparacao negativa com semana passada, "
                "nem qualquer frase que soe como cobranca ou critica velada. "
                "Se a tendencia for negativa, simplesmente ignore esse dado e foque no presente.")
        if tipo == "elogio_top":
            return base + " Tom: celebrativo e desafiador — meta ja batida na quarta, incentive a ir ainda mais longe."
        if tipo == "elogio":
            faltam_txt = f"Destaque que faltam apenas {faltam} {'vaga' if faltam == 1 else 'vagas'} para bater a meta ate sexta."
            return base + f" Tom: animado e confiante. {faltam_txt}"
        return base + " Tom: motivacional puro — acredite na virada, destaque o que ainda e possivel."


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

    projecao_linha = (
        "" if sexta
        else f"- Projecao para sexta-feira (fim da semana util): {projecao} vagas\n"
    )

    prompt = f"""Voce escreve mensagens de performance para recrutadores da Raiz Educacao.

Tom: caloroso, direto, colega proximo. Portugues BR informal mas profissional. Sem emojis.
Tamanho: exatamente 2 paragrafos curtos (3-4 linhas cada). Sem saudacao, sem assinatura.
IMPORTANTE: "semana" significa apenas dias uteis (segunda a sexta). Nunca mencione sabado, domingo ou fim de semana como dias de trabalho.

Dados:
- Nome: {nome}
- Dia: {dia}
- Vagas fechadas na semana util (seg-sex): {vagas} de {meta} ({percentual}%)
- Semana passada: {vagas_ant} vagas ({tendencia_txt})
{projecao_linha}- {ultima_txt}
- Total no mes: {vagas_mes} vagas
- Tipo: {tipo}

Instrucao: {instrucao}

Mencione naturalmente o dia da semana, as vagas fechadas e{' a ultima vaga especifica.' if ultima_vaga else ' o total do mes.'}
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
