"""
Utilitários de Entrada/Saída de imagens.
"""

from __future__ import annotations
from pathlib import Path
from typing import Union
import numpy as np
from PIL import Image


def load_image(path: Union[str, Path]) -> np.ndarray:
    """
    Carrega uma imagem do disco e retorna ndarray (grayscale).
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Imagem não encontrada: {p}")
    # converte para 'L' (tons de cinza)
    img = Image.open(p).convert("L")
    return np.array(img)


def save_image(array: np.ndarray, path: Union[str, Path]) -> None:
    """
    Salva um ndarray (0..255) como imagem no disco.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(array).save(p)