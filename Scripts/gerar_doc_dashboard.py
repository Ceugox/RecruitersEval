"""
Gera documentação HTML do Dashboard Métricas P&C.
Execução: python gerar_doc_dashboard.py
Saída: Documentação/dashboard_regras_negocio.html
"""

from pathlib import Path

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Dashboard Métricas P&C — Regras de Negócio</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #f4f6f9; color: #1a1a2e; }
  header { background: #1a1a2e; color: #fff; padding: 32px 48px; }
  header h1 { font-size: 1.8rem; }
  header p { opacity: .7; margin-top: 6px; font-size: .9rem; }
  nav { background: #fff; border-bottom: 1px solid #e0e0e0; padding: 0 48px; display: flex; gap: 4px; overflow-x: auto; }
  nav a { display: block; padding: 14px 16px; text-decoration: none; color: #555; font-size: .85rem; white-space: nowrap; border-bottom: 3px solid transparent; }
  nav a:hover, nav a.active { color: #1a1a2e; border-color: #e74c3c; font-weight: 600; }
  main { max-width: 1100px; margin: 32px auto; padding: 0 24px; }
  .page { display: none; }
  .page.active { display: block; }
  .section-title { font-size: 1.4rem; font-weight: 700; margin-bottom: 24px; border-left: 4px solid #e74c3c; padding-left: 14px; }
  .filters-bar { background: #fff; border-radius: 8px; padding: 16px 20px; margin-bottom: 24px; border: 1px solid #e8e8e8; }
  .filters-bar h3 { font-size: .8rem; text-transform: uppercase; letter-spacing: .05em; color: #888; margin-bottom: 10px; }
  .filter-pill { display: inline-block; background: #eef2ff; color: #3730a3; border-radius: 20px; padding: 4px 12px; font-size: .8rem; margin: 3px; }
  .cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
  .card { background: #fff; border-radius: 8px; border: 1px solid #e8e8e8; overflow: hidden; }
  .card-header { padding: 14px 18px; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #f0f0f0; }
  .badge { font-size: .7rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; white-space: nowrap; }
  .badge-card { background: #dbeafe; color: #1e40af; }
  .badge-bar { background: #d1fae5; color: #065f46; }
  .badge-line { background: #fce7f3; color: #9d174d; }
  .badge-column { background: #fef3c7; color: #92400e; }
  .badge-combo { background: #ede9fe; color: #5b21b6; }
  .badge-table { background: #f3f4f6; color: #374151; }
  .badge-kpi { background: #fff7ed; color: #c2410c; }
  .badge-pivot { background: #ecfdf5; color: #065f46; }
  .badge-slicer { background: #f0fdf4; color: #166534; }
  .card-title { font-weight: 600; font-size: .9rem; }
  .card-body { padding: 14px 18px; font-size: .85rem; line-height: 1.6; }
  .card-body ul { padding-left: 18px; }
  .card-body li { margin-bottom: 4px; }
  .metric-row { display: flex; flex-direction: column; gap: 8px; }
  .metric { background: #fafafa; border-radius: 6px; padding: 8px 12px; border: 1px solid #f0f0f0; }
  .metric-name { font-weight: 600; font-size: .8rem; color: #374151; }
  .metric-desc { font-size: .78rem; color: #6b7280; margin-top: 2px; }
  .metric-rule { font-size: .78rem; color: #1a1a2e; margin-top: 4px; background: #f0f4ff; border-radius: 4px; padding: 4px 8px; }
  .note { background: #fffbeb; border-left: 3px solid #f59e0b; padding: 10px 14px; border-radius: 0 6px 6px 0; font-size: .82rem; margin-top: 16px; }
  .note.danger { background: #fef2f2; border-color: #ef4444; }
  .note.info { background: #eff6ff; border-color: #3b82f6; }
  .rel-table { width: 100%; border-collapse: collapse; font-size: .82rem; margin-top: 12px; }
  .rel-table th { background: #1a1a2e; color: #fff; padding: 8px 12px; text-align: left; }
  .rel-table td { padding: 8px 12px; border-bottom: 1px solid #e8e8e8; }
  .rel-table tr:nth-child(even) td { background: #fafafa; }
  .status-active { color: #16a34a; font-weight: 700; }
  .status-inactive { color: #9ca3af; }
  @media print { nav { display: none; } .page { display: block !important; page-break-after: always; } }
</style>
</head>
<body>

<header>
  <h1>Dashboard Métricas P&C</h1>
  <p>Raíz Educação · Documentação de Regras de Negócio · Gerado automaticamente</p>
</header>

<nav id="nav">
  <a href="#" class="active" onclick="show('pg-modelo',this)">Modelo de Dados</a>
  <a href="#" onclick="show('pg-geral',this)">Geral</a>
  <a href="#" onclick="show('pg-performance',this)">Performance</a>
  <a href="#" onclick="show('pg-qualidade',this)">Qualidade SLA</a>
  <a href="#" onclick="show('pg-recrutadores',this)">Recrutadores</a>
  <a href="#" onclick="show('pg-consulta',this)">Consulta</a>
  <a href="#" onclick="show('pg-extracao',this)">Extração de Bases</a>
  <a href="#" onclick="show('pg-historico',this)">Perf. Histórica</a>
</nav>

<main>

<!-- ==================== MODELO ==================== -->
<div class="page active" id="pg-modelo">
  <h2 class="section-title">Modelo de Dados</h2>

  <div class="card" style="margin-bottom:20px">
    <div class="card-header"><span class="card-title">Tabelas principais</span></div>
    <div class="card-body">
      <table class="rel-table">
        <tr><th>Tabela</th><th>Tipo</th><th>Colunas</th><th>Medidas</th><th>Descrição</th></tr>
        <tr><td><b>Fonte_Sheets</b></td><td>Fato</td><td>63</td><td>—</td><td>Origem Google Sheets — dados brutos de vagas</td></tr>
        <tr><td><b>R&S_CONTROLE DE VAGAS 2026</b></td><td>Medidas</td><td>2</td><td>92</td><td>Todas as métricas calculadas do dashboard</td></tr>
        <tr><td><b>dCalendario</b></td><td>Dim. Data</td><td>11</td><td>—</td><td>Dimensão de datas para filtros de período</td></tr>
        <tr><td><b>Marcas</b></td><td>Dimensão</td><td>2</td><td>—</td><td>Lista de marcas para filtro</td></tr>
        <tr><td><b>Status Prazo</b></td><td>Auxiliar</td><td>2</td><td>—</td><td>Tabela de apoio para gráficos de prazo</td></tr>
        <tr><td><b>R&S 2026</b></td><td>Suporte</td><td>76</td><td>—</td><td>Base auxiliar de vagas 2026</td></tr>
      </table>
    </div>
  </div>

  <div class="card" style="margin-bottom:20px">
    <div class="card-header"><span class="card-title">Relacionamentos com dCalendario</span></div>
    <div class="card-body">
      <table class="rel-table">
        <tr><th>Tabela</th><th>Coluna</th><th>Status</th><th>Impacto</th></tr>
        <tr><td>Fonte_Sheets</td><td>DATA DE FECHAMENTO DA VAGA</td><td class="status-active">✅ Ativo</td><td>Filtro de período padrão usa data de fechamento</td></tr>
        <tr><td>Fonte_Sheets</td><td>DATA DE ABERTURA DA VAGA</td><td class="status-inactive">❌ Inativo</td><td>Precisa de USERELATIONSHIP para ser ativado</td></tr>
        <tr><td>Fonte_Sheets</td><td>DATA DE INTEGRAÇÃO NA GUPY</td><td class="status-inactive">❌ Inativo</td><td>Precisa de USERELATIONSHIP para ser ativado</td></tr>
      </table>
      <div class="note danger" style="margin-top:12px">
        <b>Atenção:</b> Medidas que não usam <code>USERELATIONSHIP</code> filtram automaticamente por <b>DATA DE FECHAMENTO</b>.
        Medidas de "vagas abertas" usam <code>REMOVEFILTERS(dCalendario)</code> + lógica própria para não depender dessa relação.
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-header"><span class="card-title">Pastas de medidas (92 medidas)</span></div>
    <div class="card-body">
      <table class="rel-table">
        <tr><th>Pasta</th><th>O que contém</th></tr>
        <tr><td>Vagas Fechadas</td><td>Totais fechados, MTD, WTD, componentes R&S e Admissão</td></tr>
        <tr><td>Vagas Abertas</td><td>Estoque atual, acumulado de período, variações MoM/WoW</td></tr>
        <tr><td>SLA</td><td>Médias de SLA R&S, ADM e Total; versões período anterior</td></tr>
        <tr><td>Pipeline & Status</td><td>Vagas em admissão, congeladas, pipeline total, entrega de docs, Gupy</td></tr>
        <tr><td>Qualidade & Eficiência</td><td>Taxa cancelamento, SLA cumprido, aging, vagas críticas, insights</td></tr>
        <tr><td>Produtividade</td><td>Rank semana, projeção mês, atingimento de meta, semáforo</td></tr>
        <tr><td>Recrutadores</td><td>Rankings, médias mensais, mês atual/anterior por consultor</td></tr>
        <tr><td>Auxiliares</td><td>Dias úteis, medidas de diagnóstico internas</td></tr>
      </table>
    </div>
  </div>
</div>

<!-- ==================== GERAL ==================== -->
<div class="page" id="pg-geral">
  <h2 class="section-title">Aba — Geral</h2>
  <p style="margin-bottom:20px;color:#555;font-size:.9rem">Visão macro das operações de P&C: volume de tickets, vagas fechadas, SLA e distribuição de vagas abertas por cargo e marca.</p>

  <div class="filters-bar">
    <h3>Filtros disponíveis</h3>
    <span class="filter-pill">📅 Período (Ano / Mês)</span>
    <span class="filter-pill">🏷️ Marca</span>
    <span class="filter-pill">💼 Grupo de Cargo</span>
  </div>

  <div class="cards">

    <div class="card">
      <div class="card-header">
        <span class="badge badge-column">Coluna</span>
        <span class="card-title">Tickets Diários por Tipo</span>
      </div>
      <div class="card-body">
        <p>Volume de tickets por dia, segmentado por <b>TIPO de solicitação</b> (R&S, Admissão etc.).</p>
        <div class="metric-row" style="margin-top:10px">
          <div class="metric">
            <div class="metric-name">Eixo X</div>
            <div class="metric-desc">Hierarquia de datas: Ano › Mês › Dia</div>
          </div>
          <div class="metric">
            <div class="metric-name">Eixo Y</div>
            <div class="metric-desc">CountNonNull(TICKET)</div>
          </div>
          <div class="metric">
            <div class="metric-name">Série (legenda)</div>
            <div class="metric-desc">Fonte_Sheets[TIPO]</div>
          </div>
        </div>
        <div class="note info" style="margin-top:10px">
          Filtro de período limita os dias exibidos no eixo X. A contagem usa a relação ativa (DATA DE FECHAMENTO).
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-card">Card</span>
        <span class="card-title">Vagas Fechadas (MTD) — R&S / ADM</span>
      </div>
      <div class="card-body">
        <div class="metric-row">
          <div class="metric">
            <div class="metric-name">VagasFechadas_Total</div>
            <div class="metric-desc">R&S fechadas + Admissões fechadas no período</div>
            <div class="metric-rule">
              R&S: STATUS ≠ CANCELADA/DESISTENTE + DATA FECHAMENTO preenchida + NOME COMPLETO preenchido<br>
              ADM: STATUS = FECHADA + DATA FECHAMENTO preenchida + RESPONSÁVEL PELA ADMISSÃO preenchido
            </div>
          </div>
          <div class="metric">
            <div class="metric-name">VagasFechadas_Total_MTD_Mês_Anterior</div>
            <div class="metric-desc">Mesmo total, deslocado -1 mês via DATEADD</div>
          </div>
          <div class="metric">
            <div class="metric-name">MoM_MTD_VagasFechadas_%</div>
            <div class="metric-desc">(MTD atual − MTD anterior) ÷ MTD anterior</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-card">Card</span>
        <span class="card-title">SLA</span>
      </div>
      <div class="card-body">
        <div class="metric-row">
          <div class="metric">
            <div class="metric-name">SLA_R&S_Médio</div>
            <div class="metric-desc">AVERAGE(Fonte_Sheets[SLA R&S])</div>
            <div class="metric-rule">Dias médios do ticket até o fechamento R&S. Filtrado pelo período via relação ativa (DATA DE FECHAMENTO).</div>
          </div>
          <div class="metric">
            <div class="metric-name">SLA_ADM_Médio</div>
            <div class="metric-desc">AVERAGE(Fonte_Sheets[SLA ADM])</div>
          </div>
          <div class="metric">
            <div class="metric-name">SLA_Total</div>
            <div class="metric-desc">AVERAGE(Fonte_Sheets[SLA TOTAL]) — soma R&S + ADM</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-bar">Barra</span>
        <span class="card-title">Vagas Abertas por Cargo</span>
      </div>
      <div class="card-body">
        <p>Medida: <b>Vagas_Abertas_Acumulado_Periodo</b></p>
        <div class="metric-row" style="margin-top:8px">
          <div class="metric">
            <div class="metric-name">Critério "vaga aberta no período"</div>
            <div class="metric-rule">
              DATA DE ABERTURA ≤ último dia do período<br>
              AND (DATA DE FECHAMENTO ≥ primeiro dia do período OR sem fechamento)<br>
              AND se sem fechamento: STATUS ∉ {CANCELADA, DESISTENTE, CONGELADA, FECHADA}
            </div>
          </div>
        </div>
        <div class="note info" style="margin-top:10px">
          Usa <code>MIN/MAX(dCalendario[Date])</code> como janela e <code>REMOVEFILTERS(dCalendario)</code> internamente.
          Mede <b>estoque ativo no período</b>, não vagas que fecharam.
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-bar">Barra</span>
        <span class="card-title">Vagas Abertas por Marca</span>
      </div>
      <div class="card-body">
        <p>Mesma medida <b>Vagas_Abertas_Acumulado_Periodo</b>, agrupada por <code>Fonte_Sheets[MARCA]</code>.</p>
        <p style="margin-top:8px;color:#555">Tem filtro visual sobre <code>dCalendario[Date]</code> (início/fim do ano corrente).</p>
      </div>
    </div>

  </div>
</div>

<!-- ==================== PERFORMANCE ==================== -->
<div class="page" id="pg-performance">
  <h2 class="section-title">Aba — Performance</h2>
  <p style="margin-bottom:20px;color:#555;font-size:.9rem">Acompanhamento de fechamentos R&S: cards MTD/WTD, ranking semanal por consultor, gráficos de evolução mensal e diária.</p>

  <div class="filters-bar">
    <h3>Filtros disponíveis</h3>
    <span class="filter-pill">🏷️ Marca</span>
  </div>

  <div class="cards">

    <div class="card">
      <div class="card-header">
        <span class="badge badge-card">Card</span>
        <span class="card-title">Vagas Fechadas R&S</span>
      </div>
      <div class="card-body">
        <div class="metric-row">
          <div class="metric">
            <div class="metric-name">VagasFechadasR&S Mês Atual (MTD)</div>
            <div class="metric-desc">Fechamentos R&S acumulados no mês corrente até hoje</div>
          </div>
          <div class="metric">
            <div class="metric-name">MoM VagasFechadasR&S %</div>
            <div class="metric-desc">Variação % do MTD atual vs MTD do mês anterior</div>
          </div>
          <div class="metric">
            <div class="metric-name">VagasFechadas Semana Atual (WTD)</div>
            <div class="metric-desc">Fechamentos R&S da semana corrente (Week To Date)</div>
          </div>
          <div class="metric">
            <div class="metric-name">WoW VagasFechadas %</div>
            <div class="metric-desc">Variação % WTD atual vs semana anterior</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-card">Card</span>
        <span class="card-title">Vagas Abertas</span>
      </div>
      <div class="card-body">
        <div class="metric-row">
          <div class="metric">
            <div class="metric-name">Vagas_Abertas</div>
            <div class="metric-desc">Estoque de vagas abertas hoje (sem data de fechamento, status ativo)</div>
          </div>
          <div class="metric">
            <div class="metric-name">Vagas_Abertas_MoM_%_Card</div>
            <div class="metric-desc">Variação % do estoque vs fim do mês anterior</div>
          </div>
          <div class="metric">
            <div class="metric-name">VagasAbertas Semana Atual</div>
            <div class="metric-desc">Estoque de vagas abertas ao final da semana atual</div>
          </div>
          <div class="metric">
            <div class="metric-name">Vagas_Abertas_WoW_%_Card</div>
            <div class="metric-desc">Variação % do estoque vs semana anterior</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card" style="grid-column: span 2">
      <div class="card-header">
        <span class="badge badge-table">Tabela</span>
        <span class="card-title">Ranking Semanal</span>
      </div>
      <div class="card-body">
        <p>Ranking de consultores de R&S pela performance da semana e do mês.</p>
        <table class="rel-table" style="margin-top:10px">
          <tr><th>Coluna</th><th>Regra</th></tr>
          <tr><td>Rank Especialista Ajustado</td><td>Ranking por fechamentos WTD, desempate por MTD</td></tr>
          <tr><td>WTD (Semana Atual)</td><td>VagasFechadas R&S da semana corrente por consultor</td></tr>
          <tr><td>MTD (Mês Atual)</td><td>VagasFechadas R&S do mês corrente por consultor</td></tr>
          <tr><td>Total</td><td>VagasFechadas_Total (inclui ADM)</td></tr>
          <tr><td>% Acumulado</td><td>Share do consultor sobre o total de fechamentos do período</td></tr>
          <tr><td>SLA R&S / ADM</td><td>Média de SLA filtrada pelo consultor selecionado</td></tr>
        </table>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-combo">Combo</span>
        <span class="card-title">Vagas Fechadas × Mês (R&S)</span>
      </div>
      <div class="card-body">
        <p>Eixo X: Meses do dCalendario · Eixo Y: <b>VagasFechadaR&S</b> por mês.</p>
        <p style="margin-top:6px;color:#555">Permite visualizar sazonalidade e tendência de fechamentos ao longo do ano.</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-combo">Combo</span>
        <span class="card-title">Vagas Fechadas × Dia (R&S)</span>
      </div>
      <div class="card-body">
        <p>Eixo X: Dias do mês · Eixo Y: <b>VagasFechadaR&S</b> por dia.</p>
        <p style="margin-top:6px;color:#555">Identifica padrões intra-mensais (picos no fim de mês, baixa performance em datas específicas).</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-pivot">Pivot</span>
        <span class="card-title">Recrutamentos por Recrutador</span>
      </div>
      <div class="card-body">
        <p>Linhas: <b>CONSULTOR DE R&S</b> · Colunas: <b>Mês</b> · Valores: <b>VagasFechadaR&S</b>.</p>
        <p style="margin-top:6px;color:#555">Visão matricial para comparação histórica de produtividade individual por mês.</p>
      </div>
    </div>

  </div>
</div>

<!-- ==================== QUALIDADE SLA ==================== -->
<div class="page" id="pg-qualidade">
  <h2 class="section-title">Aba — Qualidade SLA</h2>
  <p style="margin-bottom:20px;color:#555;font-size:.9rem">Monitora saúde do pipeline: aging de vagas abertas, evolução histórica do SLA e lista de vagas críticas.</p>

  <div class="filters-bar">
    <h3>Filtros disponíveis</h3>
    <span class="filter-pill">🏷️ Marca</span>
  </div>

  <div class="cards">

    <div class="card">
      <div class="card-header">
        <span class="badge badge-column">Coluna</span>
        <span class="card-title">Aging Vagas Abertas</span>
      </div>
      <div class="card-body">
        <p>Medida: <b>Vagas_Aging_Distribuicao</b> · Eixo X: <b>Faixa Aging</b></p>
        <div class="metric-row" style="margin-top:10px">
          <div class="metric">
            <div class="metric-name">Faixas de Aging</div>
            <div class="metric-rule">
              0–7 dias → pipeline jovem (saudável)<br>
              8–15 dias → zona de atenção moderada<br>
              16–30 dias → zona de risco<br>
              +30 dias → crítico (alerta acima de 20% do total)
            </div>
          </div>
        </div>
        <div class="note info" style="margin-top:10px">
          Usa <code>KEEPFILTERS</code> para preservar o contexto de faixa e <code>REMOVEFILTERS(dCalendario)</code>
          para não cortar vagas com abertura em meses anteriores.
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-line">Linha</span>
        <span class="card-title">SLA Aging Histórico</span>
      </div>
      <div class="card-body">
        <div class="metric-row">
          <div class="metric">
            <div class="metric-name">Aging_Médio_Hist_RS</div>
            <div class="metric-desc">Média de dias (SLA R&S) das vagas R&S fechadas no período — linha de evolução mensal</div>
          </div>
          <div class="metric">
            <div class="metric-name">Aging_Médio_Hist_ADM</div>
            <div class="metric-desc">Média de dias (SLA ADM) das vagas Admissão fechadas no período</div>
          </div>
        </div>
        <p style="margin-top:8px;color:#555;font-size:.8rem">Eixo X: Ano › Mês. Permite acompanhar se o processo está acelerando ou lentificando ao longo do tempo.</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-card">Card</span>
        <span class="card-title">Insight SLA (IA)</span>
      </div>
      <div class="card-body">
        <p>Texto gerado dinamicamente pela medida <b>Insight_SLA</b> (DAX com lógica de cenário).</p>
        <p style="margin-top:6px;color:#555">Interpreta o SLA atual e retorna uma frase contextual de diagnóstico. Controlado por <code>Insight_SLA_Cenario</code>, <code>Insight_SLA_Titulo</code> e <code>Insight_SLA_Cor</code>.</p>
      </div>
    </div>

    <div class="card" style="grid-column: span 2">
      <div class="card-header">
        <span class="badge badge-table">Tabela</span>
        <span class="card-title">Vagas Críticas</span>
      </div>
      <div class="card-body">
        <p>Lista detalhada de vagas abertas há mais de 30 dias. Colunas exibidas:</p>
        <p style="margin-top:8px">STATUS · TICKET · NÍVEL · CARGO · MARCA · CONSULTOR DE R&S · GESTOR DA VAGA · REMUNERAÇÃO · Aging Dias · Faixa Aging</p>
        <div class="note danger" style="margin-top:10px">
          <b>Critério de alerta:</b> Vagas com <code>DATA DE ABERTURA</code> preenchida e mais de 30 dias sem fechamento.
          Vagas sem DATA DE ABERTURA são excluídas para evitar falsos positivos (TODAY() − BLANK = TRUE em DAX).
        </div>
      </div>
    </div>

  </div>
</div>

<!-- ==================== RECRUTADORES ==================== -->
<div class="page" id="pg-recrutadores">
  <h2 class="section-title">Aba — Recrutadores</h2>
  <p style="margin-bottom:20px;color:#555;font-size:.9rem">Ranking e performance individual dos consultores. Janela de comparação: últimos 3 meses completos + mês atual (MTD).</p>

  <div class="filters-bar">
    <h3>Filtros disponíveis</h3>
    <span class="filter-pill">🏷️ Marca</span>
    <span class="filter-pill">💼 Grupo de Cargo</span>
  </div>

  <div class="cards">

    <div class="card">
      <div class="card-header">
        <span class="badge badge-kpi">KPI</span>
        <span class="card-title">Fechamento de Vagas R&S (M-1)</span>
      </div>
      <div class="card-body">
        <div class="metric-row">
          <div class="metric">
            <div class="metric-name">Rec_RS_MediaMensal (valor)</div>
            <div class="metric-desc">Média de fechamentos R&S por mês ativo nos últimos 3M completos</div>
            <div class="metric-rule">Janela fixa: últimos 3 meses completos (ex: fev–abr quando hoje é maio). Denominador = meses com ao menos 1 fechamento — torna justa a comparação entre consultores novos e veteranos.</div>
          </div>
          <div class="metric">
            <div class="metric-name">Rec_RS_MesAnterior (meta/referência)</div>
            <div class="metric-desc">Total de fechamentos R&S do mês anterior completo — referência de comparação</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-kpi">KPI</span>
        <span class="card-title">Admissões Realizadas (M-1)</span>
      </div>
      <div class="card-body">
        <div class="metric-row">
          <div class="metric">
            <div class="metric-name">Rec_ADM_MediaMensal</div>
            <div class="metric-desc">Média de fechamentos ADM por mês ativo nos últimos 3M. Critério: DATA DE INICIO PREVISTA no período.</div>
          </div>
          <div class="metric">
            <div class="metric-name">Rec_ADM_MesAnterior</div>
            <div class="metric-desc">Total ADM do mês anterior completo</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-kpi">KPI</span>
        <span class="card-title">Fechamento de Vagas R&S — Mês Atual</span>
      </div>
      <div class="card-body">
        <div class="metric-row">
          <div class="metric">
            <div class="metric-name">Rec_RS_MesAtual (valor)</div>
            <div class="metric-desc">R&S fechados no mês atual (MTD) por consultor</div>
          </div>
          <div class="metric">
            <div class="metric-name">Rec_RS_MesAnterior (referência)</div>
            <div class="metric-desc">Base de comparação: mês anterior completo</div>
          </div>
          <div class="metric">
            <div class="metric-name">Rec_RS_MoM_%</div>
            <div class="metric-desc">Variação % mês atual vs anterior. Retorna BLANK nos primeiros 7 dias do mês (evita -100% enganoso).</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-kpi">KPI</span>
        <span class="card-title">Admissões Realizadas — Mês Atual</span>
      </div>
      <div class="card-body">
        <div class="metric-row">
          <div class="metric">
            <div class="metric-name">Rec_ADM_MesAtual</div>
            <div class="metric-desc">ADM com DATA DE INICIO PREVISTA no mês atual (MTD)</div>
          </div>
          <div class="metric">
            <div class="metric-name">Rec_ADM_MoM_%</div>
            <div class="metric-desc">Variação % mês atual vs anterior. BLANK nos primeiros 7 dias.</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-bar">Barra</span>
        <span class="card-title">Ranking R&S — Média Mensal (3M)</span>
      </div>
      <div class="card-body">
        <p>Eixo Y: <b>CONSULTOR DE R&S</b> · Valor: <b>Rec_RS_MediaMensal</b></p>
        <p style="margin-top:6px;color:#555">Ordenado pela média mensal dos últimos 3 meses completos. Ranking justo independente de tempo de casa.</p>
        <div class="note info" style="margin-top:10px">Consultores sem nenhum fechamento R&S na janela de 3M retornam BLANK e não aparecem no ranking.</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-bar">Barra</span>
        <span class="card-title">Ranking ADM — Média Mensal (3M)</span>
      </div>
      <div class="card-body">
        <p>Eixo Y: <b>RESPONSÁVEL PELA ADMISSÃO</b> · Valor: <b>Rec_ADM_MediaMensal</b></p>
        <p style="margin-top:6px;color:#555">Mesma lógica do ranking R&S, mas pelo responsável pela admissão.</p>
      </div>
    </div>

    <div class="card" style="grid-column: span 2">
      <div class="card-header">
        <span class="badge badge-line">Linha</span>
        <span class="card-title">Histórico de Recrutamentos</span>
      </div>
      <div class="card-body">
        <p>Eixo X: Meses · Eixo Y: <b>VagasFechadaR&S</b> · Série: <b>CONSULTOR DE R&S</b></p>
        <p style="margin-top:6px;color:#555">Permite comparar a evolução de performance de múltiplos consultores ao longo dos meses. Selecione um ou mais consultores no visual para foco.</p>
      </div>
    </div>

  </div>
</div>

<!-- ==================== CONSULTA ==================== -->
<div class="page" id="pg-consulta">
  <h2 class="section-title">Aba — Consulta</h2>
  <p style="margin-bottom:20px;color:#555;font-size:.9rem">Tabela detalhada de vagas individuais para consulta operacional e exportação.</p>

  <div class="filters-bar">
    <h3>Filtros disponíveis</h3>
    <span class="filter-pill">🏷️ Marca</span>
    <span class="filter-pill">📅 Período (Ano / Trimestre / Mês / Dia)</span>
    <span class="filter-pill">👤 Nome Completo do candidato</span>
  </div>

  <div class="cards">
    <div class="card" style="grid-column: span 2">
      <div class="card-header">
        <span class="badge badge-table">Tabela</span>
        <span class="card-title">Tabela de Vagas</span>
      </div>
      <div class="card-body">
        <p>Listagem linha a linha de todas as vagas. Colunas:</p>
        <table class="rel-table" style="margin-top:10px">
          <tr><th>Campo</th><th>Descrição</th></tr>
          <tr><td>STATUS</td><td>Status atual da vaga (FECHADA, CANCELADA, ABERTA etc.)</td></tr>
          <tr><td>TICKET</td><td>Identificador único da solicitação</td></tr>
          <tr><td>NÍVEL</td><td>Senioridade do cargo</td></tr>
          <tr><td>CARGO</td><td>Nome do cargo solicitado</td></tr>
          <tr><td>MARCA</td><td>Marca/unidade solicitante</td></tr>
          <tr><td>NOME COMPLETO</td><td>Candidato contratado (preenchido quando fechada)</td></tr>
          <tr><td>CONSULTOR DE R&S</td><td>Responsável pelo processo seletivo</td></tr>
          <tr><td>GESTOR DA VAGA</td><td>Gestor solicitante</td></tr>
          <tr><td>DATA DE FECHAMENTO DA VAGA</td><td>Data de conclusão do processo</td></tr>
          <tr><td>DATA DE INICIO PREVISTA</td><td>Data prevista de início do candidato</td></tr>
          <tr><td>REMUNERAÇÃO</td><td>Salário da posição</td></tr>
        </table>
        <div class="note info" style="margin-top:12px">
          O filtro de período nesta aba usa <b>DATA DE FECHAMENTO</b> (relação ativa).
          Use o filtro de Nome para localizar um candidato específico.
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ==================== EXTRAÇÃO ==================== -->
<div class="page" id="pg-extracao">
  <h2 class="section-title">Aba — Extração de Bases</h2>
  <p style="margin-bottom:20px;color:#555;font-size:.9rem">Aba operacional para exportar dados filtrados. Voltada ao time de P&C para geração de relatórios pontuais.</p>

  <div class="filters-bar">
    <h3>Filtros disponíveis</h3>
    <span class="filter-pill">📅 Período (Ano / Mês / Dia)</span>
    <span class="filter-pill">📋 Tipo de Solicitação</span>
    <span class="filter-pill">👤 Consultor de R&S</span>
    <span class="filter-pill">🎫 Ticket (busca individual)</span>
    <span class="filter-pill">💼 Grupo de Cargo</span>
  </div>

  <div class="cards">
    <div class="card" style="grid-column: span 2">
      <div class="card-header">
        <span class="badge badge-table">Tabela</span>
        <span class="card-title">Extração de Bases</span>
      </div>
      <div class="card-body">
        <p>Tabela exportável com campos operacionais essenciais:</p>
        <ul style="margin-top:8px">
          <li><b>CONSULTOR DE R&S</b> — responsável pelo processo</li>
          <li><b>TICKET</b> — ID da solicitação</li>
          <li><b>TIPO DE SOLICITAÇÃO RECEBIDA</b> — R&S ou Admissão</li>
          <li><b>CARGO</b> — posição solicitada</li>
          <li><b>DATA DE FECHAMENTO DA VAGA</b> — data de conclusão</li>
          <li><b>DATA DE INICIO PREVISTA</b> — previsão de entrada do candidato</li>
        </ul>
        <div class="note info" style="margin-top:12px">
          Use o filtro de <b>Ticket</b> para buscar uma vaga específica. Use <b>Tipo</b> para separar bases de R&S e Admissão antes de exportar.
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ==================== PERFORMANCE HISTÓRICA ==================== -->
<div class="page" id="pg-historico">
  <h2 class="section-title">Aba — Performance Histórica — Recrutadores</h2>
  <p style="margin-bottom:20px;color:#555;font-size:.9rem">Matriz cruzando recrutadores × meses para acompanhamento longitudinal de produtividade.</p>

  <div class="cards">
    <div class="card" style="grid-column: span 2">
      <div class="card-header">
        <span class="badge badge-pivot">Pivot</span>
        <span class="card-title">Tabela Dinâmica — Recrutamentos por Recrutador × Mês</span>
      </div>
      <div class="card-body">
        <table class="rel-table">
          <tr><th>Dimensão</th><th>Campo</th><th>Papel</th></tr>
          <tr><td>Linha</td><td>CONSULTOR DE R&S</td><td>Cada consultor em uma linha</td></tr>
          <tr><td>Coluna</td><td>Ano › Mês (dCalendario)</td><td>Um mês por coluna</td></tr>
          <tr><td>Valor</td><td>VagasFechadaR&S</td><td>Fechamentos R&S no cruzamento consultor × mês</td></tr>
        </table>
        <div class="note info" style="margin-top:12px">
          Critério da medida <b>VagasFechadaR&S</b>: STATUS ≠ CANCELADA/DESISTENTE + DATA DE FECHAMENTO preenchida + NOME COMPLETO preenchido + TIPO = "R&S". Filtra por DATA DE FECHAMENTO (USERELATIONSHIP ativo nesta medida).
        </div>
      </div>
    </div>
  </div>
</div>

</main>

<script>
function show(id, el) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  el.classList.add('active');
  event.preventDefault();
}
</script>
</body>
</html>
"""

out = Path(r"C:\\Users\\marce\\Documents\\Raíz Educação\\Dados P&C\\Documentação\\dashboard_regras_negocio.html")
out.write_text(HTML, encoding="utf-8")
print(f"Gerado: {out}")
