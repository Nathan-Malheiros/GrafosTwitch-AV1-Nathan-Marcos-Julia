import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import powerlaw
import networkx as nx

# ================================
# Caminho do arquivo .dot
# ================================
DOT_PATH = r"graphs\grafo_full.dot"

with open(DOT_PATH, 'r', encoding='utf-8') as file:
    raw_lines = [l.strip() for l in file if l.strip()]

def parse_edge(line):
    if "--" in line:
        parts = line.split("--")
        a = parts[0].strip()
        b = parts[1].strip().rstrip(';')
        return a, b
    return None

# ================================
# Mapear nós e Calcular Graus (Otimizado para não dar MemoryError)
# ================================
node_index = {}
next_idx = 0
degrees_map = {} # Usaremos um dicionário para contar graus sem criar listas gigantes

print("[INFO] Processando graus do grafo (Streaming)...")

with open(DOT_PATH, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if "--" in line:
            # Parse direto da linha sem guardar na lista
            parts = line.split("--")
            a = parts[0].strip()
            b = parts[1].strip().rstrip(';')
            
            # Contagem de graus direta
            degrees_map[a] = degrees_map.get(a, 0) + 1
            degrees_map[b] = degrees_map.get(b, 0) + 1

# Transforma os valores do dicionário em um array numpy para o restante do código
degrees = np.array(list(degrees_map.values()))
degrees = degrees[degrees > 0] 

print(f"[OK] Graus calculados para {len(degrees):,} nós.")
# ================================
# Cálculo da Densidade
# ================================

N = len(degrees_map)      # número de vértices
sum_degrees = degrees.sum()

E = sum_degrees / 2       # número de arestas

density = (2 * E) / (N * (N - 1))

print("\n--- Métricas da Rede ---")
print(f"Vértices (N): {N}")
print(f"Arestas (E): {int(E)}")
print(f"Densidade: {density:.8f}")

#=================================
# Clustering
#=================================

G = nx.Graph()

with open("graphs\grafo_full.dot", "r", encoding="utf-8") as file:
    for line in file:
        if "--" in line:
            a, b = line.split("--")
            a = a.strip()
            b = b.strip().rstrip(";")

            G.add_edge(a, b)

clustering = nx.approximation.average_clustering(G, trials=1000)

print("Clustering médio aproximado:", clustering)
# ================================
# Ajuste Power Law
# ================================
xmax = degrees.max()
fit = powerlaw.Fit(degrees, discrete=True)
alpha = fit.power_law.alpha
xmin = fit.power_law.xmin
k_limite_ruido = xmax / 2  

print(f"Alpha (α): {alpha:.4f}")
print(f"xmin: {xmin}")

# ================================
# Histograma manual (Dados Reais)
# ================================
degree_count = Counter(degrees)
graus = np.array(sorted(degree_count.keys()))
frequencias = np.array([degree_count[g] for g in graus])
pk = frequencias / np.sum(frequencias)

# Filtramos apenas para visualização log-log
log_k = np.log10(graus)
log_pk = np.log10(pk)

# ================================
# Curva Teórica (Ajuste de Escala)
# ================================
# --- ALTERAÇÃO 2: Normalização Discreta e Escala ---
# Geramos k_vals apenas até o limite do ruído, como na Figura 2
k_vals = np.linspace(xmin, k_limite_ruido, 100)

# Para a reta coincidir com os pontos azuis, multiplicamos a PDF teórica 
# pela fração de nós que estão na cauda (k >= xmin)
fracao_cauda = np.sum(degrees >= xmin) / len(degrees)
pdf_teorica = fit.power_law.pdf(k_vals)

log_k_vals = np.log10(k_vals)
log_powerlaw = np.log10(pdf_teorica * fracao_cauda)


# ================================
# Estatísticas Descritivas
# ================================
def imprimir_estatisticas(degrees):
    print("\n--- Estatísticas da Distribuição de Graus ---")
    print(f"Número total de nós (com grau > 0): {len(degrees)}")
    print(f"Grau Máximo (k_max): {np.max(degrees)}")
    print(f"Grau Mínimo (k_min): {np.min(degrees)}")
    print(f"Grau Médio (<k>): {np.mean(degrees):.2f}")
    print(f"Mediana do Grau: {np.median(degrees)}")
    print(f"Desvio Padrão: {np.std(degrees):.2f}")
    
    # Coeficiente de Gini (Mede desigualdade na conectividade)
    sorted_degrees = np.sort(degrees)
    n = len(degrees)
    index = np.arange(1, n + 1)
    gini = ((np.sum((2 * index - n  - 1) * sorted_degrees)) / (n * np.sum(sorted_degrees)))
    print(f"Coeficiente de Gini: {gini:.4f} (0=igualdade, 1=extrema desigualdade)")

imprimir_estatisticas(degrees)

# ================================
# Comparação de Modelos (Relação de Verossimilhança)
# ================================
R, p = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
print(f"\n--- Comparação de Modelos ---")
print(f"Power Law vs. Exponencial: R={R:.2f}, p-value={p:.4f}")
if R > 0 and p < 0.05:
    print("Resultado: A Lei de Potência é o melhor ajuste.")
else:
    print("Resultado: Não há evidência estatística de que seja Lei de Potência pura.")

# Interpretação do Alpha
def interpretar_alpha(a):
    print(f"\n--- Interpretação do Expoente α ({a:.2f}) ---")
    if 2 < a < 3:
        print("Regime 'Scale-Free': O grafo é ultra-pequeno. Hubs dominam a topologia.")
    elif a <= 2:
        print("Regime de Hubs Anômalos: O maior nó cresce com o tamanho da rede.")
    else:
        print("Decaimento Rápido: A rede se comporta de forma mais similar a uma rede aleatória.")

interpretar_alpha(alpha)

# ================================
# Plot Final
# ================================
plt.figure(figsize=(9, 6))

# Pontos azuis originais (conforme solicitado)
plt.scatter(log_k, log_pk, color='#377eb8', label='Dados reais', alpha=0.7, s=30)

# Ajuste teórico corrigido e limitado
plt.plot(log_k_vals, log_powerlaw,
         color='#e41a1c', 
         linestyle='--',
         linewidth=2.5,
         label=f'Ajuste Power Law (α={alpha:.2f})')

plt.xlabel('log10(k)')
plt.ylabel('log10(P(k))')
plt.title('Distribuição de Grau: Ajuste vs. Ruído Estatístico')

plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.tight_layout()


# Defina o caminho completo com o nome do arquivo e a extensão
caminho_saida = r"output\distribuicao_final.png"

# Salva o arquivo (o parâmetro bbox_inches='tight' garante que nada seja cortado)
plt.savefig(caminho_saida, dpi=300, bbox_inches='tight')

print(f"Gráfico salvo com sucesso em: {caminho_saida}")
plt.show()

def plotar_histogramas(degrees):
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))

    # 1. Histograma de Frequência Absoluta
    ax[0].hist(degrees, bins=50, color='#4daf4a', edgecolor='black', alpha=0.7)
    ax[0].set_title('Histograma de Frequência Absoluta')
    ax[0].set_xlabel('Grau (k)')
    ax[0].set_ylabel('Frequência (Contagem)')
    ax[0].grid(axis='y', linestyle='--', alpha=0.6)

    # 2. Histograma Normalizado (Densidade de Probabilidade)
    ax[1].hist(degrees, bins=50, density=True, color='#984ea3', edgecolor='black', alpha=0.7)
    ax[1].set_yscale('log')
    ax[1].set_title('Histograma Normalizado (Escala Log Y)')
    ax[1].set_xlabel('Grau (k)')
    ax[1].set_ylabel('P(k)')
    ax[1].grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()

    # --- PARTE ADICIONADA PARA SALVAR ---
    caminho_histograma = r"output\histogramas_analise.png"
    plt.savefig(caminho_histograma, dpi=300, bbox_inches='tight')
    print(f"Gráfico de histogramas salvo em: {caminho_histograma}")
    # ------------------------------------

    plt.show()

