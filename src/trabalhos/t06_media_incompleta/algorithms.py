from __future__ import annotations
import numpy as np

def ensure_u8(x: np.ndarray) -> np.ndarray:
    return np.clip(x, 0, 255).astype(np.uint8)

# ----------------------------
# Padding (tratamento de bordas)
# ----------------------------
_PAD_MAP = {
    "zero": "constant",     # preenche com 0
    "replicate": "edge",    # repete borda
    "reflect": "reflect",   # espelha
    "wrap": "wrap",         # periódico
}

def _pad(img: np.ndarray, pad: int, mode: str) -> np.ndarray:
    """
    Aplica padding ao redor da imagem conforme 'mode'.
    'mode' ∈ {zero, replicate, reflect, wrap}.
    """
    mode = mode.lower()
    if mode not in _PAD_MAP:
        raise ValueError("Modo de borda inválido. Use: zero | replicate | reflect | wrap")
    np_mode = _PAD_MAP[mode]
    if np_mode == "constant":
        return np.pad(img, ((pad, pad), (pad, pad)), mode=np_mode, constant_values=0)
    return np.pad(img, ((pad, pad), (pad, pad)), mode=np_mode)

# ----------------------------
# Box filter via imagem integral (rápido)
# ----------------------------
def _integral_image(img: np.ndarray) -> np.ndarray:
    """
    Imagem integral 2D (com linha/coluna extras de zeros).
    I tem shape (H+1, W+1) e I[y, x] é a soma no retângulo [0..y-1, 0..x-1].
    """
    I = img.cumsum(axis=0).cumsum(axis=1)
    H, W = img.shape
    out = np.zeros((H + 1, W + 1), dtype=np.float64)
    out[1:, 1:] = I
    return out

def _box_sum_via_integral(padded: np.ndarray, k: int) -> np.ndarray:
    """
    Soma dos blocos kxk para todos os pixels da imagem NÃO-paddada,
    usando a imagem integral do array 'padded'.
    """
    I = _integral_image(padded.astype(np.float64))
    # janelas kxk: top-left caminha de (0,0) até (H-1, W-1) na imagem original
    H = padded.shape[0] - (k - 1)
    W = padded.shape[1] - (k - 1)
    # somatório de cada bloco via inclusão-exclusão
    block_sum = I[k:, k:] - I[:-k, k:] - I[k:, :-k] + I[:-k, :-k]
    # block_sum tem shape (H, W)
    assert block_sum.shape == (H, W)
    return block_sum

def mean_filter(img: np.ndarray, k: int = 3, border: str = "zero") -> np.ndarray:
    """
    Filtro da Média (suavização) com janela k×k (k ímpar).
    Tratamento de bordas: zero | replicate | reflect | wrap (periódico).
    """
    if img.dtype != np.uint8:
        img = ensure_u8(img)
    if k < 1 or k % 2 == 0:
        raise ValueError("k deve ser ímpar e >= 1 (ex.: 3, 5, 7).")

    pad = k // 2
    padded = _pad(img, pad, border)
    block_sum = _box_sum_via_integral(padded, k)
    mean = block_sum / float(k * k)
    return ensure_u8(mean)
