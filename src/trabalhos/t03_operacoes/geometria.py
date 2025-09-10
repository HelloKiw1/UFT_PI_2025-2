from __future__ import annotations
import numpy as np
from PIL import Image

def rotate(img: np.ndarray, angle_deg: float = 45.0) -> np.ndarray:
    """
    Rotação anti-horária mantendo o mesmo tamanho da imagem (expand=False).
    Interpolação bilinear (como no T01).
    """
    pil = Image.fromarray(img)
    rot = pil.rotate(angle=angle_deg, resample=Image.BILINEAR, expand=False, fillcolor=0)
    return np.array(rot)

def translate(img: np.ndarray, tx: int = 40, ty: int = 40) -> np.ndarray:
    """
    Translação usando transformação afim do PIL (preenche com 0 fora da imagem).
    """
    h, w = img.shape[:2]
    pil = Image.fromarray(img)
    # Matriz afim (a, b, c, d, e, f) corresponde a:
    # x' = a*x + b*y + c ; y' = d*x + e*y + f
    # Para pura translação: a=1, b=0, c=tx ; d=0, e=1, f=ty
    aff = (1, 0, tx, 0, 1, ty)
    out = pil.transform((w, h), Image.AFFINE, aff, resample=Image.BILINEAR, fillcolor=0)
    return np.array(out)

def flip(img: np.ndarray, mode: str = "horizontal") -> np.ndarray:
    pil = Image.fromarray(img)
    if mode == "horizontal":
        out = pil.transpose(Image.FLIP_LEFT_RIGHT)
    elif mode == "vertical":
        out = pil.transpose(Image.FLIP_TOP_BOTTOM)
    elif mode == "ambos":
        out = pil.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
    else:
        raise ValueError("mode deve ser 'horizontal', 'vertical' ou 'ambos'.")
    return np.array(out)
