from __future__ import annotations
import numpy as np

def ensure_u8(x: np.ndarray) -> np.ndarray:
    return np.clip(x, 0, 255).astype(np.uint8) 

# ----------------------------
# tratamento de bordas (apenas ZERO)
# ----------------------------
def _pad(img: np.ndarray, pad: int) -> np.ndarray:
    if pad <= 0:
        return img
    return np.pad(img, ((pad, pad), (pad, pad)), mode="constant", constant_values=0)

def mean_filter(img: np.ndarray, k: int = 3) -> np.ndarray:
    """
    Parâmetros:
    - k: tamanho da janela (ímpar);
    Observação: o tratamento de borda é fixo para 'zero'.
    """
    if img.dtype != np.uint8:
        img = ensure_u8(img)
    if k < 1 or k % 2 == 0:
        raise ValueError("k deve ser ímpar e >= 1 (ex.: 3, 5, 7).")

    pad = k // 2
    padded = _pad(img, pad).astype(np.int64)
    H, W = img.shape
    out = np.empty((H, W), dtype=np.float64)

    for y in range(H):
        for x in range(W):
            s = 0
            # soma manual da janela kxk
            for dy in range(k): 
                py = y + dy 
                row = padded[py]
                for dx in range(k):
                    s += int(row[x + dx])
            out[y, x] = s / float(k * k)

    return ensure_u8(out)
