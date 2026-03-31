#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gerador de relatório HTML para resultados dos testes de API (pytest).
Lê o JUnit XML e gera um HTML visual equivalente ao relatório do framework Behave.
Textos em PT-BR. Estrutura: reports/ano/mês/Testes - data/
"""
import platform
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Optional

# Mapeamento de meses em português
MESES = {
    "01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril",
    "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
    "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro",
}


def _agrupar_por_modulo(testes: list) -> dict:
    """Agrupa testes por módulo (extraído do classname)."""
    grupos = {}
    for t in testes:
        classname = t.get("classname", "testes")
        # testes.api.auth.test_auth -> auth
        partes = classname.split(".")
        modulo = partes[-2] if len(partes) >= 2 else partes[-1] if partes else "outros"
        if modulo not in grupos:
            grupos[modulo] = []
        grupos[modulo].append(t)
    return grupos


def gerar_relatorio_html(
    xml_file: str = "reports/junit.xml",
    output_dir: Optional[Path] = None,
    copiar_junit: bool = True,
) -> Optional[Path]:
    """
    Gera relatório HTML a partir do JUnit XML (pytest).
    Retorna o path do arquivo HTML ou None se XML não existir.
    """
    path_xml = Path(xml_file)
    if not path_xml.exists():
        print(f"[AVISO] Arquivo não encontrado: {path_xml}")
        return None

    root = ET.parse(path_xml).getroot()
    now = datetime.now()
    year = now.strftime("%Y")
    month_num = now.strftime("%m")
    month_name = MESES.get(month_num, month_num)
    day_folder = now.strftime("Testes - %Y-%m-%d %Hh%M")
    timestamp = now.strftime("%d-%m-%Y_%H-%M")

    if output_dir is None:
        output_dir = Path("reports") / year / month_name / day_folder
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"report_{timestamp}.html"

    # Copia JUnit para a pasta do relatório
    if copiar_junit:
        junit_dest = output_dir / f"junit_{timestamp}.xml"
        shutil.copy2(path_xml, junit_dest)
        print(f"[OK] JUnit copiado para: {junit_dest}")

    # Coleta todos os testcases do JUnit
    testes = []
    tempo_total = 0.0
    for elem in root.iter():
        if elem.tag == "testcase":
            nome = elem.get("name", "")
            classname = elem.get("classname", "")
            tempo = float(elem.get("time", 0))
            tempo_total += tempo
            status = "passed"
            msg = ""
            for child in elem:
                if child.tag in ("failure", "error"):
                    status = "failed"
                    msg = (child.get("message") or "") + "\n" + (child.text or "")
                elif child.tag == "skipped":
                    status = "skipped"
                    msg = child.get("message") or (child.text or "")
            testes.append({
                "nome": nome,
                "classname": classname,
                "tempo": tempo,
                "status": status,
                "msg": msg.strip(),
            })

    # Estatísticas
    total = len(testes)
    passaram = sum(1 for t in testes if t["status"] == "passed")
    falharam = sum(1 for t in testes if t["status"] == "failed")
    pulados = sum(1 for t in testes if t["status"] == "skipped")

    # Duração formatada
    horas = int(tempo_total // 3600)
    minutos = int((tempo_total % 3600) // 60)
    segundos = int(tempo_total % 60)
    duracao_formatada = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    # Agrupa por módulo para exibir como "Funcionalidade"
    grupos = _agrupar_por_modulo(testes)

    # HTML com mesmo estilo do Behave (header, info colapsável, cards, conteúdo, footer)
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Testes de API</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header .timestamp {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .execution-info {{
            background: white;
            border-bottom: 2px solid #e0e0e0;
        }}
        .info-header {{
            padding: 15px 30px;
            background: #f8f9fa;
            cursor: pointer;
            user-select: none;
            font-weight: bold;
            font-size: 16px;
            transition: background 0.2s;
        }}
        .info-header:hover {{
            background: #e9ecef;
        }}
        .info-content {{
            display: none;
            padding: 20px 30px;
        }}
        .info-content.expanded {{
            display: block;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .info-section {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
        }}
        .info-section h3 {{
            margin-bottom: 15px;
            color: #667eea;
            font-size: 16px;
        }}
        .info-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        .info-item:last-child {{
            border-bottom: none;
        }}
        .info-label {{
            font-weight: 500;
            color: #666;
        }}
        .info-value {{
            color: #333;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .summary-card .number {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .summary-card .label {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
        }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .skipped {{ color: #ffc107; }}
        .summary-card.clickable {{
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .summary-card.clickable:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .summary-card.active {{
            border: 3px solid #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}
        .content {{
            padding: 30px;
        }}
        .feature {{
            margin-bottom: 30px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}
        .feature-header {{
            background: #667eea;
            color: white;
            padding: 15px 20px;
            font-size: 18px;
            font-weight: bold;
        }}
        .scenario {{
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
        }}
        .scenario:last-child {{
            border-bottom: none;
        }}
        .scenario-header {{
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
            cursor: pointer;
            user-select: none;
            padding: 10px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}
        .scenario-header:hover {{
            background: #f8f9fa;
        }}
        .toggle-icon {{
            margin-right: 10px;
            transition: transform 0.3s;
            display: inline-block;
        }}
        .toggle-icon.expanded {{
            transform: rotate(90deg);
        }}
        .scenario-details {{
            display: none;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 4px;
            margin-top: 10px;
        }}
        .scenario-details.expanded {{
            display: block;
        }}
        .step {{
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }}
        .step.passed {{
            background: #d4edda;
            border-left: 4px solid #28a745;
        }}
        .step.failed {{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
        }}
        .step.skipped {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
        }}
        .step-duration {{
            float: right;
            color: #666;
            font-size: 12px;
        }}
        .error-message {{
            background: #f8f9fa;
            border: 1px solid #dc3545;
            border-radius: 4px;
            padding: 15px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            color: #dc3545;
            white-space: pre-wrap;
        }}
        .filters-section {{
            padding: 20px 30px;
            background: white;
            border-bottom: 2px solid #e0e0e0;
        }}
        .search-container {{
            margin-bottom: 15px;
        }}
        #searchInput {{
            width: 100%;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
        }}
        #searchInput:focus {{
            outline: none;
            border-color: #667eea;
        }}
        .filter-info {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
            color: #666;
        }}
        #clearFilters {{
            padding: 8px 16px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }}
        #clearFilters:hover {{
            background: #c82333;
        }}
        .scenario.hidden {{
            display: none;
        }}
        .feature.hidden {{
            display: none;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Relatório de Testes de API</h1>
            <div class="timestamp">Gerado em: {now.strftime('%d/%m/%Y às %H:%M:%S')}</div>
        </div>

        <div class="execution-info">
            <div class="info-header" onclick="toggleInfo(this)">
                <span class="toggle-icon">▶</span>
                Informações de Execução e Ambiente
            </div>
            <div class="info-content">
                <div class="info-grid">
                    <div class="info-section">
                        <h3>Execução</h3>
                        <div class="info-item">
                            <span class="info-label">Duração total:</span>
                            <span class="info-value">{duracao_formatada}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Data/hora geração:</span>
                            <span class="info-value">{now.strftime('%d/%m/%Y %H:%M:%S')}</span>
                        </div>
                    </div>
                    <div class="info-section">
                        <h3>Sistema</h3>
                        <div class="info-item">
                            <span class="info-label">Sistema operacional:</span>
                            <span class="info-value">{platform.system()} {platform.release()}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Python:</span>
                            <span class="info-value">{platform.python_version()}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Diretório:</span>
                            <span class="info-value" style="font-size: 11px;">{Path.cwd()}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="summary">
            <div class="summary-card">
                <div class="number">{total}</div>
                <div class="label">Total de testes</div>
            </div>
            <div class="summary-card clickable" data-status="passed" onclick="filterByStatus('passed', this)" title="Clique para filtrar">
                <div class="number passed">{passaram}</div>
                <div class="label">Passaram</div>
            </div>
            <div class="summary-card clickable" data-status="failed" onclick="filterByStatus('failed', this)" title="Clique para filtrar">
                <div class="number failed">{falharam}</div>
                <div class="label">Falharam</div>
            </div>
            <div class="summary-card clickable" data-status="skipped" onclick="filterByStatus('skipped', this)" title="Clique para filtrar">
                <div class="number skipped">{pulados}</div>
                <div class="label">Pulados</div>
            </div>
            <div class="summary-card">
                <div class="number">{duracao_formatada}</div>
                <div class="label">Duração</div>
            </div>
        </div>

        <div class="filters-section">
            <div class="search-container">
                <input type="text" id="searchInput" placeholder="Buscar testes..." onkeyup="filterScenarios()">
            </div>
            <div class="filter-info">
                <span id="filterStatus">Mostrando todos os testes</span>
                <button id="clearFilters" onclick="clearAllFilters()" style="display: none;">Limpar filtros</button>
            </div>
        </div>

        <div class="content">
"""

    # Agrupa por módulo (funcionalidade)
    for modulo_nome in sorted(grupos.keys()):
        lista_testes = grupos[modulo_nome]
        # Nome amigável: auth -> Auth, test_health -> Health
        titulo_modulo = modulo_nome.replace("_", " ").title()
        html += f"""
            <div class="feature">
                <div class="feature-header">Funcionalidade: {titulo_modulo}</div>
"""
        for t in lista_testes:
            status = t["status"]
            expanded_class = " expanded" if status == "failed" else ""
            # Escapa HTML no nome e na mensagem
            nome_safe = t["nome"].replace("<", "&lt;").replace(">", "&gt;")
            msg_safe = (t["msg"][:2000] or "").replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
            html += f"""
                <div class="scenario" data-status="{status}">
                    <div class="scenario-header" onclick="toggleScenario(this)">
                        <span class="toggle-icon{expanded_class}">▶</span>
                        {nome_safe}
                    </div>
                    <div class="scenario-details{expanded_class}">
                        <div class="step {status}">
                            <span>{nome_safe}</span>
                            <span class="step-duration">{t['tempo']:.3f}s</span>
                        </div>
"""
            if t["msg"]:
                html += f"""
                        <div class="error-message">{msg_safe}</div>
"""
            html += """
                    </div>
                </div>
"""
        html += """
            </div>
"""
    html += """
        </div>

        <div class="footer">
            Relatório gerado automaticamente pelo framework de testes de API (pytest)
        </div>
    </div>

    <script>
        function toggleInfo(header) {
            var content = header.nextElementSibling;
            var icon = header.querySelector('.toggle-icon');
            content.classList.toggle('expanded');
            icon.classList.toggle('expanded');
        }
        function toggleScenario(header) {
            var details = header.nextElementSibling;
            var icon = header.querySelector('.toggle-icon');
            details.classList.toggle('expanded');
            icon.classList.toggle('expanded');
        }
        var currentFilter = 'all';
        var currentSearchTerm = '';
        function filterScenarios() {
            currentSearchTerm = document.getElementById('searchInput').value.toLowerCase();
            applyFilters();
        }
        function filterByStatus(status, cardEl) {
            document.querySelectorAll('.summary-card').forEach(function(card) {
                card.classList.remove('active');
            });
            if (currentFilter === status) {
                currentFilter = 'all';
            } else {
                currentFilter = status;
                if (cardEl) cardEl.classList.add('active');
            }
            applyFilters();
        }
        function applyFilters() {
            var features = document.querySelectorAll('.feature');
            var visibleCount = 0;
            features.forEach(function(feature) {
                var scenarios = feature.querySelectorAll('.scenario');
                var featureHasVisible = false;
                scenarios.forEach(function(scenario) {
                    var visible = true;
                    if (currentFilter !== 'all') {
                        visible = scenario.getAttribute('data-status') === currentFilter;
                    }
                    if (currentSearchTerm) {
                        visible = visible && scenario.textContent.toLowerCase().indexOf(currentSearchTerm) !== -1;
                    }
                    if (visible) {
                        scenario.classList.remove('hidden');
                        featureHasVisible = true;
                        visibleCount++;
                    } else {
                        scenario.classList.add('hidden');
                    }
                });
                feature.classList.toggle('hidden', !featureHasVisible);
            });
            document.getElementById('filterStatus').textContent = currentFilter !== 'all' || currentSearchTerm
                ? 'Mostrando ' + visibleCount + ' de ' + document.querySelectorAll('.scenario').length + ' testes'
                : 'Mostrando todos os testes';
            document.getElementById('clearFilters').style.display = (currentFilter !== 'all' || currentSearchTerm) ? 'inline-block' : 'none';
        }
        function clearAllFilters() {
            currentFilter = 'all';
            currentSearchTerm = '';
            document.getElementById('searchInput').value = '';
            document.querySelectorAll('.summary-card').forEach(function(card) {
                card.classList.remove('active');
            });
            applyFilters();
        }
    </script>
</body>
</html>
"""

    output_file.write_text(html, encoding="utf-8")
    print(f"[OK] Relatório gerado: {output_file}")
    print(f"Estrutura: reports/{year}/{month_name}/{day_folder}/")
    return output_file


if __name__ == "__main__":
    gerar_relatorio_html()
