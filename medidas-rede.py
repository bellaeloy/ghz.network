from pathlib import Path
import csv
import networkx as nx

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


#4. Códigos para gerar as imagens, manter desativado
'''
#4.1 Gerar imagem de um gráfico de barras dos top 10 centralidade
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path

# Configuração da fonte Montserrat
# Caminho personalizado
caminho_fonte = "/home/bellx/Montserrat/static/Montserrat-Medium.ttf"

if Path(caminho_fonte).exists():
    font_manager.fontManager.addfont(caminho_fonte)
    plt.rcParams['font.family'] = 'Montserrat'
    print(f"Fonte Montserrat carregada de: {caminho_fonte}")
else:
    print(f"Fonte Montserrat não encontrada em: {caminho_fonte}. Usando fonte padrão do sistema.")

# Selecionar top 10 por centralidade
top10_centralidade = sorted(centralidade.items(), key=lambda item: item[1], reverse=True)[:10]

# Separar os dados
nodos_top10 = [item[0] for item in top10_centralidade]
valores_top10 = [item[1] for item in top10_centralidade]

# Destacar o nó com maior valor
maior_no_top10 = nodos_top10[0]
cores = ['purple' if no == maior_no_top10 else 'orange' for no in nodos_top10]

# Criar gráfico
plt.figure(figsize=(10, 6))
plt.bar(nodos_top10, valores_top10, color=cores, width=0.5)

plt.title('Top 10 Centralidade de Grau', fontsize=14)
plt.xlabel('Nó', fontsize=12)
plt.ylabel('Centralidade de Grau', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.tight_layout()

# Salvar imagem
plt.savefig("/home/bellx/github/ghz.site/imagens/centralidade_grau_top10.png", dpi=300)
plt.close()
'''


'''
#4.2 Gerar imagem da rede com gradiente de betweenness (rótulos apenas top 10)
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
from pathlib import Path
import matplotlib.patheffects as path_effects  # <-- Import para o contorno do texto

# Configuração da fonte Montserrat
caminho_fonte = "/home/bellx/Montserrat/static/Montserrat-Medium.ttf"
if Path(caminho_fonte).exists():
    font_manager.fontManager.addfont(caminho_fonte)
    plt.rcParams['font.family'] = 'Montserrat'
    print(f"Fonte Montserrat carregada de: {caminho_fonte}")
else:
    print(f"Fonte Montserrat não encontrada em: {caminho_fonte}. Usando fonte padrão do sistema.")

# Normalizar betweenness para usar em colormap
valores_bet = list(betweenness.values())
norm = mpl.colors.Normalize(vmin=min(valores_bet), vmax=max(valores_bet))
cmap = plt.cm.plasma
cores_nos = [cmap(norm(betweenness[n])) for n in G.nodes()]

# Layout e tamanho dos nós
pos = nx.spring_layout(G, seed=42, k=0.3)
tamanhos = [500 * centralidade[n] + 50 for n in G.nodes()]

# Criar figura e eixo explicitamente
fig, ax = plt.subplots(figsize=(10, 8))

# Desenhar nós e arestas
nx.draw_networkx_nodes(G, pos, node_color=cores_nos, node_size=tamanhos, alpha=0.9, ax=ax, linewidths=0.5, edgecolors="white")
nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.25, ax=ax)

# Selecionar top 10 nós por betweenness
top10 = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
nodos_rotulados = set([n for n, _ in top10])

# Preparar labels só para esses nós
labels = {n: n for n in G.nodes() if n in nodos_rotulados}

# Ajustar posição dos labels para ficar um pouco acima do nó (deslocamento maior)
labels_pos = {n: (x, y + 0.06) for n, (x, y) in pos.items() if n in labels}

# Desenhar labels com bbox branca semi-transparente e contorno para legibilidade
labels_drawn = nx.draw_networkx_labels(
    G, labels_pos, labels=labels, font_size=8, font_color='black',
    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'),
    ax=ax
)

# Contorno branco nos textos para destacar
for text in labels_drawn.values():
    text.set_path_effects([
        path_effects.Stroke(linewidth=2, foreground='white'),
        path_effects.Normal()
    ])

# Barra de cores
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Betweenness Centrality', fontsize=10)

ax.set_title('Rede GHZ – Gradiente de Betweenness (Top 10 rotulados)', fontsize=13, pad=15)
ax.axis('off')

plt.tight_layout()
plt.savefig("/home/bellx/github/ghz.site/imagens/rede_betweenness.png", dpi=300)
plt.close()

print("Imagem 'rede_betweenness.png' gerada com sucesso.")
'''

