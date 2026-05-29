# Setup — Sistema de E-mails Semanais para Recrutadores

## 1. Instalar dependências (uso local)

```bash
pip install -r requirements.txt
```

---

## 2. Google Cloud — criar Service Account

1. Acesse https://console.cloud.google.com/
2. Crie um novo projeto (ex: "Raiz PC Emails")
3. Ative a API **Google Sheets** em "APIs e Serviços > Biblioteca"
4. Em "APIs e Serviços > Credenciais":
   - Clique em "Criar Credenciais" > **Conta de Serviço**
   - Nome: `raiz-emails` > Criar e continuar > Concluir
5. Clique na conta de serviço criada > aba **Chaves** > Adicionar chave > JSON
6. Salve o arquivo baixado como `service_account.json` nesta pasta

> A Service Account tem um e-mail no formato `nome@projeto.iam.gserviceaccount.com`

---

## 3. Compartilhar a planilha com a Service Account

1. Abra a planilha no Google Sheets
2. Compartilhar > adicionar o e-mail da Service Account como **Visualizador**

---

## 4. Obter ID da planilha

Na URL do Google Sheets:
```
https://docs.google.com/spreadsheets/d/ID_DA_PLANILHA_AQUI/edit
```
Copie o trecho entre `/d/` e `/edit`.

---

## 5. Gmail App Password

1. Acesse https://myaccount.google.com/security
2. Ative **Verificação em duas etapas** (se não estiver ativa)
3. Em "Senhas de app" > gere para "Outro" > "Raiz Emails"
4. Copie a senha de 16 caracteres (formato: `xxxx xxxx xxxx xxxx`)

---

## 6. Preencher config.json

```json
{
  "google_sheets": {
    "spreadsheet_id": "SEU_ID_AQUI",
    "sheet_name": "CONTROLE DE VAGA 2026"
  },
  "meta_semanal": 10,
  "threshold_elogio": {
    "quarta": 0.40,
    "sexta": 0.70
  },
  "gmail": {
    "sender_email": "seuemail@gmail.com",
    "app_password": "xxxx xxxx xxxx xxxx"
  },
  "recrutadores": [
    {
      "nome_planilha": "FULANA DE TAL",
      "primeiro_nome": "Fulana",
      "email": "fulana@raizeducacao.com.br"
    }
  ]
}
```

> **nome_planilha**: exatamente como aparece na coluna `CONSULTOR DE R&S` (caixa alta).

---

## 7. Testar localmente

```bash
# Valida leitura + templates sem enviar e-mail
python main.py --dry-run

# Recebe todos os e-mails em um endereço de teste
python main.py --test seuemail@gmail.com

# Envia apenas para um recrutador
python main.py --recrutador "Nome"
```

---

## 8. Deploy no GitHub Actions

### 8.1 Criar repositório privado no GitHub

Suba a pasta do projeto (sem `service_account.json` — está no `.gitignore`).

### 8.2 Adicionar Secrets no GitHub

No repositório: **Settings > Secrets and variables > Actions > New repository secret**

| Secret | Valor |
|--------|-------|
| `SERVICE_ACCOUNT_JSON` | Conteúdo completo do `service_account.json` (copie e cole o JSON inteiro) |
| `SPREADSHEET_ID` | ID da planilha |
| `GMAIL_SENDER` | E-mail remetente |
| `GMAIL_APP_PASSWORD` | Senha de app do Gmail |

### 8.3 Agendamento automático

O workflow `.github/workflows/email_recrutadores.yml` já configura:

| Dia | Horário (BRT) | Cron (UTC) |
|-----|---------------|------------|
| Quarta-feira | 09:00 | `0 12 * * 3` |
| Sexta-feira | 16:00 | `0 19 * * 5` |

### 8.4 Disparo manual (via GitHub web)

1. Acesse o repositório no GitHub
2. Aba **Actions** > **Email Recrutadores** > **Run workflow**
3. Opções disponíveis:
   - **Dry run** — imprime sem enviar
   - **Recrutador** — envia apenas para um nome específico
   - **Test email** — redireciona todos para um e-mail de teste

---

## 9. Migração de conta

Quando a conta atual for deletada:
1. Transferir propriedade da planilha para nova conta
2. Criar nova Service Account no Google Cloud (na nova conta)
3. Compartilhar planilha com e-mail da nova Service Account
4. Atualizar secrets no GitHub (`SERVICE_ACCOUNT_JSON`, `GMAIL_SENDER`, `GMAIL_APP_PASSWORD`)
5. O código não muda nada

---

## 10. Estrutura dos arquivos

```
Scripts/email_recrutadores/
├── main.py                  # Entry point
├── sheets_reader.py         # Google Sheets (Service Account)
├── performance.py           # Cálculo semanal
├── email_templates.py       # Templates HTML com imagens base64
├── email_sender.py          # Gmail SMTP
├── config.json              # Configurações (sem senhas no repo)
├── service_account.json     # ← você coloca aqui (não commitado)
├── requirements.txt         # gspread, google-auth
├── .gitignore               # Ignora service_account.json
└── SETUP.md                 # Este arquivo

.github/workflows/
└── email_recrutadores.yml   # GitHub Actions (cron + manual)
```
