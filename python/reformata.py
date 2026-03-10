import csv

def csv_to_algs4(input_file, output_file):
    edges = []
    unique_ids = set()
    with open(input_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            v = int(row["numeric_id_1"])
            w = int(row["numeric_id_2"])
            edges.append((v, w))
            unique_ids.add(v)
            unique_ids.add(w)

    # Mapeia IDs grandes para 0..V-1
    id_to_index = {node_id: idx for idx, node_id in enumerate(sorted(unique_ids))}

    V = len(unique_ids)
    E = len(edges)

    # Escreve no formato algs4
    with open(output_file, 'w') as f:
        f.write(f"{V}\n")
        f.write(f"{E}\n")
        for v, w in edges:
            f.write(f"{id_to_index[v]} {id_to_index[w]}\n")

    print("Conversão concluída!")
    print(f"Vértices: {V}")
    print(f"Arestas: {E}")



if __name__ == "__main__":
    csv_to_algs4("data\\entrada.csv", "graphs\\grafo_formatado.txt")