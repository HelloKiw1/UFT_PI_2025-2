# src/trabalhos/t06_media/main_t06.py
from __future__ import annotations
import argparse
from datetime import datetime
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# IO do T01 (grayscale)
from src.trabalhos.t01_interpolacao.io_utils import load_image, save_image
# Importar a implementação atual do filtro da média
from .algorithms import mean_filter

# ---------- utilidades ----------
def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def _auto_out(prefix: str, base: str, extra: str | None = None, suffix: str = ".png") -> Path:
    parts = [prefix, base]
    if extra:
        parts.append(extra)
    parts.append(_stamp())
    name = "__".join(parts) + suffix
    outdir = Path("outputs"); outdir.mkdir(parents=True, exist_ok=True)
    return outdir / name

def _ask(prompt: str, default: str | None = None) -> str:
    s = input(f"{prompt}{f' [{default}]' if default is not None else ''}: ").strip()
    return s if s else (default or "")

def _show_side_by_side(title_l: str, img_l: np.ndarray,
                       title_r: str, img_r: np.ndarray):
    try:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1); plt.imshow(img_l, cmap="gray"); plt.title(title_l); plt.axis("off")
        plt.subplot(1, 2, 2); plt.imshow(img_r, cmap="gray"); plt.title(title_r); plt.axis("off")
        plt.tight_layout(); plt.show()
    except Exception as e:
        print(f"(Aviso) Não foi possível exibir as figuras: {e}")

# ---------- run ----------
def run_media(imagem: str, k: int = 3,
              out: str | None = None, visualizar: bool = True) -> Path:
    """
    Executa o Filtro da Média com janela k×k e tratamento de bordas.
    border ∈ {zero, replicate, reflect, wrap}.
    """
    img = load_image(imagem)
    # o tratamento de borda é fixo para 'zero'
    out_img = mean_filter(img, k=k)

    base = Path(imagem).stem
    extra = f"k{k}_zero"
    out_path = Path(out) if out else _auto_out("t06_media", base, extra=extra)
    save_image(out_img, out_path)
    print(f"✅ [media k={k}, border=zero] salvo em: {out_path}")

    if visualizar:
        _show_side_by_side("Original", img, f"Média {k}×{k} (zero)", out_img)
    return out_path

# ---------- questionário ----------
def questionario():
    print("\n=== T06 — Filtro da Média (suavização) ===")
    imagem = _ask("Caminho da imagem", default="data/flor.png")
    k = int(_ask("Tamanho da janela k (ímpar)", default="3"))
    # Tratamento de borda fixo: zero
    run_media(imagem=imagem, k=k, visualizar=True)

# ---------- CLI ----------
def _cli():
    """
    Exemplos:
    # k=3 (borda fixa: zero)
    python -m src.trabalhos.t06_media.main_t06 media --imagem data/flor.png --k 3

    # exemplo com k=5
    python -m src.trabalhos.t06_media.main_t06 media --imagem data/flor.png --k 5
    """
    p = argparse.ArgumentParser(description="T06 — Filtro da Média (suavização)")
    sub = p.add_subparsers(dest="cmd")

    pm = sub.add_parser("media", help="Filtro da Média")
    pm.add_argument("--imagem", required=True)
    pm.add_argument("--k", type=int, default=3)
    # Borda removida: o tratamento é fixo para "zero"
    pm.add_argument("--out")
    pm.add_argument("--no-show", action="store_true")

    args = p.parse_args()
    if args.cmd == "media":
        run_media(imagem=args.imagem, k=args.k, out=args.out, visualizar=not args.no_show)
    else:
        questionario()

if __name__ == "__main__":
    _cli()
