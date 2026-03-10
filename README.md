# Análise e Visualização de Grafos

Este projeto realiza o **processamento, análise e visualização de grafos grandes** a partir de um dataset em formato **CSV**.

O sistema utiliza uma combinação de ferramentas:

* **Python** → pré-processamento e análise do grafo
* **Java (algs4)** → manipulação da estrutura de dados do grafo
* **Graphviz** → geração de visualizações
* **Batch Scripts (.bat)** → automação do pipeline

---

# 📦 Requisitos

Antes de executar o projeto, instale os seguintes softwares.

## 1️⃣ Python

Instale **Python 3.10 ou superior**.

Download:

https://www.python.org/downloads/

Durante a instalação marque a opção:

```
Add Python to PATH
```

Depois verifique no terminal:

```
python --version
```

ou

```
py --version
```

---

# 📚 Bibliotecas Python

Instale as dependências com **pip**.

Execute no terminal:

```
pip install numpy
pip install matplotlib
pip install networkx
pip install powerlaw
pip install pydot
```

Essas bibliotecas são usadas para:

| Biblioteca | Função                               |
| ---------- | ------------------------------------ |
| numpy      | operações matemáticas e estatísticas |
| matplotlib | geração de gráficos                  |
| networkx   | manipulação de grafos                |
| powerlaw   | análise de distribuição de grau      |
| pydot      | integração com Graphviz              |

---

# 🧠 Instalação do Graphviz

O **Graphviz** é usado para gerar a visualização do grafo.

Download:

https://graphviz.org/download/

Instale a versão para **Windows**.

Normalmente o executável ficará em:

```
C:\Program Files (x86)\Graphviz\bin
```

ou

```
C:\Program Files\Graphviz\bin
```

Verifique a instalação:

```
dot -V
```

ou

```
sfdp -V
```

Se aparecer a versão, o Graphviz está instalado corretamente.

---

# 📁 Estrutura do Projeto

Estrutura típica do projeto:

```
Projeto-Grafos
│
├── data
│   └── entrada.csv
│
├── graphs
│   ├── grafo_formatado.txt
│   ├── grafo_full.dot
│   ├── grafo_curto.dot
│   └── PDF
│        └── resultado_teste.pdf
│
├── python
│   ├── reformata.py
│   └── histograma.py
│
├── dot
│   └── dot.py
│
├── algs4
│   └── biblioteca Java (Sedgewick)
│
├── clear.bat
├── executar.bat
└── gerarvisualgrafo.bat
```

---

# ⚙️ Pipeline do Sistema

O processamento do grafo segue o fluxo abaixo:

```
CSV (dataset)
     ↓
reformata.py
     ↓
grafo_formatado.txt
     ↓
Java algs4
     ↓
grafo_full.dot
     ↓
dot.py
     ↓
grafo_curto.dot
     ↓
Graphviz
     ↓
PDF / PNG
```

Descrição das etapas:

1. O **CSV** contendo as arestas do grafo é carregado.
2. O script **reformata.py** converte o dataset para o formato usado pela biblioteca `algs4`.
3. O **Java** processa o grafo.
4. Um arquivo `.dot` é gerado.
5. O script **dot.py** cria uma versão reduzida do grafo.
6. O **Graphviz** gera a visualização final.

---

# ▶️ Como Executar

## Limpar arquivos gerados

Remove arquivos intermediários do projeto:

```
clear.bat
```

---

## Executar pipeline completo

Executa todo o processamento do grafo:

```
executar.bat
```

Esse script realiza automaticamente:

1. limpeza do projeto
2. execução do Python
3. compilação do Java
4. geração do `.dot`
5. análise do grafo

---

## Gerar visualização do grafo

Para gerar um **PDF com a visualização do grafo reduzido**, execute:

```
gerarvisualgrafo.bat
```

O arquivo será salvo em:

```
graphs/PDF/resultado_teste.pdf
```

---

# 📊 Visualização do Grafo

Grafos muito grandes podem possuir **milhões de arestas**, o que torna impossível gerar uma visualização completa.

Por isso o projeto cria uma **amostra do grafo**.

Exemplo:

```
grafo_full.dot  → grafo completo
grafo_curto.dot → amostra do grafo
```

Essa amostra permite gerar uma visualização sem travar o Graphviz.

O layout utilizado é:

```
SFDP (Scalable Force Directed Placement)
```

Esse algoritmo é otimizado para **redes grandes**.

---

# ⚠️ Possíveis Problemas

## Python não encontrado

Reinstale o Python e marque:

```
Add Python to PATH
```

---

## Graphviz não encontrado

Verifique se o caminho está correto:

```
C:\Program Files (x86)\Graphviz\bin
```

---

## Visualização demora muito

Isso ocorre quando o grafo possui muitas arestas.

Utilize sempre a versão reduzida:

```
grafo_curto.dot
```

---

# 🎓 Aplicações do Projeto

Este sistema pode ser usado para:

* análise de **redes complexas**
* estudo de **distribuição de grau**
* detecção de **power-law**
* experimentos acadêmicos com grafos
* projetos de **pesquisa e iniciação científica**

---

# 👨‍💻 Autor

Projeto desenvolvido para **estudos de análise de grafos e redes complexas**, integrando Python, Java e Graphviz para processamento e visualização de grandes datasets.
