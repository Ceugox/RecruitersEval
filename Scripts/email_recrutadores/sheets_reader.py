"""
sheets_reader.py — Lê dados do Google Sheets via Apps Script Web App.

Não requer Google Cloud Console nem credenciais OAuth.
A segurança é feita por token secreto passado como parâmetro.
"""

import json
import urllib.request
import urllib.parse


APPS_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbyGsUDUmCJXklxcW9dJqQVYzciJInd6Wpy5KZ56odS55_UYYn2vtgla37WH_l-5flP7"
    "/exec"
)


def read_sheet(token: str) -> list[dict]:
    """
    Chama o Apps Script Web App e retorna lista de dicts com os dados da planilha.

    Args:
        token: Token secreto configurado no Apps Script.

    Returns:
        Lista de dicts — cada item é uma linha da planilha.

    Raises:
        urllib.error.HTTPError: Se a URL estiver inacessível.
        ValueError: Se o token estiver errado ou a resposta for inesperada.
    """
    url = f"{APPS_SCRIPT_URL}?token={urllib.parse.quote(token)}"

    with urllib.request.urlopen(url, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    if isinstance(data, dict) and data.get("error"):
        raise ValueError(f"Apps Script retornou erro: {data['error']}")

    return data
