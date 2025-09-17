from pathlib import Path
import csv
import networkx as nx
from pyvis.network import Network
import json

#1_ Importar CSV
arestas = Path('./R02_Arestas.csv').read_text().splitlines()
reader = csv.reader(arestas)
header_row = next(reader)

# Listas de dados
agentes = []
conexoes = []
tipo_de_cada_agente = []
tipo_de_conexoes = []

for row in reader:
    agente = row[0]
    agentes.append(agente)
    conexao = row[2]
    conexoes.append(conexao)
    tipo_de_conexao = row[8]
    tipo_de_conexoes.append(tipo_de_conexao)
    tipo_de_agente = row[7]
    tipo_de_cada_agente.append(tipo_de_agente)

#2_ Construir rede networkx
G = nx.Graph()
edge_list = list(zip(agentes, conexoes))
G = nx.from_edgelist(edge_list)

#3_ PyVis
net = Network(notebook=False, height='100vh', width='100%', bgcolor='#ffffff', font_color='black')
net.from_nx(G)

# cores iniciais (visão geral)
for node in G.nodes():
    grau = G.degree[node]
    if node in agentes:
        cor = '#6a1b9a'
        tamanho = grau/2
    elif node in conexoes:
        cor = '#f5b041'
        tamanho = 10
    else:
        cor = 'gray'
        tamanho = 10

    for n in net.nodes:
        if n['id'] == node:
            n['color'] = cor
            n['size'] = tamanho
            n['title'] = f"{node} | conexões: {grau}"
            break

# Arestas: cor por tipo de conexão
cores_por_conexao = {
    "parceria em projeto": "#d8be3c",
    "financiamento": "#e83010",
    "membro": "#9327d6",
    "coleta de dados": "#5983c6",
}
for i, edge in enumerate(net.edges):
    if i < len(tipo_de_conexoes):
        tipo = tipo_de_conexoes[i].strip().lower()
        cor = cores_por_conexao.get(tipo, "#999999")
        edge['color'] = cor
        edge['title'] = f"Tipo de conexão: {tipo.title()}"
    else:
        edge['color'] = "#cccccc"
        edge['title'] = "Tipo de conexão: desconhecido"
    edge['id'] = i  # id único

#4_ Exportar HTML inicial
net.write_html("./index.html")

# ---------- Injetar painel + JS ----------
html_path = "./index.html"

# JSONs para injetar
agentes_json = json.dumps(agentes)
conexoes_json = json.dumps(conexoes)
tipos_agente_dict = {agentes[i]: tipo_de_cada_agente[i].strip().lower()
                     for i in range(len(agentes))}
tipos_agente_json = json.dumps(tipos_agente_dict)
tipos_conexao_dict = {i: tipo_de_conexoes[i].strip().lower()
                      for i in range(len(tipo_de_conexoes))}
tipos_conexao_json = json.dumps(tipos_conexao_dict)


# título

titulo_html = """
<div style="position: absolute; top: 20px; left: 20px; background: rgba(255,255,255,0.9); 
            padding: 12px 20px; border-radius: 8px; font-family: 'Montserrat', sans-serif; 
            font-size: 40px; font-weight: 900 color: #333333; z-index: 1000;">
  Rede GHZ
  <div style="font-size: 14px; font-weight: normal; margin-top: 5px;">
    Agentes sociais para inteligência coletiva e governança de dados urbanos
  </div>
</div>
"""


# Painel de legenda com botões