'''
# 4.4 Gerar imagem da rede com gradiente de closeness (rótulos top 5 e bottom 5)
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
from pathlib import Path
import matplotlib.patheffects as path_effects  # Para contorno do texto

# Configuração da fonte Montserrat
caminho_fonte = "/home/bellx/Montserrat/static/Montserrat-Medium.ttf"
if Path(caminho_fonte).exists():
    font_manager.fontManager.addfont(caminho_fonte)
    plt.rcParams['font.family'] = 'Montserrat'
    print(f"Fonte Montserrat carregada de: {caminho_fonte}")
else:
    print(f"Fonte Montserrat não encontrada em: {caminho_fonte}. Usando fonte padrão do sistema.")

# Normalizar closeness para usar em colormap
valores_close = list(closeness.values())
norm = mpl.colors.Normalize(vmin=min(valores_close), vmax=max(valores_close))
cmap = plt.cm.plasma
cores_nos = [cmap(norm(closeness[n])) for n in G.nodes()]

# Layout e tamanho dos nós
pos = nx.spring_layout(G, seed=42, k=0.3)
tamanhos = [500 * centralidade[n] + 50 for n in G.nodes()]  # mantém tamanho baseado na centralidade de grau

# Criar figura e eixo
fig, ax = plt.subplots(figsize=(10, 8))

# Desenhar nós e arestas
nx.draw_networkx_nodes(G, pos, node_color=cores_nos, node_size=tamanhos, alpha=0.9, ax=ax, linewidths=0.5, edgecolors="white")
nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.25, ax=ax)

# Selecionar top 5 e bottom 5 por closeness
top5 = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:5]
bottom5 = sorted(closeness.items(), key=lambda x: x[1])[:5]
nodos_rotulados = set([n for n, _ in top5 + bottom5])

# Preparar labels apenas para esses nós 
labels = {n: n for n in G.nodes() if n in nodos_rotulados}
labels_pos = {n: (x, y + 0.06) for n, (x, y) in pos.items() if n in labels}

# Desenhar labels com bbox branca semi-transparente e contorno
labels_drawn = nx.draw_networkx_labels(
    G, labels_pos, labels=labels, font_size=8, font_color='black',
    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'),
    ax=ax
)

# Contorno branco nos textos para destacar
for text in labels_drawn.values():
    text.set_path_effects([
        path_effects.Stroke(linewidth=2, foreground='white'),
        path_effects.Normal()
    ])

# Barra de cores
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Closeness Centrality', fontsize=10)

ax.set_title('Rede GHZ - Gradiente de Closeness (Top 5 e Bottom 5 rotulados)', fontsize=13, pad=15)
ax.axis('off')

plt.tight_layout()
plt.savefig("/home/bellx/github/ghz.site/imagens/rede_closeness.png", dpi=300)
plt.close()

print("Imagem 'rede_closeness.png' gerada com sucesso.")
'''


