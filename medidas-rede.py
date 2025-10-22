from pathlib import Path
import csv
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 1. Importar CSV
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

# 2. Construir rede NetworkX
edge_list = list(zip(agentes, conexoes))
G = nx.from_edgelist(edge_list)

# 3. Cálculo das métricas
num_nodes = G.number_of_nodes()
num_arestas = G.number_of_edges()
grau_medio = sum(dict(G.degree()).values()) / G.number_of_nodes()
densidade = nx.density(G)
comp_desconectados = nx.number_connected_components(G)
nos_maior_componente = len(max(nx.connected_components(G), key=len))
centralidade = nx.degree_centrality(G)
maior_no = max(centralidade, key=centralidade.get)
maior_valor = centralidade[maior_no]
menor_no = min(centralidade, key=centralidade.get)
menor_valor = centralidade[menor_no]
betweenness = nx.betweenness_centrality(G)
top5 = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
closeness = nx.closeness_centrality(G)
top5_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:5]
assortatividade = nx.degree_assortativity_coefficient(G)
media_grau = 2 * G.number_of_edges() / G.number_of_nodes()
graus = [d for n, d in G.degree()]
variancia_grau = sum((k - media_grau)**2 for k in graus) / len(graus)

comunidades = nx.community.louvain_communities(G)
modularidade = nx.community.modularity(G, comunidades)

lista_unica_agentes = list(set(agentes))
''' ###AQUI
#4. Gerar imagem de um gráfico de barras dos top 10 centralidade
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Montserrat'

top10_centralidade = sorted(centralidade.items(), key=lambda item: item[1], reverse=True)[:10]

# Separar os dados
nodos_top10 = [item[0] for item in top10_centralidade]
valores_top10 = [item[1] for item in top10_centralidade]

# Destacar o nó com maior valor
maior_no_top10 = nodos_top10[0]
cores = ['red' if no == maior_no_top10 else 'steelblue' for no in nodos_top10]

# Criar figura com barras mais esbeltas (largura menor)
plt.figure(figsize=(10, 6))
plt.bar(nodos_top10, valores_top10, color=cores, width=0.3)

# Título e eixos
plt.title('Top 10 Centralidade de Grau', fontsize=14)
plt.xlabel('Nó', fontsize=12)
plt.ylabel('Centralidade de Grau', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.tight_layout()

# Salvar imagem
plt.savefig("centralidade_grau_top10.png", dpi=300)
plt.close()
'''


# 4. Painel HTML das medidas (sem alterar!)
painel_medidas_html = f"""
<div style="max-width: 800px; margin: 20px auto 40px auto;
            background: rgba(255,255,255,0.95); padding: 25px 30px; 
            border-radius: 8px; font-family: 'Montserrat', sans-serif; font-size: 13px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0); color: #333;">

  <strong style="font-size: 18px; display: block; margin-bottom: 20px;">Medidas da Rede</strong>

  <div style="border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
  <strong style = "font-size: 16px;">Propriedades básicas</strong>
  
  <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Medidas que descrevem as características formais.</em>
  </p>
  
  <div style="display: flex; justify-content: space-between; margin-top: 15px;">
    
    <div style="text-align: center;">
      <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/img1.png" alt="Agentes" style="width: 50px; margin-top: 5px; margin-bottom: 5px;">
      <div>Número de agentes</div>
      <div style="font-size: 30px; font-weight: bold;">{len(lista_unica_agentes)}</div>
    </div>

    <div style="text-align: center;">
      <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/img1.png" alt="Nós" style="width: 50px; margin-top: 5px;">
      <div>Número de nós</div>
      <div style="font-size: 30px; font-weight: bold;">{num_nodes}</div>
    </div>

    <div style="text-align: center;">
      <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/img1.png" alt="Arestas" style="width: 50px; margin-top: 5px;">
      <div>Número de arestas</div>
      <div style="font-size: 30px; font-weight: bold;">{num_arestas}</div>
    </div>

    <div style="text-align: center;">
      <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/img1.png" alt="Grau" style="width: 50px; margin-top: 5px;">
      <div>Grau médio</div>
      <div style="font-size: 30px; font-weight: bold;">{grau_medio:.3f}</div>
    </div>

    <div style="text-align: center;">
      <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/img1.png" alt="Densidade" style="width: 50px; margin-top: 5px;">
      <div>Densidade</div>
      <div style="font-size: 30px; font-weight: bold;">{densidade:.3f}</div>
    </div>

  </div>
</div>


<div style="border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
  <strong style = "font-size: 16px;">Estrutura e conectividade</strong>
  
  <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Informações sobre a organização dos componentes.</em>
  </p>


    <!-- Indicadores em formato de texto normal -->
  <p style="margin: 0; color: #333;">
    Componentes desconectados: <strong style="font-size: 13px;">{comp_desconectados}</strong><br>
    Nós do maior componente: <strong style="font-size: 13px;">{nos_maior_componente}</strong>
  </p>
  <p></p>

  <!-- Imagem única ocupando 100% da largura da caixa -->
  <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/componentes.png" alt="Visualização da estrutura da rede" style="width: 100%; border-radius: 4px; margin-bottom: 15px;">
</div>


  <div style="border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
    <strong style = "font-size: 16px;">Centralidade e influência</strong><br>
    Maior centralidade: {maior_no} ({maior_valor:.3f})<br>
    Menor centralidade: {menor_no} ({menor_valor:.3f})
  </div>

  <div style="border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
    <strong style = "font-size: 16px;">Top 5 Betweenness</strong><br>
    {"<br>".join([f"{no}: {valor:.4f}" for no, valor in top5])}
  </div>

  <div style="border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
    <strong style = "font-size: 16px;">Top 5 Closeness</strong><br>
    {"<br>".join([f"{no}: {valor:.4f}" for no, valor in top5_closeness])}
  </div>

  <div style="border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
    <strong style = "font-size: 16px;">Distribuição de grau</strong><br>
    Assortatividade: {assortatividade:.3f}<br>
    Média de grau: {media_grau:.2f}<br>
    Variância de grau: {variancia_grau:.2f}
  </div>

  <div style="border: 1px solid #ccc; padding: 15px; margin-bottom: 0; border-radius: 6px; background: #fff; width: 100%;">
    <strong style = "font-size: 16px;">Comunidades</strong><br>
    Número de comunidades: {len(comunidades)}<br>
    Modularidade: {modularidade:.3f}
  </div>

</div>
"""


# 5. Carregar header e footer
with open("header.html", "r", encoding="utf-8") as h:
    header_html = h.read()

with open("footer.html", "r", encoding="utf-8") as f:
    footer_html = f.read()

# 6. Injetar painel entre header e footer
html_final = f"""
{header_html}
{painel_medidas_html}
{footer_html}
"""

# 7. Salvar o HTML
with open("medidas-rede.html", "w", encoding="utf-8") as f:
    f.write(html_final)

print("Arquivo 'medidas-rede.html'")