legenda_html = f"""
<div style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.95); 
            padding: 15px; border: 1px solid #ccc; border-radius: 8px; font-family: sans-serif;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1); z-index: 999; color: #333; font-size: 13px;">
  <strong>Legenda</strong><br><br>

  <div style="margin-bottom: 8px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #6a1b9a; margin-right: 8px; border: .5px solid #000;"></span>
    Agentes
  </div>
  <div style="margin-bottom: 15px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #f5b041; margin-right: 8px; border: .5px solid #000;"></span>
    Conexões
  </div>

  <!--___________TIPOS DE AGENTES -->
    <strong>Tipo de agente</strong><br><br>
  <div style="margin-bottom: 15px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #1f77b4; margin-right: 8px; border: .5px solid #000;"></span>
    Escola
  </div>
    <div style="margin-bottom: 15px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #e7d56d; margin-right: 8px; border: .5px solid #000;"></span>
    Organização da sociedade civil (osc) / Associação/ Coletivo
  </div>
    <div style="margin-bottom: 15px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #2ca02c; margin-right: 8px; border: .5px solid #000;"></span>
    Rede/Conexão
  </div>
    <div style="margin-bottom: 15px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #d62728; margin-right: 8px; border: .5px solid #000;"></span>
    Laboratório
  </div>
    <div style="margin-bottom: 15px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #9467bd; margin-right: 8px; border: .5px solid #000;"></span>
    Programa/Projeto
  </div>
    <div style="margin-bottom: 15px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #8c564b; margin-right: 8px; border: .5px solid #000;"></span>
    Empresa privada
  </div>
    <div style="margin-bottom: 15px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #a09f9f; margin-right: 8px; border: .5px solid #000;"></span>
    Público
  </div>
    <div style="margin-bottom: 15px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #EB81EA; margin-right: 8px; border: .5px solid #000;"></span>
    Instituto
  </div>

<!-- LINHAS COLORIDAS DE TIPO DE CONEXÃO -->
<strong>Tipo de conexão</strong><br><br>

<div style="margin-bottom: 10px;">
  <div style="width: 100%; height: 3px; background: #d8be3c; margin-bottom: 4px;"></div>
  Parceria em projeto
</div>

<div style="margin-bottom: 10px;">
  <div style="width: 100%; height: 3px; background: #e83010; margin-bottom: 4px;"></div>
  Financiamento
</div>

<div style="margin-bottom: 10px;">
  <div style="width: 100%; height: 3px; background: #9327d6; margin-bottom: 4px;"></div>
  Membro
</div>

<div style="margin-bottom: 10px;">
  <div style="width: 100%; height: 3px; background: #5983c6; margin-bottom: 4px;"></div>
  Coleta de dados
</div>

  <strong>Visualização da rede</strong><br>
  <button onclick="tiposAgente()" style="margin-top: 5px; color: #333;"> Tipo de agente </button><br>
  <button onclick="tiposConexao()" style="margin-top: 5px; color: #333;"> Relações </button><br>
  <button onclick="temasPrincipais()" style="margin-top: 5px; color: #333;"> Temas </button>
</div>

<script>
  // Dados do Python
  var agentes = {agentes_json};
  var conexoes = {conexoes_json};
  var tiposAgenteDict = {tipos_agente_json};
  var tiposConexaoDict = {tipos_conexao_json};

  // Funções JS
  function tiposAgente() {{
    const coresPorTipo = {{
      "escola": "#1f77b4",
      "organização da sociedade civil (osc) / associação/ coletivo": "#e7d56d",
      "rede/conexão": "#2ca02c",
      "laboratório": "#d62728",
      "programa/projeto": "#9467bd",
      "empresa privada": "#8c564b",
      "público": "#a09f9f",
      "instituto": "#EB81EA",
      "desconhecido": "#aaaaaa"
    }};
    nodes.forEach(function(node) {{
      let tipo = tiposAgenteDict[node.id] || "desconhecido";
      node.color = coresPorTipo[tipo] || "#aaaaaa";
      nodes.update(node);
    }});
  }}

  function tiposConexao() {{
    const coresPorConexao = {{
      "parceria em projeto": "#d8be3c",
      "financiamento": "#e83010",
      "membro": "#9327d6",
      "coleta de dados": "#5983c6"
    }};
    edges.forEach(function(edge) {{
      let tipo = tiposConexaoDict[edge.id] || "desconhecido";
      edge.color = coresPorConexao[tipo] || "#999999";
      edges.update(edge);
    }});
  }}

  function temasPrincipais() {{
    alert("Função de temas principais ainda não implementada!");
  }}
</script>
"""

# Injetar no HTML
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Injetar link da fonte Montserrat e CSS global no <head>
html = html.replace(
    "</head>",
    """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
<style>
  body, button, div, span, h1, h2, h3, h4, h5, h6, a, p {
    font-family: 'Montserrat', sans-serif !important;
  }
</style>
</head>
"""
)

html_modificado = html.replace("<body>", f"<body>\n{titulo_html}\n{legenda_html}")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_modificado)

print("rede3.html gerado")
