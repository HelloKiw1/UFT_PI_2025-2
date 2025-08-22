"""
Algoritmos de interpolação para imagens em tons de cinza.
Implementações manuais de:
- Vizinho mais Próximo
- Bilinear

Obs.: Trabalhamos em escala [0..255] e retornamos uint8.
"""

from __future__ import annotations
import numpy as np


def _ensure_gray(img: np.ndarray) -> np.ndarray:
    """
    Converte para tons de cinza se vier RGB (média simples dos canais).
    Retorna float32 para os cálculos.
    """
    if img.ndim == 3:
        img = img.mean(axis=2)
    return img.astype(np.float32)


def resize_nearest(img: np.ndarray, new_h: int, new_w: int) -> np.ndarray:
    """
    Redimensiona usando Vizinho Mais Próximo.

    Parâmetros:
        img   : ndarray (H, W) ou (H, W, 3)
        new_h : nova altura
        new_w : nova largura

    Retorna:
        ndarray (new_h, new_w) uint8
    """
    img = _ensure_gray(img)
    h, w = img.shape[:2]

    # evita casos degenerados
    new_h = max(1, int(new_h))
    new_w = max(1, int(new_w))

    out = np.empty((new_h, new_w), dtype=np.float32)

    row_scale = h / new_h
    col_scale = w / new_w

    for i in range(new_h):
        # mapeamento proporcional
        src_i = int(round(i * row_scale))
        if src_i >= h:
            src_i = h - 1

        for j in range(new_w):
            src_j = int(round(j * col_scale))
            if src_j >= w:
                src_j = w - 1

            out[i, j] = img[src_i, src_j]

    return np.clip(out, 0, 255).astype(np.uint8)


def resize_bilinear(img: np.ndarray, new_h: int, new_w: int) -> np.ndarray:
    """
    Redimensiona usando Interpolação Bilinear.

    Parâmetros:
        img   : ndarray (H, W) ou (H, W, 3)
        new_h : nova altura
        new_w : nova largura

    Retorna:
        ndarray (new_h, new_w) uint8
    """
    img = _ensure_gray(img)
    h, w = img.shape[:2]

    # evita casos degenerados
    new_h = max(1, int(new_h))
    new_w = max(1, int(new_w))

    out = np.empty((new_h, new_w), dtype=np.float32)

    # escalas (mapeiam as bordas exatamente quando new_* > 1)
    row_scale = (h - 1) / (new_h - 1) if new_h > 1 else 0.0
    col_scale = (w - 1) / (new_w - 1) if new_w > 1 else 0.0

    for i in range(new_h):
        src_y = i * row_scale
        y0 = int(np.floor(src_y))
        y1 = min(y0 + 1, h - 1)
        wy = src_y - y0  # peso vertical (fração)

        for j in range(new_w):
            src_x = j * col_scale
            x0 = int(np.floor(src_x))
            x1 = min(x0 + 1, w - 1)
            wx = src_x - x0  # peso horizontal (fração)

            # Interpola na linha de cima e na de baixo, depois mistura verticalmente
            top    = (1 - wx) * img[y0, x0] + wx * img[y0, x1]
            bottom = (1 - wx) * img[y1, x0] + wx * img[y1, x1]
            out[i, j] = (1 - wy) * top + wy * bottom

    return np.clip(out, 0, 255).astype(np.uint8)