'''
#4.5 histograma de grau x nós
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from pathlib import Path

# Fonte Montserrat
caminho_fonte = "/home/bellx/Montserrat/static/Montserrat-Medium.ttf"
if Path(caminho_fonte).exists():
    font_manager.fontManager.addfont(caminho_fonte)
    plt.rcParams['font.family'] = 'Montserrat'
else:
    print("Fonte Montserrat não encontrada, usando padrão do sistema.")

# Dados
graus = [d for n, d in G.degree()]
media_grau = np.mean(graus)
desvio_grau = np.std(graus)

# Criar histograma
plt.figure(figsize=(10, 6))
n_bins = min(20, len(set(graus)))  # número de bins razoável
plt.hist(graus, bins=n_bins, color='orange', edgecolor='black', alpha=0.8)

# Linhas verticais para média e desvio padrão
plt.axvline(media_grau, color='purple', linestyle='--', linewidth=2, label=f"Média ({media_grau:.2f})")
plt.axvline(media_grau + desvio_grau, color='blue', linestyle=':', linewidth=2, label=f"+1 Desvio ({media_grau + desvio_grau:.2f})")
plt.axvline(media_grau - desvio_grau, color='blue', linestyle=':', linewidth=2, label=f"-1 Desvio ({media_grau - desvio_grau:.2f})")

# Estilo do gráfico
plt.title("Rede GHZ - Histograma de Grau", fontsize=14)
plt.xlabel("Grau", fontsize=12)
plt.ylabel("Número de nós", fontsize=12)
plt.legend()
plt.tight_layout()

# Salvar
plt.savefig("/home/bellx/github/ghz.site/imagens/histograma_grau.png", dpi=300)
plt.close()
print("Histograma gerado e salvo como 'histograma_grau.png'.")
'''

'''
#4.6 Gerar imagem da rede colorida por comunidade (Louvain, com nome do agente principal)
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
from pathlib import Path
import matplotlib.patheffects as path_effects

# Fonte Montserrat
caminho_fonte = "/home/bellx/Montserrat/static/Montserrat-Medium.ttf"
if Path(caminho_fonte).exists():
    font_manager.fontManager.addfont(caminho_fonte)
    plt.rcParams['font.family'] = 'Montserrat'
    print(f"Fonte Montserrat carregada de: {caminho_fonte}")
else:
    print(f"Fonte Montserrat não encontrada em: {caminho_fonte}. Usando fonte padrão do sistema.")

# Gerar paleta de cores
num_comunidades = len(comunidades)
cmap = plt.cm.get_cmap('tab20', num_comunidades)
cores_por_comunidade = {i: cmap(i) for i in range(num_comunidades)}

# Mapear cada nó à cor da comunidade
cor_nodo = {}
lideres_comunidades = []  # para legenda
for i, comunidade in enumerate(comunidades):
    # Determinar o agente principal (maior grau dentro da comunidade)
    no_lider = max(comunidade, key=lambda n: G.degree(n))
    lideres_comunidades.append((i, no_lider))
    for n in comunidade:
        cor_nodo[n] = cores_por_comunidade[i]

# Layout da rede
pos = nx.spring_layout(G, seed=42, k=0.3)
tamanhos = [500 * centralidade[n] + 50 for n in G.nodes()]
cores_nos = [cor_nodo[n] for n in G.nodes()]

# Criar figura e eixo
fig, ax = plt.subplots(figsize=(12, 8))

# Desenhar arestas e nós
nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.25, ax=ax)
nx.draw_networkx_nodes(G, pos, node_color=cores_nos, node_size=tamanhos,
                       alpha=0.9, ax=ax, linewidths=0.5, edgecolors='white')

# Labels: apenas para líderes das comunidades
labels = {no_lider: no_lider for _, no_lider in lideres_comunidades}
labels_pos = {n: (x, y + 0.05) for n, (x, y) in pos.items() if n in labels}

labels_drawn = nx.draw_networkx_labels(
    G, labels_pos, labels=labels, font_size=8, font_color='black',
    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'),
    ax=ax
)
for text in labels_drawn.values():
    text.set_path_effects([
        path_effects.Stroke(linewidth=2, foreground='white'),
        path_effects.Normal()
    ])

# Legenda: "Comunidade + Nome do agente principal" 
for i, no_lider in lideres_comunidades:
    ax.scatter([], [], color=cores_por_comunidade[i],
               label=f"Comunidade {no_lider}")

ax.legend(loc='best', fontsize=8, frameon=True)

# Título e estilo
ax.set_title('Rede GHZ – Comunidades (Louvain, coloridas por agente principal)', fontsize=13, pad=15)
ax.axis('off')
plt.tight_layout()

# Salvar imagem
plt.savefig("/home/bellx/github/ghz.site/imagens/rede_comunidades.png", dpi=300)
plt.close()

print("Imagem 'rede_comunidades.png' gerada com sucesso.")
'''



