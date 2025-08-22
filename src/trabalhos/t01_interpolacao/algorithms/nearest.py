from __future__ import annotations
import numpy as np
from ._base import ensure_gray, clamp_u8

def resize_nearest(img: np.ndarray, new_h: int, new_w: int) -> np.ndarray:
    """
    Redimensiona usando Vizinho Mais Próximo.
    img: (H,W) ou (H,W,3)
    retorna: (new_h, new_w) uint8
    """
    img = ensure_gray(img)
    h, w = img.shape[:2]

    new_h = max(1, int(new_h))
    new_w = max(1, int(new_w))

    out = np.empty((new_h, new_w), dtype=np.float32)

    row_scale = h / new_h
    col_scale = w / new_w

    for i in range(new_h):
        src_i = int(round(i * row_scale))
        if src_i >= h:
            src_i = h - 1
        for j in range(new_w):
            src_j = int(round(j * col_scale))
            if src_j >= w:
                src_j = w - 1
            out[i, j] = img[src_i, src_j]

    return clamp_u8(out)
