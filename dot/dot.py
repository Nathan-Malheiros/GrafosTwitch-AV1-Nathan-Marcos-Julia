import networkx as nx
import pydot
# Caminhos dos seus arquivos
caminho_entrada = r"graphs\grafo_full.dot"
caminho_saida = r"graphs\grafo_curto.dot"

print("Lendo o arquivo e pegando apenas os primeiros 1.000 dados (amostra reduceida)...")

try:
    with open(caminho_entrada, 'r', encoding='utf-8') as original:
        with open(caminho_saida, 'w', encoding='utf-8') as novo:
            contador = 0
            for linha in original:
                # Escreve a linha no novo arquivo
                novo.write(linha)
                
                # Se a linha tiver uma conexão (-> ou --), a gente conta
                if '--' in linha or '->' in linha:
                    contador += 1
                
                # Quando chegar em 1.000, para tudo e fecha o grafo
                if contador >= 1000:
                    novo.write("\n}") # Garante que o arquivo feche certinho
                    break
                    
    print(f"Pronto! O arquivo 'grafo_curto.dot' foi criado com {contador} conexões.")
    print("Atenção: esta é apenas uma amostra de 1.000 arestas para viabilizar a execução do Graphviz.")

except Exception as e:
    print(f"Erro: {e}")