# 5. Painel HTML das medidas
painel_medidas_html = f"""
<div style="max-width: 800px; margin: 20px auto 40px auto; background: transparent; padding: 25px 30px; 
            border-radius: 8px; font-family: 'Montserrat', sans-serif; font-size: 13px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0); color: #333;">

  <strong style="font-size: 22px; display: block; margin-bottom: 20px;">Medições da Rede</strong>

  <div style="line-height: 1.5; border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
  <strong style = "font-size: 16px;">Propriedades básicas</strong>
  
  <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Medidas que descrevem as características formais da rede.</em>
  </p>
  
  <div style="display: flex; justify-content: space-between; margin-top: 15px;">
    
    <div style="text-align: center;">
      <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/agente.png" alt="Agentes" style="width: 50px; margin-top: 5px; margin-bottom: 5px;">
      <div>Número de agentes primários</div>
      <div style="font-size: 25px; font-weight: bold;">{len(lista_unica_agentes)}</div>
    </div>

    <div style="text-align: center;">
      <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/nos.png" alt="Nós" style="width: 50px; margin-top: 5px;">
      <div>Número de nós</div>
      <div style="font-size: 25px; font-weight: bold;">{num_nodes}</div>
    </div>

    <div style="text-align: center;">
      <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/arestas.png" alt="Arestas" style="width: 50px; margin-top: 5px;">
      <div>Número de arestas</div>
      <div style="font-size: 25px; font-weight: bold;">{num_arestas}</div>
    </div>

    <div style="text-align: center;">
      <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/net.png" alt="Grau" style="width: 50px; margin-top: 5px;">
      <div>Grau médio</div>
      <div style="font-size: 25px; font-weight: bold;">{grau_medio:.3f}</div>
    </div>

    <div style="text-align: center;">
      <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/rede.png" alt="Densidade" style="width: 50px; margin-top: 5px;">
      <div>Densidade</div>
      <div style="font-size: 25px; font-weight: bold;">{densidade:.3f}</div>
    </div>

  </div>
</div>

<div style=" line-height: 1.5; border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
  <strong style = "font-size: 16px;">Estrutura e conectividade</strong>
  
  <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Medidas que mostram como os nós e arestas estão conectados — se a rede é densa, fragmentada ou possui componentes isolados.</em>
  </p>

  <!-- Imagem única ocupando 100% da largura da caixa -->
  <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/componentes.png" alt="Visualização da estrutura da rede" style="width: 100%; border-radius: 4px; margin-bottom: 15px;">

    <!-- Indicadores em formato de texto normal -->
  <p style="margin: 0; color: #333;">
    Componentes desconectados: <style="font-size: 13px;">{comp_desconectados}<br>
    Nós do maior componente: <style="font-size: 13px;">{nos_maior_componente}
  </p>
  <p></p>
  </div>

  <div style="line-height: 1.5; border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
    <strong style = "font-size: 16px;">Centralidade e influência</strong><br>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Medidas que identificam os nós mais importantes ou influentes na rede, com base em sua posição e conexões.</em>
    </p>
    
    <!-- Imagem única ocupando 100% da largura da caixa -->
    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/centralidade_grau_top10.png" alt="top 10 centralidade grau" style="width: 100%; border-radius: 4px; margin-bottom: 15px;">
    Maior centralidade: {maior_no} ({maior_valor:.3f})<br>
    Menor centralidade: {menor_no} ({menor_valor:.3f})
  </div>

  <div style="line-height: 1.5; border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
    <strong style="font-size: 16px;">Betweenness (intermediação)</strong><br>
    
    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Mede quantas vezes um nó aparece nos caminhos mais curtos entre outros nós, indicando se ele atua como ponte ou mediador na comunicação da rede.</em>
    </p>

    <!-- Imagem única ocupando 100% da largura da caixa -->
    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/rede_betweenness.png" alt="betweeenness" style="width: 100%; border-radius: 4px; margin-bottom: 15px;">
    <strong>Top 5</strong><br>
    {"<br>".join([f"{no}: {valor:.4f}" for no, valor in top5])}
  </div>


  <div style="line-height: 1.5; border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
    <strong style = "font-size: 16px;">Closeness (proximidade)</strong><br>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Mede o quão perto um nó está de todos os outros, com base na distância média dos caminhos mais curtos. Quanto maior a proximidade, mais rapidamente o nó pode alcançar os demais na rede.</em>
    </p>

    <!-- Imagem única ocupando 100% da largura da caixa -->
    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/rede_closeness.png" alt="closeness" style="width: 100%; border-radius: 4px; margin-bottom: 15px;">
    <strong>Top 5</strong><br>
    {"<br>".join([f"{no}: {valor:.4f}" for no, valor in top5_closeness])}
  </div>

  <div style="line-height: 1.5; border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
    <strong style="font-size: 16px;">Distribuição de grau</strong><br>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Medidas que descrevem como os graus (número de conexões por nó) variam na rede, revelando desigualdades ou padrões de conectividade.</em>
    </p>

    <!-- Imagem única ocupando 100% da largura da caixa -->
    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/histograma_grau.png" alt="histograma grau versus nós" style="width: 100%; border-radius: 4px; margin-bottom: 15px;">
    Assortatividade: {assortatividade:.3f}<br>
    Média de grau: {media_grau:.2f}<br>
    Variância de grau:{variancia_grau:.2f}
  </div>


  <div style="line-height: 1.5; border: 1px solid #ccc; padding: 15px; margin-bottom: 0; border-radius: 6px; background: #fff; width: 100%;">
    <strong style = "font-size: 16px;">Comunidades</strong><br>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Medidas que analisam como a rede se organiza em grupos densamente conectados internamente e fracamente conectados entre si.</em>
    </p>

    <!-- Imagem única ocupando 100% da largura da caixa -->
    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/rede_comunidades.png" alt="comunidades" style="width: 100%; border-radius: 4px; margin-bottom: 15px;">
    Número de comunidades: {len(comunidades)}<br>
    Modularidade: {modularidade:.3f}
  </div>

   
  <div style="line-height: 1.5; border: 1px solid #ccc; padding: 15px; margin-bottom: 0; border-radius: 6px; background: #fff; width: 100%;">
    <strong style = "font-size: 16px;">Síntese</strong><br>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>A rede de agentes sociais GHZ analisada apresenta uma <strong>dinâmica ampla</strong>, mas <strong>esparsa</strong>, composta por <strong>809 nós</strong>, incluindo 35 agentes primários, e 1.017 conexões. Apesar do <strong>baixo grau médio (2,51)</strong> e da densidade reduzida (0,003), a rede é <strong>quase totalmente conectada</strong>, com 805 nós formando um único componente, o que permite circulação de informações, ainda que de forma desigual entre os agentes.</em>
    </p>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>A centralidade evidencia que nem todos os atores institucionais possuem influência efetiva. A Casa Fluminense surge como hub central, conectando comunidades e controlando fluxos de informação, enquanto atores formais, como o Governo do Rio de Janeiro, apresentam posições periféricas. A análise de betweenness destaca outros intermediadores estratégicos, como Open Knowledge Brasil e DataLabe, que atuam como pontes entre subgrupos, e a proximidade revela nós capazes de alcançar rapidamente a rede, como Open Society Foundations e Fundação Ford, ideais para disseminação de conhecimento.</em>
    </p>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>A rede é desassortativa (-0,523) e apresenta <strong>grande desigualdade de grau</strong>, seguindo padrões de lei de potência: <strong>poucos hubs concentram a maioria das conexões</strong>, enquanto a maioria dos nós permanece periférica. Além disso, a rede organiza-se em 15 comunidades com alta modularidade (0,737), evidenciando <strong>grupos coesos e relativamente isolados</strong>, integrados por hubs estratégicos.</em>
    </p>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Em síntese, a rede combina <strong>comunidades densas com hubs integradores</strong>, nos quais organizações de advocacy e conhecimento aberto assumem papel central, enquanto atores institucionais formais ocupam posições periféricas. A configuração sugere que a difusão de informação e a coordenação social dependem fortemente de um pequeno conjunto de agentes estratégicos, capazes de conectar, integrar e dinamizar toda a rede.</em>
    </p>
  </div> 

</div>
"""

