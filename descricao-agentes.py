from pathlib import Path
import csv
from pyvis.network import Network

# 1. Importar CSV
arestas = Path('./R01_node-list.csv').read_text().splitlines()
reader = csv.reader(arestas)
header_row = next(reader)

agentes, tipo_de_cada_agente, descricoes, sites = [], [], [], []

for row in reader:
    agentes.append(row[0])
    tipo_de_cada_agente.append(row[1])
    descricoes.append(row[2])
    sites.append(row[3])

# 2. Gerar HTML base
net = Network(height='400px', width='100%', bgcolor='#ffffff', font_color='#333333')
html_path = "./descricao-agentes.html"
net.write_html(html_path)

# 3. Título
titulo_html = """
<div style="margin-top: 30px; margin-left: 5%; width: 50%; 
            font-family: 'Montserrat', sans-serif; color: #333333;">
  <div style="font-size: 40px; font-weight: 900;">Rede GHZ</div>
  <div style="font-size: 14px; font-weight: normal; margin-top: 5px;">
    Agentes sociais para inteligência coletiva e governança de dados urbanos
  </div>
</div>
"""

# 4. Bloco de descrições
descricao_agentes_html = """
<div style="
    margin-top: 40px;
    margin-left: 5%; 
    width: 50%; 
    font-family: 'Montserrat', sans-serif; 
    font-size: 14px; 
    color: #333;
    line-height: 1.5;
    padding-bottom: 80px;
">
<h2 style="font-size: 22px; margin-bottom: 20px;">Descrição dos Agentes</h2>
"""

# --- CORES por tipo ---
cores_tipos = {
    "escola": "#1f77b4",
    "organização da sociedade civil (osc) / associação/ coletivo": "#e7d56d",
    "rede/conexão": "#2ca02c",
    "laboratório": "#d62728",
    "programa/projeto": "#9467bd",
    "empresa privada": "#8c564b",
    "público": "#a09f9f",
    "instituto": "#D117CE",
}

# 5. Enumerar agentes com cores de fundo diferentes
for i, (agente, tipo, descricao, site) in enumerate(zip(agentes, tipo_de_cada_agente, descricoes, sites), start=1):
    cor_fundo = cores_tipos.get(tipo.strip().lower(), "#f9f9f9")
    descricao_agentes_html += f"""
    <div style="margin-bottom: 18px;">
        <div style="background-color:{cor_fundo}80; padding: 6px 10px; border-radius:4px; display:inline-block;">
            <b>{i}. {agente}</b> <span style="font-size:12px; color:#666;">({tipo})</span>
        </div><br>
        {descricao}<br>
        <a href="{site}" target="_blank" style="color:#0066cc; text-decoration:none;">{site}</a><br>
        <span style="font-size: 11px; color:#555;">
            <i>descrições geradas a partir dos sites oficiais</i>
        </span>
    </div>
    """

descricao_agentes_html += "</div>"

# 6. Injetar no HTML final
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Fonte Montserrat, fundo com imagem e opacidade
html = html.replace(
    "</head>",
    """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
<style>
  body, button, div, span, h1, h2, h3, h4, h5, h6, a, p {
    font-family: 'Montserrat', sans-serif !important;
  }

  /* Fundo com imagem e opacidade */
  body {
    background: 
      linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)), 
      url('rede.png') no-repeat center center fixed;
    background-size: cover;
    margin: 0;
    padding: 0;
  }

  /* Corrigir faixa branca da rede */
  #mynetwork {
    height: 300px !important;
    position: relative !important;
  }
</style>
</head>
"""
)

# 7. Inserir o título e descrições
html_modificado = html.replace("<body>", f"<body>\n{titulo_html}\n{descricao_agentes_html}")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_modificado)

print("✅ descricao-agentes.html gerado com fundo e cores por tipo")
