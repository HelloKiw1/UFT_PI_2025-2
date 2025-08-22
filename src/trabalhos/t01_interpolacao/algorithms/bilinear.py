from __future__ import annotations
import numpy as np
from ._base import ensure_gray, clamp_u8

def resize_bilinear(img: np.ndarray, new_h: int, new_w: int) -> np.ndarray:
    """
    Redimensiona usando Interpolação Bilinear.
    img: (H,W) ou (H,W,3)
    retorna: (new_h, new_w) uint8
    """
    img = ensure_gray(img)
    h, w = img.shape[:2]

    new_h = max(1, int(new_h))
    new_w = max(1, int(new_w))

    out = np.empty((new_h, new_w), dtype=np.float32)

    # mapeiam bordas -> bordas (quando >1)
    row_scale = (h - 1) / (new_h - 1) if new_h > 1 else 0.0
    col_scale = (w - 1) / (new_w - 1) if new_w > 1 else 0.0

    for i in range(new_h):
        src_y = i * row_scale
        y0 = int(np.floor(src_y))
        y1 = min(y0 + 1, h - 1)
        wy = src_y - y0
        for j in range(new_w):
            src_x = j * col_scale
            x0 = int(np.floor(src_x))
            x1 = min(x0 + 1, w - 1)
            wx = src_x - x0

            top    = (1 - wx) * img[y0, x0] + wx * img[y0, x1]
            bottom = (1 - wx) * img[y1, x0] + wx * img[y1, x1]
            out[i, j] = (1 - wy) * top + wy * bottom

    return clamp_u8(out)
