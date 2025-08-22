from __future__ import annotations
import numpy as np

def ensure_gray(img: np.ndarray) -> np.ndarray:
    """
    Garante imagem em tons de cinza (float32).
    Se vier RGB, usa média simples dos canais.
    """
    if img.ndim == 3:
        img = img.mean(axis=2)
    return img.astype(np.float32, copy=False)

def clamp_u8(arr: np.ndarray) -> np.ndarray:
    """Recorta para [0,255] e retorna uint8."""
    return np.clip(arr, 0, 255).astype(np.uint8)
