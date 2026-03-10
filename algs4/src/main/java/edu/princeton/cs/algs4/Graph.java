package edu.princeton.cs.algs4;

import java.util.NoSuchElementException;

public class Graph {
    private static final String NEWLINE = System.getProperty("line.separator");

    private final int V;
    private int E;
    private Bag<Integer>[] adj;

    public Graph(int V) {
        if (V < 0) throw new IllegalArgumentException("Number of vertices must be non-negative");
        this.V = V;
        this.E = 0;
        adj = (Bag<Integer>[]) new Bag[V];
        for (int v = 0; v < V; v++) {
            adj[v] = new Bag<Integer>();
        }
    }

    public Graph(In in) {
        if (in == null) throw new IllegalArgumentException("argument is null");
        try {
            this.V = in.readInt();
            if (V < 0) throw new IllegalArgumentException("number of vertices in a Graph must be non-negative");
            adj = (Bag<Integer>[]) new Bag[V];
            for (int v = 0; v < V; v++) {
                adj[v] = new Bag<Integer>();
            }
            int E = in.readInt();
            if (E < 0) throw new IllegalArgumentException("number of edges in a Graph must be non-negative");
            for (int i = 0; i < E; i++) {
                int v = in.readInt();
                int w = in.readInt();
                validateVertex(v);
                validateVertex(w);
                addEdge(v, w);
            }
        }
        catch (NoSuchElementException e) {
            throw new IllegalArgumentException("invalid input format in Graph constructor", e);
        }
    }

    public Graph(Graph graph) {
        this.V = graph.V();
        this.E = graph.E();
        adj = (Bag<Integer>[]) new Bag[V];

        for (int v = 0; v < V; v++) {
            adj[v] = new Bag<Integer>();
        }

        for (int v = 0; v < graph.V(); v++) {
            Stack<Integer> reverse = new Stack<Integer>();
            for (int w : graph.adj[v]) {
                reverse.push(w);
            }
            for (int w : reverse) {
                adj[v].add(w);
            }
        }
    }

    public int V() { return V; }
    public int E() { return E; }

    private void validateVertex(int v) {
        if (v < 0 || v >= V)
            throw new IllegalArgumentException("vertex " + v + " is not between 0 and " + (V-1));
    }

    public void addEdge(int v, int w) {
        validateVertex(v);
        validateVertex(w);
        E++;
        adj[v].add(w);
        adj[w].add(v);
    }

    public Iterable<Integer> adj(int v) {
        validateVertex(v);
        return adj[v];
    }

    public int degree(int v) {
        validateVertex(v);
        return adj[v].size();
    }

    public String toString() {
        StringBuilder s = new StringBuilder();
        s.append(V + " vertices, " + E + " edges " + NEWLINE);
        for (int v = 0; v < V; v++) {
            s.append(v + ": ");
            for (int w : adj[v]) {
                s.append(w + " ");
            }
            s.append(NEWLINE);
        }
        return s.toString();
    }

    public String toDot() {
        StringBuilder s = new StringBuilder();
        s.append("graph {" + NEWLINE);
       s.append("node[shape=circle, style=filled, fixedsize=true, width=0.3, fontsize=\"10pt\"];" + NEWLINE);


        int selfLoops = 0;

        for (int v = 0; v < V; v++) {
            for (int w : adj[v]) {
                if (v < w) {
                    s.append(v + " -- " + w + NEWLINE);
                }
                else if (v == w) {
                    if (selfLoops % 2 == 0) {
                        s.append(v + " -- " + w + NEWLINE);
                    }
                    selfLoops++;
                }
            }
        }
        s.append("}" + NEWLINE);
        return s.toString();
    }

   public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Uso: java Graph <caminho_do_arquivo_txt>");
            return;
        }

        // 1. Carrega o grafo do arquivo TXT passado pelo .bat
        In in = new In(args[0]);
        Graph graph = new Graph(in);

        // 2. Lógica de Caminho Portátil
        // Pegamos o caminho do arquivo de entrada (ex: graphs\grafo_formatado.txt)
        java.io.File arquivoEntrada = new java.io.File(args[0]);
        
        // Pegamos a pasta onde esse arquivo está (a pasta "graphs")
        String pastaPai = arquivoEntrada.getParent(); 
        
        // Criamos o novo caminho para o arquivo .dot na mesma pasta
        // Se pastaPai for nulo (arquivo na raiz), usamos apenas o nome
        String caminhoDot = (pastaPai != null) ? 
                            pastaPai + java.io.File.separator + "grafo_full.dot" : 
                            "grafo_full.dot";

        System.out.println("Gerando DOT em: " + caminhoDot);
        
        // 3. Gera o arquivo
        graph.toDotFull(caminhoDot);

        System.out.println("DOT full gerado com sucesso!");
    }

    public void salvarEmArquivo(String caminhoArquivo) {
        try {
            java.io.FileWriter writer = new java.io.FileWriter(caminhoArquivo);
            writer.write(this.toString());
            writer.close();
        } catch (java.io.IOException e) {
            e.printStackTrace();
        }
    }
    public void toDotFull(String filename) {
    try (java.io.PrintWriter out = new java.io.PrintWriter(filename)) {
        out.println("graph G {");
        out.println("layout=sfdp;");
        out.println("overlap=false;");
        out.println("node[shape=circle, width=0.25, height=0.25, fontsize=8];");

        for (int v = 0; v < V; v++) {
            for (int w : adj[v]) {
                if (w > v) {
                    out.println(v + " -- " + w + ";");
                }
            }
        }

        out.println("}");
    } catch (java.io.IOException e) {
        e.printStackTrace();
    }
    }

}
