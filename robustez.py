from pathlib import Path
import csv
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import json


# (opcional) reprodutibilidade
random.seed(42)
np.random.seed(42)


# 1. Leitura do CSV
def carregar_rede(caminho):
    edge_list = []
    tipos_conexao = []

    with open(caminho, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            origem = row[0]
            destino = row[2]
            tipo = row[8].strip().lower()

            edge_list.append((origem, destino))
            tipos_conexao.append(tipo)

    return edge_list, tipos_conexao


# 2. Construção do grafo
def construir_grafo(edge_list):
    G = nx.from_edgelist(edge_list)
    return G


# 3. Métricas da rede
def calcular_metricas(G):
    metricas = {}

    metricas["num_nodes"] = G.number_of_nodes()
    metricas["num_edges"] = G.number_of_edges()
    metricas["densidade"] = nx.density(G)

    graus = dict(G.degree())
    metricas["grau_medio"] = sum(graus.values()) / len(graus)

    # componente gigante
    metricas["maior_componente"] = len(max(nx.connected_components(G), key=len))

    # centralidades
    degree_centrality = nx.degree_centrality(G)
    metricas["maior_centralidade"] = max(degree_centrality, key=degree_centrality.get)

    # betweenness (top 5)
    bet = nx.betweenness_centrality(G)
    metricas["top5_betweenness"] = sorted(bet.items(), key=lambda x: x[1], reverse=True)[:5]

    # assortatividade
    metricas["assortatividade"] = nx.degree_assortativity_coefficient(G)

    return metricas


# 4. Funções de robustez
def remover_nos_aleatorios(G, frac):
    G_copy = G.copy()
    num_remove = int(frac * G.number_of_nodes())

    if num_remove > 0:
        nos = random.sample(list(G.nodes()), num_remove)
        G_copy.remove_nodes_from(nos)

    return G_copy


def remover_hubs(G, frac):
    G_copy = G.copy()
    graus = dict(G.degree())

    ordenados = sorted(graus, key=graus.get, reverse=True)
    num_remove = int(frac * G.number_of_nodes())

    G_copy.remove_nodes_from(ordenados[:num_remove])

    return G_copy


def tamanho_maior_componente(G):
    if G.number_of_nodes() == 0:
        return 0
    return len(max(nx.connected_components(G), key=len))


# 5. Simulação de robustez (múltiplas execuções)
def simular_robustez_multiplas(G, n_sim=50):
    fracoes = np.linspace(0, 0.5, 15)

    resultados_random = []
    resultados_hub = []

    for _ in range(n_sim):
        rand = []
        hub = []

        for f in fracoes:
            G_rand = remover_nos_aleatorios(G, f)
            G_hub = remover_hubs(G, f)

            rand.append(tamanho_maior_componente(G_rand))
            hub.append(tamanho_maior_componente(G_hub))

        resultados_random.append(rand)
        resultados_hub.append(hub)

    # média
    media_random = np.mean(resultados_random, axis=0)
    media_hub = np.mean(resultados_hub, axis=0)

    # desvio padrão
    std_random = np.std(resultados_random, axis=0)
    std_hub = np.std(resultados_hub, axis=0)

    return fracoes, media_random, media_hub, std_random, std_hub


# 6. Plot dos resultados
def plotar_resultados(fracoes, rand, hub, std_rand=None, std_hub=None):
    plt.figure(figsize=(14, 8))

    #PT
    #plt.plot(fracoes, rand, label='Falha aleatória (média)', marker='o')
    #plt.plot(fracoes, hub, label='Ataque direcionado (hubs)', marker='s')

    #EN
    plt.plot(fracoes, rand, label='Random failure (mean)', marker='o')
    plt.plot(fracoes, hub, label='Targeted attack (hubs)', marker='s')

    # faixa de incerteza
    if std_rand is not None:
        plt.fill_between(fracoes, rand - std_rand, rand + std_rand, alpha=0.2)

    if std_hub is not None:
        plt.fill_between(fracoes, hub - std_hub, hub + std_hub, alpha=0.2)

    #PT
    #plt.xlabel('Fração de nós removidos')
    #plt.ylabel('Tamanho da maior componente')
    #plt.title('Robustez da Rede (média de simulações)')

    #EN
    plt.xlabel('Fraction of nodes removed')
    plt.ylabel('Largest connected component size')
    plt.title('Network robustness (mean over 50 simulations)')

    plt.legend()
    plt.grid(True)
    plt.show()


# 7. Execução principal
if __name__ == "__main__":
    caminho_csv = "./R02_Arestas.csv"

    edge_list, tipos = carregar_rede(caminho_csv)
    G = construir_grafo(edge_list)

    # métricas
    metricas = calcular_metricas(G)

    print("\n=== MÉTRICAS DA REDE ===")
    for k, v in metricas.items():
        print(f"{k}: {v}")

    # salvar métricas
    with open("metricas.json", "w") as f:
        json.dump(metricas, f, indent=4)

    # robustez com múltiplas simulações
    fracoes, rand, hub, std_rand, std_hub = simular_robustez_multiplas(G, n_sim=50)

    # plot
    plotar_resultados(fracoes, rand, hub, std_rand, std_hub)