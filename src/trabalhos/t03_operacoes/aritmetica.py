from __future__ import annotations
import numpy as np
from PIL import Image

def _ensure_u8(arr: np.ndarray) -> np.ndarray:
    return np.clip(arr, 0, 255).astype(np.uint8)

def _to_float(arr: np.ndarray) -> np.ndarray:
    return arr.astype(np.float32)

def _resize_to(img_arr: np.ndarray, target_shape: tuple[int, int]) -> np.ndarray:
    th, tw = target_shape[:2]
    pil = Image.fromarray(img_arr)
    pil = pil.resize((tw, th), resample=Image.BILINEAR)
    return np.array(pil)

def coerce_pair(img1: np.ndarray, img2: np.ndarray, mode: str = "resize") -> tuple[np.ndarray, np.ndarray]:
    """
    Garante que as imagens tenham o mesmo tamanho (H,W).
    Para T03 manter simples e consistente com T01, usamos 'resize' da img2 para img1.
    """
    a = img1
    b = img2
    if a.shape != b.shape:
        if mode == "resize":
            b = _resize_to(b, a.shape)
        else:
            raise ValueError("Atualmente só 'resize' está implementado.")
    return a, b

def add(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    a, b = coerce_pair(img1, img2, "resize")
    out = _to_float(a) + _to_float(b)
    return _ensure_u8(out)

def sub(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    a, b = coerce_pair(img1, img2, "resize")
    out = _to_float(a) - _to_float(b)
    return _ensure_u8(out)

def mul(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    a, b = coerce_pair(img1, img2, "resize")
    out = (_to_float(a) * _to_float(b)) / 255.0
    return _ensure_u8(out)

def div(img1: np.ndarray, img2: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    a, b = coerce_pair(img1, img2, "resize")
    out = (_to_float(a) / (_to_float(b) + eps)) * 255.0
    return _ensure_u8(out)
