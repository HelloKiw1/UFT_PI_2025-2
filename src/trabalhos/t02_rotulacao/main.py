from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from .algorithms import connected_components

# Reuso opcional: se você já tem io_utils com load/save, pode importar e usar no lugar
def _load_any_image(path: str | Path) -> np.ndarray:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Imagem não encontrada: {p}")
    # Lê RGB e converte para cinza apenas para binarizar
    arr = np.array(Image.open(p).convert("RGB"), dtype=np.uint8)
    gray = arr.mean(axis=2).astype(np.uint8)
    return gray

def _binarize(gray: np.ndarray, thresh: int = 127) -> np.ndarray:
    # conforme os slides: f(x,y) < 127 -> 0, senão 255  :contentReference[oaicite:1]{index=1}
    bin_img = np.where(gray < thresh, 0, 255).astype(np.uint8)
    # para a rotulação, convertemos 255->1 (foreground), 0 fica 0
    bin01 = (bin_img == 255).astype(np.uint8)
    return bin_img, bin01

def _labels_to_color(labels: np.ndarray) -> np.ndarray:
    """Converte mapa de rótulos para RGB colorido: cada componente recebe uma cor estável."""
    h, w = labels.shape
    out = np.zeros((h, w, 3), dtype=np.uint8)
    rng = np.random.default_rng(42)  # fixo p/ reprodutibilidade
    palette = {0: (0, 0, 0)}
    for lab in np.unique(labels):
        if lab == 0:
            continue
        if lab not in palette:
            palette[lab] = tuple(int(x) for x in rng.integers(64, 256, size=3))
    for lab, color in palette.items():
        out[labels == lab] = color
    return out

def run(imagem: str | None = None, thresh: int | None = 127, conectividade: int | None = 4) -> Path:
    """
    Trabalho 02 — Conectividade & Rotulação.
    - Lê imagem, binariza por limiar, rotula componentes (4 ou 8), salva resultados.
    """
    if imagem is None:
        imagem = input("Caminho da imagem (ex: data/manchas.png): ").strip()
    if not imagem:
        raise ValueError("Informe o caminho da imagem.")

    try:
        thresh = int(thresh if thresh is not None else input("Limiar de binarização [127]: ") or "127")
    except Exception:
        raise ValueError("Limiar deve ser inteiro (ex.: 127).")
    try:
        conectividade = int(conectividade if conectividade is not None else input("Conectividade (4/8) [4]: ") or "4")
    except Exception:
        raise ValueError("Conectividade deve ser 4 ou 8.")
    if conectividade not in (4, 8):
        raise ValueError("Conectividade inválida. Use 4 ou 8.")

    gray = _load_any_image(imagem)
    bin_img, bin01 = _binarize(gray, thresh=thresh)
    labels, K = connected_components(bin01, connectivity=conectividade)

    # salvar saídas
    outputs = Path("outputs")
    outputs.mkdir(parents=True, exist_ok=True)

    base = Path(imagem).stem
    bin_path = outputs / f"{base}_bin_t{thresh}.png"
    lab_path = outputs / f"{base}_labels_c{conectividade}.png"

    Image.fromarray(bin_img, mode="L").save(bin_path)
    Image.fromarray(_labels_to_color(labels), mode="RGB").save(lab_path)

    print(f"✅ Componentes encontrados: {K}")
    print(f"🖼️ Binária:  {bin_path}")
    print(f"🖼️ Rótulos:  {lab_path}")

    # visualizar
    try:
        plt.figure(figsize=(12, 4))
        plt.subplot(1, 3, 1); plt.imshow(gray, cmap="gray"); plt.title("Grayscale"); plt.axis("off")
        plt.subplot(1, 3, 2); plt.imshow(bin_img, cmap="gray"); plt.title(f"Binária (t={thresh})"); plt.axis("off")
        plt.subplot(1, 3, 3); plt.imshow(_labels_to_color(labels)); plt.title(f"Rótulos (K={K}, {conectividade}-conn)"); plt.axis("off")
        plt.tight_layout(); plt.show()
    except Exception as e:
        print(f"(Aviso) Não foi possível exibir a figura: {e}")

    return lab_path

def questionario():
    """
    Questionário específico do Trabalho 02 — chamado pelo menu global.
    """
    imagem = input("Caminho da imagem (ex: data/manchas.png): ").strip() or "data/manchas.png"
    t_txt = input("Limiar de binarização [127]: ").strip() or "127"
    c_txt = input("Conectividade (4/8) [4]: ").strip() or "4"
    try:
        thresh = int(t_txt)
    except Exception:
        print("Limiar inválido — usando 127."); thresh = 127
    try:
        conectividade = int(c_txt)
    except Exception:
        print("Conectividade inválida — usando 4."); conectividade = 4
    run(imagem=imagem, thresh=thresh, conectividade=conectividade)

def _cli():
    parser = argparse.ArgumentParser(description="Trabalho 02 — Conectividade & Rotulação (4/8)")
    parser.add_argument("--imagem", type=str, help="Caminho da imagem (RGB/Gray)")
    parser.add_argument("--thresh", type=int, default=127, help="Limiar de binarização (ex.: 127)")
    parser.add_argument("--conectividade", type=int, default=4, help="4 ou 8")
    args = parser.parse_args()
    run(imagem=args.imagem, thresh=args.thresh, conectividade=args.conectividade)

if __name__ == "__main__":
    _cli()
