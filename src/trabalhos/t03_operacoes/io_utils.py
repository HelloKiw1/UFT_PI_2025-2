# src/trabalhos/t03_operacoes/io_utils.py
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Reaproveita IO do T01 (grayscale)
from src.trabalhos.t01_interpolacao.io_utils import load_image as _load_gray, save_image as _save_gray


# =========================
# IO (grayscale)
# =========================
def load_image(path: str | Path) -> np.ndarray:
    """Carrega imagem em tons de cinza (uint8) usando o IO do T01."""
    return _load_gray(path)

def save_image(arr: np.ndarray, path: str | Path) -> None:
    """Salva imagem (uint8) usando o IO do T01."""
    _save_gray(arr, path)


# =========================
# Nomes de saída
# =========================
def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def auto_out_name(prefix: str, base: str | None = None, extra: str | None = None, suffix: str = ".png") -> Path:
    """
    Gera nomes autoexplicativos:
      outputs/<prefix>__<base>__<extra>__<timestamp>.png
    Componentes ausentes são omitidos.
    """
    parts = [prefix]
    if base:
        parts.append(base)
    if extra:
        parts.append(extra)
    parts.append(_stamp())
    fname = "__".join(parts) + suffix
    outdir = Path("outputs")
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir / fname


# Helpers opcionais de nome (caso queira padronizar em um lugar só)
def name_arit(imagem1: str | Path, imagem2: str | Path, op: str) -> Path:
    base = f"{Path(imagem1).stem}__{Path(imagem2).stem}"
    return auto_out_name(prefix=f"t03_{op.lower()}", base=base)

def name_geo(imagem: str | Path, gop: str, *, angle: float | None = None, tx: int | None = None, ty: int | None = None, mode: str | None = None) -> Path:
    b = Path(imagem).stem
    if gop == "rotate" and angle is not None:
        extra = f"ang{angle:.0f}"
    elif gop == "translate" and (tx is not None and ty is not None):
        extra = f"tx{tx}_ty{ty}"
    elif gop == "flip" and mode is not None:
        extra = f"{mode}"
    else:
        extra = None
    return auto_out_name(prefix=f"t03_{gop.lower()}", base=b, extra=extra)


# =========================
# Visualização / UI mínima
# =========================
def show_side_by_side(title_left: str, img_left: np.ndarray, title_right: str, img_right: np.ndarray):
    """Exibição best-effort (não falha se GUI não estiver disponível)."""
    try:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(img_left, cmap="gray")
        plt.title(title_left)
        plt.axis("off")

        plt.subplot(1, 2, 2)
        plt.imshow(img_right, cmap="gray")
        plt.title(title_right)
        plt.axis("off")

        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"(Aviso) Não foi possível exibir a figura: {e}")

def ask(prompt: str, default: str | None = None) -> str:
    """Input com default opcional (pergunta só quando necessário)."""
    s = input(f"{prompt}{f' [{default}]' if default is not None else ''}: ").strip()
    return s if s else (default or "")