painel_analises_html = f"""
<div style="max-width: 800px; margin: 20px auto 40px auto; background: transparent; padding: 25px 30px; 
            border-radius: 8px; font-family: 'Montserrat', sans-serif; font-size: 13px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0); color: #333;">

  <strong style="font-size: 22px; display: block; margin-bottom: 20px;">Interpretações e Contexto</strong>

  <div style="line-height: 1.5; border: 1px solid #ccc; padding: 15px; 
              margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
    
    <strong style="font-size: 16px;">Atuação no território</strong>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
      <em>Mapeamento das áreas de atuação dos agentes primários.</em>
    </p>
    
    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/atuacao-com-legenda/geral.png" 
         alt="mapa-geral" 
         style="width: 100%; border-radius: 0px; margin-top: 10px">

    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/atuacao-com-legenda/zoom-centroo.png" 
         alt="mapa-zoom1" 
         style="width: 100%; border-radius: 0px; margin-top: 10px;">

    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/atuacao-com-legenda/zoom-nordes.png" 
         alt="mapa-zoom2" 
         style="width: 100%; border-radius: 0px; margin-top: 10px;">

    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/atuacao-com-legenda/zoom-norte.png" 
         alt="mapa-zoom3" 
         style="width: 100%; border-radius: 0px; margin-top: 10px;">

    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/atuacao-com-legenda/zoom-sp.png" 
         alt="mapa-zoom4" 
         style="width: 100%; border-radius: 0px; margin-top: 10px;">                    

  </div>

  <div style="line-height: 1.5; border: 1px solid #ccc; padding: 15px; 
              margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
    
    <strong style="font-size: 16px;">Financiadores</strong>
    
    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
      <em>Agentes primários e seus financiadores.</em>
    </p>
    
    <iframe src="financiadores_rede.html" width="100%" height="600" style="border: none;"></iframe>

  </div>
  
  <div style="line-height: 1.5; border: 1px solid #ccc; padding: 15px; 
              margin-bottom: 20px; border-radius: 6px; background: #fff; width: 100%;">
    
    <strong style="font-size: 16px;">Mapeamento temático dos agentes</strong>
    
    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
      <em>Identificação de correspondências entre agentes e campos temáticos</em>
    </p>
    
    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/temas.gif" 
         alt="temas-atuacao" 
         style="width: 100%; border-radius: 4px; margin-top: 10px;">

  </div>

  <div style="line-height: 1.5; border: 1px solid #ccc; padding: 15px; margin-bottom: 0; border-radius: 6px; background: #fff; width: 100%;">
    <strong style = "font-size: 16px;">Síntese</strong><br>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Além dos aspectos quantitativos da rede GHZ, interessa-nos também examinar elementos contextuais e interpretativos, resultantes de estudos territoriais e das dinâmicas sociais e inter-relacionais entre os nós que a compõem. Considerando que nosso campo de estudo é o urbanismo e tecnologia e que um dos objetivos centrais consiste em identificar e analisar uma rede voltada à troca de informações para a formulação de políticas públicas urbanas, é fundamental visualizar a <strong>presença territorial dos agentes primários</strong>. A partir de pesquisa em relatórios e sites oficiais, coletamos informações sobre os locais de sede e os territórios de atuação dos projetos de cada agente. O mapa temático produzido, acompanhado de imagens em diferentes níveis de zoom, evidencia uma <strong>forte concentração de agentes na região Sudeste</strong>, sobretudo nos estados de São Paulo e Rio de Janeiro. Contudo, observamos também a <strong>presença de agentes nas demais macrorregiões do país</strong> e, em alguns casos, até mesmo além das fronteiras nacionais, demonstrando que <strong>a rede possui alcance efetivamente nacional</strong>.</em>
    </p>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>O segundo aspecto analisado diz respeito à dinâmica existente entre os <strong>agentes e seus financiadores</strong>. Para isso, modelamos uma rede composta tanto pelos agentes quanto pelas entidades responsáveis por seu apoio financeiro, observando que alguns atores desempenham o papel de financiadores de diversos agentes analisados, concentrando, assim, diferentes níveis de poder e influência. Considerando nosso interesse em examinar os fenômenos sob uma perspectiva decolonial, foi igualmente relevante mapear as <strong>origens desses financiamentos</strong>. Por meio de diferenciação cromática, é possível distinguir na rede os financiadores nacionais dos internacionais. Os dados indicam que <strong>aproximadamente metade desses financiadores têm origem fora do Brasil</strong>, o que nos leva a refletir sobre o grau de influência que organismos internacionais exercem na governança de dados em nosso país e quais os seus interesses em fomentar tais agentes. </em>
    </p>

    <p style="margin-top: 10px; margin-bottom: 15px; color: #555;">
    <em>Por fim, com o objetivo de compreender mais profundamente as <strong>áreas temáticas de atuação</strong> dos agentes primários, realizamos uma análise das descrições institucionais disponibilizadas em seus sites, buscando identificar temas e campos de atuação recorrentes. Utilizamos ferramentas de inteligência artificial que, a partir de textos de até 400 palavras, permitiram reconhecer <strong>categorias temáticas compartilhadas</strong> entre os agentes. Após diversos processos de calibração e ajustes, foram identificados dez grandes temas que sintetizam seus principais interesses e áreas de atuação. Observamos uma forte presença de aspectos relacionados à <strong>justiça social e climática</strong>, bem como à defesa de pautas minoritárias, que constituem fundamentos centrais da atuação desses agentes.</em>
    </p>

  </div> 

  
</div>
"""




# 6. Carregar header e footer
with open("header.html", "r", encoding="utf-8") as h:
    header_html = h.read()

with open("footer.html", "r", encoding="utf-8") as f:
    footer_html = f.read()

# 7. Injetar painel entre header e footer
html_final = f"""
{header_html}
{painel_medidas_html}
{painel_analises_html}
{footer_html}
"""


# Adiciona CSS para fundo com opacidade
css_fundo = """
<style>
  body {
    background: 
      linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), 
      url('https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/fundo-pag-medidas.gif') no-repeat center center fixed;
    background-size: cover;
    margin: 0;
    padding: 0;
    font-family: 'Montserrat', sans-serif;
  }
</style>
</head>
"""

# Substitui o fechamento </head> pelo CSS + fechamento
html_final = html_final.replace("</head>", css_fundo)


# 8. Salvar o HTML
with open("medidas-rede.html", "w", encoding="utf-8") as f:
    f.write(html_final)

print("Arquivo 'medidas-rede.html'")
