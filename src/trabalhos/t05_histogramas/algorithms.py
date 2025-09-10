from __future__ import annotations
import numpy as np

def ensure_u8(img: np.ndarray) -> np.ndarray:
    return np.clip(img, 0, 255).astype(np.uint8)

def _quantize_indices(img: np.ndarray, L: int) -> np.ndarray:
    """
    Mapear níveis 0..255 para índices 0..L-1:
      k = floor( img * L / 256 )
    """
    img = ensure_u8(img).astype(np.int32)
    idx = (img * L) // 256
    # por segurança, garanta o teto
    return np.clip(idx, 0, L - 1).astype(np.int32)

def _dequantize_to_255(idx: np.ndarray, L: int) -> np.ndarray:
    """
    Mapear índices 0..L-1 de volta para 0..255:
      v = round( idx * 255 / (L-1) )
    """
    if L <= 1:
        return np.zeros_like(idx, dtype=np.uint8)
    v = np.round(idx.astype(np.float32) * (255.0 / float(L - 1)))
    return ensure_u8(v)

def histogram(img: np.ndarray, L: int = 256) -> np.ndarray:
    """
    Histograma (contagens) para níveis 0..L-1.
    Se L < 256, usa histograma dos ÍNDICES quantizados (0..L-1).
    """
    if L < 256:
        flat = _quantize_indices(img, L).ravel()
    else:
        flat = ensure_u8(img).ravel()
    h = np.bincount(flat, minlength=L)
    if h.shape[0] > L:
        h = h[:L]
    return h.astype(np.int64)

def histogram_normalized(h: np.ndarray) -> np.ndarray:
    n = h.sum()
    if n == 0:
        return np.zeros_like(h, dtype=np.float64)
    return h.astype(np.float64) / float(n)

def cdf_from_pdf(pdf: np.ndarray) -> np.ndarray:
    return np.cumsum(pdf)

def equalization_lut(pdf: np.ndarray, L: int = 256) -> np.ndarray:
    cdf = cdf_from_pdf(pdf)
    lut = np.round((L - 1) * cdf)
    lut = np.clip(lut, 0, L - 1).astype(np.uint8)
    return lut

def apply_lut(img: np.ndarray, lut: np.ndarray) -> np.ndarray:
    """Transforma a imagem via look-up table (assume img já está no domínio da LUT)."""
    return lut[img]

def equalize(img: np.ndarray, L: int = 256):
    """
    Equalização de histograma:
      - Se L < 256: trabalha no domínio quantizado 0..L-1 e depois expande para 0..255.
      - Se L = 256: opera direto em 0..255.
    Retorna: (out, lut, h_in, pdf, cdf)
    """
    if img.dtype != np.uint8:
        img = ensure_u8(img)

    if L < 2:
        raise ValueError("L deve ser >= 2.")

    # 1) obter "níveis" onde o histograma será calculado
    if L < 256:
        idx = _quantize_indices(img, L)   # 0..L-1
        h_in = histogram(idx, L=L)        # hist dos índices
    else:
        idx = img.copy()                  # 0..255
        h_in = histogram(img, L=L)        # hist original

    # 2) pdf/cdf e LUT nesse domínio
    pdf = histogram_normalized(h_in)
    cdf = cdf_from_pdf(pdf)
    lut = equalization_lut(pdf, L=L)      # 0..L-1 -> 0..L-1

    # 3) aplicar LUT nos índices
    s_idx = apply_lut(idx, lut)           # 0..L-1

    # 4) expandir para 0..255 se necessário
    if L < 256:
        out = _dequantize_to_255(s_idx, L)
    else:
        out = s_idx.astype(np.uint8)

    return out, lut, h_in, pdf, cdf

def contrast_stretch(img: np.ndarray, a: int = 0, b: int = 255,
                     c: int | None = None, d: int | None = None) -> np.ndarray:
    if img.dtype != np.uint8:
        img = ensure_u8(img)

    F = img.astype(np.float32)
    if c is None: c = int(F.min())
    if d is None: d = int(F.max())

    if d == c:
        return np.full_like(img, fill_value=a, dtype=np.uint8)

    G = (F - c) * ((b - a) / float(d - c)) + a
    return ensure_u8(G)
