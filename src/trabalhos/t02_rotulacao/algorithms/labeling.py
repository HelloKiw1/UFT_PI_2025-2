from __future__ import annotations
import numpy as np

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x: int) -> int:
        # path compression
        if self.parent.get(x, x) != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent.get(x, x)

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            # une pelo menor id para ter rótulos mais “compactos”
            if ra < rb:
                self.parent[rb] = ra
            else:
                self.parent[ra] = rb

def connected_components(binary: np.ndarray, connectivity: int = 4) -> tuple[np.ndarray, int]:
    """
    Rotulação de componentes conectadas (duas passagens) em imagem binária {0,1}.
    - connectivity: 4 ou 8
    Retorna:
      labels: (H,W) int32 com rótulos {0=background, 1..K}
      K: número de componentes
    """
    assert connectivity in (4, 8), "connectivity deve ser 4 ou 8"
    if binary.dtype != np.uint8:
        binary = binary.astype(np.uint8)
    # garante estritamente 0/1
    bin01 = (binary > 0).astype(np.uint8)

    h, w = bin01.shape
    labels = np.zeros((h, w), dtype=np.int32)
    uf = UnionFind()
    next_label = 1

    # vizinhança “r” (esquerda) e “s” (cima) conforme aula; para 8, inclui diagonais
    # r: (y, x-1), s: (y-1, x)
    # diagonais: (y-1, x-1) e (y-1, x+1)
    for y in range(h):
        for x in range(w):
            if bin01[y, x] == 0:
                continue

            neighbors = []
            # s (cima)
            if y - 1 >= 0 and labels[y - 1, x] > 0:
                neighbors.append(labels[y - 1, x])
            # r (esquerda)
            if x - 1 >= 0 and labels[y, x - 1] > 0:
                neighbors.append(labels[y, x - 1])

            if connectivity == 8:
                # diag up-left
                if y - 1 >= 0 and x - 1 >= 0 and labels[y - 1, x - 1] > 0:
                    neighbors.append(labels[y - 1, x - 1])
                # diag up-right
                if y - 1 >= 0 and x + 1 < w and labels[y - 1, x + 1] > 0:
                    neighbors.append(labels[y - 1, x + 1])

            if not neighbors:
                labels[y, x] = next_label
                uf.parent[next_label] = next_label
                next_label += 1
            else:
                # pega o menor label vizinho
                m = min(neighbors)
                labels[y, x] = m
                # registra equivalências se houver mais de um label
                for lab in neighbors:
                    if lab != m:
                        uf.union(m, lab)

    # segunda passagem: comprime equivalências e remapeia para 1..K
    # cria mapa de raiz->novo rótulo compacto
    root_to_new = {}
    new_id = 1
    for y in range(h):
        for x in range(w):
            if labels[y, x] > 0:
                root = uf.find(labels[y, x])
                if root not in root_to_new:
                    root_to_new[root] = new_id
                    new_id += 1
                labels[y, x] = root_to_new[root]

    K = new_id - 1
    return labels, K
