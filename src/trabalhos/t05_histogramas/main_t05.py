from __future__ import annotations
import argparse
from datetime import datetime
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Reutiliza IO do T01 (grayscale)
from src.trabalhos.t01_interpolacao.io_utils import load_image, save_image
from .algorithms import equalize, contrast_stretch, histogram

# ---------- Utilidades ----------
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

def _plot_hist(ax, img: np.ndarray, L: int = 256, title: str = "Histograma"):
    h = histogram(img, L=L)
    ax.bar(np.arange(L), h, width=1.0)
    ax.set_title(title)
    ax.set_xlim(0, L - 1)

def _show_pair_with_hist(title_l: str, img_l: np.ndarray,
                         title_r: str, img_r: np.ndarray, L: int = 256):
    try:
        fig = plt.figure(figsize=(10, 6))
        gs = fig.add_gridspec(2, 2, height_ratios=[3, 2])
        ax1 = fig.add_subplot(gs[0, 0]); ax2 = fig.add_subplot(gs[0, 1])
        ax3 = fig.add_subplot(gs[1, 0]); ax4 = fig.add_subplot(gs[1, 1])

        ax1.imshow(img_l, cmap="gray"); ax1.set_title(title_l); ax1.axis("off")
        ax2.imshow(img_r, cmap="gray"); ax2.set_title(title_r); ax2.axis("off")
        _plot_hist(ax3, img_l, L=L, title="Hist (antes)")
        _plot_hist(ax4, img_r, L=L, title="Hist (depois)")

        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"(Aviso) Não foi possível exibir as figuras: {e}")

# ---------- Runs ----------
def run_equalizacao(imagem: str, L: int = 256, out: str | None = None, visualizar: bool = True) -> Path:
    img = load_image(imagem)
    out_img, lut, h_in, pdf, cdf = equalize(img, L=L)

    base = Path(imagem).stem
    out_path = Path(out) if out else _auto_out("t05_equalize", base, extra=f"L{L}")
    save_image(out_img, out_path)
    print(f"✅ [equalize] salvo em: {out_path}")

    if visualizar:
        _show_pair_with_hist("Original", img, "Equalizada", out_img, L=L)
    return out_path

def run_stretch(imagem: str, a: int = 0, b: int = 255, c: int | None = None, d: int | None = None,
                out: str | None = None, visualizar: bool = True) -> Path:
    img = load_image(imagem)
    out_img = contrast_stretch(img, a=a, b=b, c=c, d=d)

    extra_parts = [f"a{a}", f"b{b}"]
    if c is not None: extra_parts.append(f"c{c}")
    if d is not None: extra_parts.append(f"d{d}")
    extra = "_".join(extra_parts)

    base = Path(imagem).stem
    out_path = Path(out) if out else _auto_out("t05_stretch", base, extra=extra)
    save_image(out_img, out_path)
    print(f"✅ [stretch] salvo em: {out_path}")

    if visualizar:
        _show_pair_with_hist("Original", img, "Contrast Stretching", out_img)
    return out_path

# ---------- Questionário minimalista ----------
def questionario():
    print("\n=== T05 — Processamento de Histogramas ===")
    print("[1] Equalização de Histograma (CDF/LUT)")
    print("[2] Alargamento de Contraste (Contrast Stretching)")
    tipo = _ask("Escolha 1 ou 2", default="1")

    if tipo == "1":
        imagem = _ask("Caminho da imagem", default="data/flor.png")
        L_txt  = _ask("Níveis de cinza (L) [256 ou 8]", default="256")
        L = int(L_txt)
        run_equalizacao(imagem=imagem, L=L, visualizar=True)

    elif tipo == "2":
        imagem = _ask("Caminho da imagem", default="data/flor.png")
        a = int(_ask("a (mín. alvo)", default="0"))
        b = int(_ask("b (máx. alvo)", default="255"))
        c_txt = _ask("c (mín. da imagem) [auto=min]", default="")
        d_txt = _ask("d (máx. da imagem) [auto=max]", default="")
        c = int(c_txt) if c_txt else None
        d = int(d_txt) if d_txt else None
        run_stretch(imagem=imagem, a=a, b=b, c=c, d=d, visualizar=True)
    else:
        print("Opção inválida.")

# ---------- CLI ----------
def _cli():
    """
    Exemplos:
      # equalização padrão (L=256)
      python -m src.trabalhos.t05_histogramas.main_t05 eq --imagem data/flor.png

      # equalização para L=8 (exercício de slides)
      python -m src.trabalhos.t05_histogramas.main_t05 eq --imagem data/flor.png --L 8

      # contrast stretching automático (c/d via min/max)
      python -m src.trabalhos.t05_histogramas.main_t05 stretch --imagem data/flor.png --a 0 --b 255

      # contrast stretching informando c/d
      python -m src.trabalhos.t05_histogramas.main_t05 stretch --imagem data/flor.png --a 0 --b 255 --c 30 --d 200
    """
    p = argparse.ArgumentParser(description="T05 — Processamento de Histogramas (equalização e contrast stretching)")
    sub = p.add_subparsers(dest="cmd")

    peq = sub.add_parser("eq", help="Equalização de histograma (CDF/LUT)")
    peq.add_argument("--imagem", required=True)
    peq.add_argument("--L", type=int, default=256)
    peq.add_argument("--out")
    peq.add_argument("--no-show", action="store_true", help="Não abrir janelas de visualização")

    pst = sub.add_parser("stretch", help="Alargamento de contraste")
    pst.add_argument("--imagem", required=True)
    pst.add_argument("--a", type=int, default=0)
    pst.add_argument("--b", type=int, default=255)
    pst.add_argument("--c", type=int)
    pst.add_argument("--d", type=int)
    pst.add_argument("--out")
    pst.add_argument("--no-show", action="store_true")

    args = p.parse_args()
    if args.cmd == "eq":
        run_equalizacao(imagem=args.imagem, L=args.L, out=args.out, visualizar=not args.no_show)
    elif args.cmd == "stretch":
        run_stretch(imagem=args.imagem, a=args.a, b=args.b, c=args.c, d=args.d, out=args.out, visualizar=not args.no_show)
    else:
        # sem subcomando → questionário
        questionario()

if __name__ == "__main__":
    _cli()
