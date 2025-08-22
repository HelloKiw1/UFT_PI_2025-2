"""
Ponto de entrada do Trabalho 01 — Interpolação.

Uso:
    # interativo (se quiser perguntar parâmetros aqui)
    python -m src.trabalhos.t01_interpolacao.main

    # chamando a função diretamente (usado pelo index.py do repositório)
    from src.trabalhos.t01_interpolacao.main import run
    run(imagem="data/flor.jpg", metodo="bilinear", escala=2.0)
"""

from __future__ import annotations
import argparse
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

from .algorithms import resize_nearest, resize_bilinear
from .io_utils import load_image, save_image


def run(imagem: str | None = None, metodo: str = "bilinear", escala: float = 2.0) -> Path:
    """
    Executa o Trabalho 01.

    Parâmetros:
        imagem : caminho do arquivo de entrada (string)
        metodo : 'vizinho' | 'bilinear'
        escala : fator de escala (>1 amplia; <1 reduz)

    Retorna:
        Path do arquivo salvo em outputs/
    """
    if imagem is None:
        imagem = input("Caminho da imagem (ex: data/flor.jpg): ").strip()

    if not imagem:
        raise ValueError("É necessário informar o caminho da imagem.")

    metodo = (metodo or "bilinear").strip().lower()
    if metodo not in {"vizinho", "bilinear"}:
        raise ValueError("Método inválido. Use 'vizinho' ou 'bilinear'.")

    try:
        escala = float(escala)
    except Exception:
        raise ValueError("Escala deve ser um número. Exemplo: 0.5, 2.0, 1.25")

    if escala <= 0:
        raise ValueError("Escala deve ser > 0. Ex.: 0.5 (reduz), 2.0 (amplia)")

    # carrega e processa
    img = load_image(imagem)
    h, w = img.shape[:2]
    new_h = max(1, int(round(h * escala)))
    new_w = max(1, int(round(w * escala)))

    if metodo == "vizinho":
        out = resize_nearest(img, new_h, new_w)
    else:
        out = resize_bilinear(img, new_h, new_w)

    # salvar
    outputs = Path("outputs")
    outputs.mkdir(exist_ok=True, parents=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = Path(imagem).stem
    out_name = f"{base}_{metodo}_esc{escala:.2f}_{ts}.png"
    out_path = outputs / out_name
    save_image(out, out_path)

    print(f"✅ Resultado salvo em: {out_path}")

    # visualizar
    try:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(img, cmap="gray")
        plt.title("Original")
        plt.axis("off")

        plt.subplot(1, 2, 2)
        plt.imshow(out, cmap="gray")
        plt.title(f"Resultado: {metodo}")
        plt.axis("off")

        plt.tight_layout()
        plt.show()
    except Exception as e:
        # caso ambiente sem backend gráfico
        print(f"(Aviso) Não foi possível exibir a figura: {e}")

    return out_path


def _cli():
    parser = argparse.ArgumentParser(description="Trabalho 01 — Interpolação (vizinho/bilinear)")
    parser.add_argument("--imagem", type=str, help="Caminho da imagem de entrada (ex.: data/flor.jpg)")
    parser.add_argument("--metodo", type=str, default="bilinear", help="vizinho | bilinear")
    parser.add_argument("--escala", type=float, default=2.0, help=">1 amplia; <1 reduz (ex.: 0.5, 2.0)")

    args = parser.parse_args()
    run(imagem=args.imagem, metodo=args.metodo, escala=args.escala)


if __name__ == "__main__":
    _cli()