# Chama a função (os prints e salvamento ocorrerão aqui)
plotar_histogramas(degrees)
# ==========================================================
# SEÇÃO FINAL: ESTATÍSTICAS, COMPARAÇÃO E QUADRO DE RESUMO
# ==========================================================

def imprimir_estatisticas(degrees):
    """Calcula métricas descritivas e retorna o Coeficiente de Gini."""
    print("\n--- Estatísticas da Distribuição de Graus ---")
    k_max = np.max(degrees)
    k_min = np.min(degrees)
    k_med = np.mean(degrees)
    k_median = np.median(degrees)
    k_std = np.std(degrees)

    print(f"Número total de nós (com grau > 0): {len(degrees):,}")
    print(f"Grau Máximo (k_max): {k_max}")
    print(f"Grau Mínimo (k_min): {k_min}")
    print(f"Grau Médio (<k>): {k_med:.2f}")
    print(f"Mediana do Grau: {k_median}")
    print(f"Desvio Padrão: {k_std:.2f}")
    
    # Cálculo do Coeficiente de Gini
    sorted_degrees = np.sort(degrees)
    n = len(degrees)
    index = np.arange(1, n + 1)
    # Fórmula de Gini para dados discretos
    gini_calculado = ((np.sum((2 * index - n - 1) * sorted_degrees)) / (n * np.sum(sorted_degrees)))
    print(f"Coeficiente de Gini: {gini_calculado:.4f} (0=igualdade, 1=extrema desigualdade)")
    
    return gini_calculado

