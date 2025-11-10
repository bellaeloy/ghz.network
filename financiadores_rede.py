from pathlib import Path
import csv
import networkx as nx
from pyvis.network import Network

# 1. Importar CSV corretamente
with open('./R02_node-list.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header_row = next(reader)

    agentes = []
    financiadores_internacionais = []
    todos_financiadores = []
    edge_list = []
    

    for row in reader:
        if len(row) < 9:  # evita erro se a linha for curta
            continue

        agente = row[0].strip()
        agentes.append(agente)

        # internacionais
        internacional = row[6]
        financiador_internacional = [f.strip() for f in internacional.split("|") if f.strip()]
        financiadores_internacionais.extend(financiador_internacional)

        # todos
        financiadores = row[7]
        financiador = [f.strip() for f in financiadores.split("|") if f.strip()]
        todos_financiadores.extend(financiador)

        # montar lista de arestas
        for f in financiador:
            edge_list.append((agente, f))


# Remover duplicatas
agentes = list(set(agentes))
financiadores_internacionais = list(set(financiadores_internacionais))
todos_financiadores = list(set(todos_financiadores))


# 2. Construir grafo
H = nx.Graph()
H.add_edges_from(edge_list)

# 3. PyVis
net = Network(notebook=False, height='100vh', width='100%', bgcolor='#ffffff', font_color='black')
net.from_nx(H)

# 4. PyVis
net = Network(notebook=False, height='100vh', width='100%', bgcolor='#ffffff', font_color='black')
net.from_nx(H)

# 5. Cores dos nós
for node in H.nodes():
    grau = H.degree[node]

    if node in agentes:
        cor = '#6a1b9a'  # Roxo - agentes
        tamanho = 20
    elif node in financiadores_internacionais:
        cor = "#f83a1d"  # Azul - financiadores internacionais
        tamanho = grau*4
        if tamanho < 12:
            tamanho = 12    
    elif node in todos_financiadores:
        cor = "#ffb2a8"  # Laranja - financiadores nacionais
        tamanho = grau*4
        if tamanho < 12:
            tamanho = 12
    else:
        cor = 'gray'
        tamanho = 12

    for n in net.nodes:
        if n['id'] == node:
            n['color'] = cor
            n['size'] = tamanho
            n['title'] = f"{node} | conexões: {grau}"
            break

# 6. Definir cor das arestas como cinza escuro
for edge in net.edges:
    edge['color'] = '#333333'

#7. calcular as porcentagens
total_financiadores = len(todos_financiadores)

if total_financiadores > 0:
    perc_internacionais = round(len(financiadores_internacionais) / total_financiadores * 100, 1)
    perc_nacionais = round((len(todos_financiadores) - len(financiadores_internacionais)) / total_financiadores * 100, 1)
else:
    perc_internacionais = perc_nacionais = 0


# 7.Legenda

legenda_html = f"""
<div style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.95); 
            padding: 15px; border: 1px solid #ccc; border-radius: 8px; font-family: sans-serif;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1); z-index: 999; color: #333; font-size: 13px;">
  <strong>Rede GHZ | Financiadores</strong><br><br>

  <div style="margin-bottom: 8px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #6a1b9a; margin-right: 8px; border: .5px solid #000;"></span>
    Agentes
  </div>
  <div style="margin-bottom: 8px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #f83a1d; margin-right: 8px; border: .5px solid #000;"></span>
    Financiadores Internacionais ({perc_internacionais}%)
  </div>
  <div style="margin-bottom: 8px;">
    <span style="display: inline-block; width: 15px; height: 15px; background: #ffb2a8; margin-right: 8px; border: .5px solid #000;"></span>
    Financiadores Nacionais ({perc_nacionais}%)
  </div>
</div>
"""


# Gerar HTML com PyVis
net.write_html("financiadores_rede.html")

# Abrir o arquivo e injetar a legenda
html_file = "financiadores_rede.html"
with open(html_file, "r", encoding="utf-8") as f:
    html_content = f.read()

# Inserir legenda antes de </body>
html_content = html_content.replace("</body>", legenda_html + "</body>")

# Salvar de volta
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Arquivo 'financiadores_rede.html'!")
