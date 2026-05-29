# Raiz P&C — Sistema de E-mails Semanais para Recrutadores

Sistema automatizado que lê a planilha de controle de vagas da Raíz Educação, calcula a performance semanal de cada recrutador e dispara e-mails personalizados toda quarta e sexta-feira.

---

## Como funciona

```
Google Sheets (Apps Script)
        │
        ▼
  Lê registros da semana
        │
        ▼
  Calcula vagas por recrutador
  + comparativo semana passada
  + projeção de fechamento
  + última vaga fechada
        │
        ▼
  Claude Haiku gera texto personalizado
        │
        ▼
  Gmail SMTP envia e-mail HTML
```

O sistema roda automaticamente via **GitHub Actions** toda quarta às 09h e sexta às 16h (horário de Brasília). Também pode ser disparado manualmente pela aba Actions do repositório.

---

## Tipos de mensagem

| Vagas na semana | Tipo | Assunto |
|---|---|---|
| ≥ 10 (meta batida) | `ELOGIO_TOP` | *"[Nome], META BATIDA! Você é incrível!"* |
| ≥ 7 (quase bateu) | `ELOGIO` | *"[Nome], você tá voando essa semana!"* |
| < 7 (quarta) | `MOTIVACAO` | *"[Nome], a semana ainda não acabou!"* |
| < 7 (sexta) | `MOTIVACAO` | *"[Nome], bom descanso e até segunda!"* |

---

## Inteligência nos e-mails

Cada e-mail é gerado com contexto real do recrutador:

- **Comparativo semanal** — vagas acima ou abaixo da semana passada
- **Projeção** — estimativa de fechamento até sexta com base na média diária
- **Tendência** — alta, queda ou estável em relação à semana anterior
- **Última vaga** — cargo e unidade do fechamento mais recente
- **Texto por IA** — Claude Haiku gera texto único por recrutador por envio
- **Ranking mensal** — tabela com todos os consultores ao final do e-mail

---

## Estrutura do projeto

```
Scripts/email_recrutadores/
├── main.py              # Entry point + CLI (--dry-run, --test, --recrutador)
├── sheets_reader.py     # Leitura via Apps Script Web App
├── performance.py       # Cálculos: semana, mês, projeção, tendência, última vaga
├── email_templates.py   # HTML + pools de mensagens + integração com IA
├── email_sender.py      # Gmail SMTP com imagens CID inline
├── ai_generator.py      # Claude Haiku API via urllib (sem dependências externas)
├── config.json          # Credenciais e configurações (não commitado)
├── requirements.txt     # Sem dependências externas — tudo stdlib Python
├── .gitignore
└── SETUP.md             # Guia completo de configuração

.github/workflows/
└── email_recrutadores.yml   # Cron quarta 09h + sexta 16h + trigger manual
```

---

## Configuração rápida

### 1. Google Sheets — Apps Script

Abra a planilha > **Extensions > Apps Script** e adicione ao final do script existente:

```javascript
const SECRET_TOKEN = "seu_token_secreto_aqui";

function doGet(e) {
  if (e.parameter.token !== SECRET_TOKEN) {
    return ContentService
      .createTextOutput(JSON.stringify({ error: "Unauthorized" }))
      .setMimeType(ContentService.MimeType.JSON);
  }

  const sheet = SpreadsheetApp
    .getActiveSpreadsheet()
    .getSheetByName("CONTROLE DE VAGA 2026");

  const data = sheet.getDataRange().getValues();

  let headerIndex = 0;
  for (let i = 0; i < data.length; i++) {
    if (data[i].some(cell => String(cell).trim() === "STATUS")) {
      headerIndex = i;
      break;
    }
  }

  const headers = data[headerIndex];
  const rows = [];
  for (let i = headerIndex + 1; i < data.length; i++) {
    const row = {};
    for (let j = 0; j < headers.length; j++) {
      row[String(headers[j]).trim()] = data[i][j];
    }
    rows.push(row);
  }

  return ContentService
    .createTextOutput(JSON.stringify(rows))
    .setMimeType(ContentService.MimeType.JSON);
}
```

Deploy > New deployment > Web App > Execute as: Me > Who has access: Anyone.

### 2. Gmail App Password

[myaccount.google.com](https://myaccount.google.com) > Segurança > Verificação em duas etapas > Senhas de app > gerar para "Raiz Emails".

### 3. config.json

```json
{
  "apps_script": {
    "token": "seu_token_secreto"
  },
  "google_sheets": {
    "sheet_name": "CONTROLE DE VAGA 2026"
  },
  "meta_semanal": 10,
  "threshold_elogio": 0.70,
  "threshold_elogio_top": 1.0,
  "gmail": {
    "sender_email": "seugmail@gmail.com",
    "app_password": "xxxx xxxx xxxx xxxx"
  },
  "anthropic": {
    "api_key": "sk-ant-..."
  },
  "recrutadores": [
    {
      "nome_planilha": "NOME COMO NA PLANILHA",
      "primeiro_nome": "Nome",
      "email": "nome@raizeducacao.com.br"
    }
  ]
}
```

### 4. Testar localmente

```bash
# Valida leitura e templates sem enviar
python main.py --dry-run

# Envia todos para um e-mail de teste
python main.py --test seuemail@gmail.com

# Envia apenas para um recrutador
python main.py --recrutador "Nome"
```

---

## GitHub Actions — Secrets necessários

| Secret | Descrição |
|---|---|
| `APPS_SCRIPT_TOKEN` | Token configurado no Apps Script |
| `GMAIL_SENDER` | E-mail Gmail remetente |
| `GMAIL_APP_PASSWORD` | App Password de 16 caracteres |
| `ANTHROPIC_API_KEY` | Chave da API Anthropic (opcional — usa templates se ausente) |

Configure em **Settings > Secrets and variables > Actions**.

---

## Disparo manual

Na aba **Actions** do repositório > **Email Recrutadores** > **Run workflow**:

| Opção | Descrição |
|---|---|
| Dry run | Imprime no log sem enviar e-mail |
| Recrutador | Envia apenas para um nome específico |
| Test email | Redireciona todos os e-mails para um endereço de teste |

---

## Stack

| Componente | Solução |
|---|---|
| Fonte de dados | Google Sheets via Apps Script Web App |
| E-mail | Gmail SMTP com imagens CID inline |
| Inteligência | Claude Haiku (Anthropic API) |
| Agendamento | GitHub Actions (cron) |
| Dependências pip | **Zero** — tudo Python stdlib |
| Linguagem | Python 3.12+ |