def gerar_quadro_resumo(degrees, alpha, xmin, R, p, gini):
    """Gera uma imagem 'Dashboard' com o resumo técnico da análise."""
    
    # Configuração da figura (sem eixos para parecer um documento)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')
    
    # Lógica de interpretação topológica
    regime = ""
    if 2 < alpha < 3: 
        regime = "Scale-Free (Hubs dominantes)"
    elif alpha <= 2: 
        regime = "Hubs Anômalos (Crescimento extremo)"
    else: 
        regime = "Decaimento Rápido (Rede Aleatória/Exponencial)"
    
    melhor_modelo = "Lei de Potência" if (R > 0 and p < 0.05) else "Outras (Exponencial/Log-normal)"
    conclusao_robusta = "Robusta a falhas aleatórias" if alpha > 2 else "Vulnerável a ataques direcionados"

    # Conteúdo do Quadro
    conteudo = (
        "======================================================================\n"
        "          RESUMO DA ANÁLISE DO GRAFO (SOCIAL NETWORKS - TWITCH)     \n"
        "======================================================================\n\n"
        "1. MÉTRICAS DE CONECTIVIDADE:\n"
        f"   - Total de Nós Ativos: {len(degrees):,}\n"
        f"   - Grau Máximo (k_max): {np.max(degrees):,}\n"
        f"   - Grau Médio (<k>): {np.mean(degrees):.2f}\n"
        f"   - Coeficiente de Gini: {gini:.4f}\n\n"
        "2. AJUSTE DE LEI DE POTÊNCIA (Power Law):\n"
        f"   - Expoente Alpha (α): {alpha:.4f}\n"
        f"   - Valor Mínimo (xmin): {xmin}\n"
        f"   - Melhor Ajuste: {melhor_modelo}\n"
        f"   - P-value: {p:.4f}\n\n"
        "3. INTERPRETAÇÃO TOPOLÓGICA:\n"
        f"   - Regime: {regime}\n"
        f"   - Estabilidade: {conclusao_robusta}\n\n"
        "==================================================\n"
        "Gerado automaticamente - Python\n"
        "=================================================="
    )

    # Renderização do texto na imagem
    plt.text(0.5, 0.5, conteudo, 
             horizontalalignment='center', 
             verticalalignment='center', 
             fontsize=11, family='monospace',
             bbox=dict(facecolor='#f9f9f9', alpha=1, edgecolor='#377eb8', boxstyle='round,pad=1'))

    # Salvamento
    caminho_resumo = r"output\analise_texto_resumo.png"
    plt.savefig(caminho_resumo, dpi=300, bbox_inches='tight')
    
    print(f"\n[OK] Dashboard de resumo salvo em: {caminho_resumo}")
    plt.show()

# --- EXECUÇÃO FINALIZADA ---

# 1. Calcula estatísticas e captura o Gini
gini_final = imprimir_estatisticas(degrees)

# 2. Executa interpretações extras (já existentes no seu código)
interpretar_alpha(alpha)

# 3. Plota os histogramas (já existente no seu código)
plotar_histogramas(degrees)

# 4. Gera o quadro final (Dashboard) usando o Gini capturado
gerar_quadro_resumo(degrees, alpha, xmin, R, p, gini_final)

print("\n>>> Processamento Completo. Todas as saídas foram salvas na pasta 'output'.")