# src/trabalhos/t03_operacoes/main_t03.py
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np

from . import aritmetica as ar
from . import geometria as geo
from .io_utils import (
    load_image, save_image,
    auto_out_name, name_arit, name_geo,
    show_side_by_side, ask,
)


# =========================
# Execuções principais
# =========================
def run_aritmetica(op: str, imagem: str, imagem2: str, out: str | None = None) -> Path:
    """
    Executa operação aritmética entre duas imagens (grayscale):
    add | sub | mul | div
    - As imagens são ajustadas (resize da 2ª para a 1ª) dentro do módulo aritmetica.
    """
    img1 = load_image(imagem)
    img2 = load_image(imagem2)

    op = op.strip().lower()
    if   op == "add": out_img = ar.add(img1, img2)
    elif op == "sub": out_img = ar.sub(img1, img2)
    elif op == "mul": out_img = ar.mul(img1, img2)
    elif op == "div": out_img = ar.div(img1, img2)
    else:
        raise ValueError("Operação inválida. Use: add | sub | mul | div")

    out_path = Path(out) if out else name_arit(imagem, imagem2, op)
    save_image(out_img, out_path)
    print(f"✅ [{op}] salvo em: {out_path}")

    show_side_by_side("Imagem 1", img1, f"Resultado {op}", out_img)
    return out_path


def run_geometria(
    gop: str,
    imagem: str,
    angle: float = 45.0,
    tx: int = 40,
    ty: int = 40,
    mode: str = "horizontal",
    out: str | None = None
) -> Path:
    """
    Executa operação geométrica em uma imagem (grayscale):
    rotate | translate | flip
    """
    img = load_image(imagem)

    gop = gop.strip().lower()
    if   gop == "rotate":
        out_img = geo.rotate(img, angle_deg=angle)
    elif gop == "translate":
        out_img = geo.translate(img, tx=tx, ty=ty)
    elif gop == "flip":
        out_img = geo.flip(img, mode=mode)
    else:
        raise ValueError("Operação geométrica inválida. Use: rotate | translate | flip")

    out_path = Path(out) if out else name_geo(imagem, gop, angle=angle, tx=tx, ty=ty, mode=mode)
    save_image(out_img, out_path)
    print(f"✅ [{gop}] salvo em: {out_path}")

    show_side_by_side("Original", img, f"Resultado {gop}", out_img)
    return out_path


# =========================
# Questionário (minimalista)
# =========================
def questionario():
    """
    Pergunta só o essencial:
    - Aritmética: operação + dois caminhos de imagens.
    - Geometria: operação + imagem e somente parâmetros relevantes.
    """
    print("\n=== T03 — Operações Aritméticas & Geométricas ===")
    print("[1] Aritmética (add, sub, mul, div)")
    print("[2] Geométrica (rotate, translate, flip)")
    tipo = ask("Escolha 1 ou 2", default="1")

    if tipo == "1":
        op = ask("Operação", default="add").lower()
        imagem  = ask("Caminho da 1ª imagem", default="data/flor.png")
        imagem2 = ask("Caminho da 2ª imagem", default="data/manchas.png")
        run_aritmetica(op=op, imagem=imagem, imagem2=imagem2, out=None)

    elif tipo == "2":
        gop    = ask("Op geométrica", default="rotate").lower()
        imagem = ask("Caminho da imagem", default="data/flor.png")

        if gop == "rotate":
            angle = float(ask("Ângulo (graus)", default="45"))
            run_geometria(gop=gop, imagem=imagem, angle=angle, out=None)
        elif gop == "translate":
            tx = int(ask("Tx (pixels)", default="40"))
            ty = int(ask("Ty (pixels)", default="40"))
            run_geometria(gop=gop, imagem=imagem, tx=tx, ty=ty, out=None)
        elif gop == "flip":
            mode = ask("Modo (horizontal|vertical|ambos)", default="horizontal").lower()
            run_geometria(gop=gop, imagem=imagem, mode=mode, out=None)
        else:
            print("Opção geométrica inválida.")
    else:
        print("Opção inválida.")


# =========================
# CLI (direto, como no T01)
# =========================
def _cli():
    """
    Exemplos:
      python -m src.trabalhos.t03_operacoes.main_t03 arit \
        --op add --imagem data/flor.png --imagem2 data/manchas.png

      python -m src.trabalhos.t03_operacoes.main_t03 geo \
        --gop rotate --imagem data/flor.png --angle 30

      python -m src.trabalhos.t03_operacoes.main_t03  # sem subcomando → questionário
    """
    p = argparse.ArgumentParser(description="T03 — Operações Aritméticas & Geométricas (PIL+NumPy)")
    sub = p.add_subparsers(dest="grupo")

    # Aritmética
    pa = sub.add_parser("arit", help="Operações aritméticas")
    pa.add_argument("--op", choices=["add", "sub", "mul", "div"], default="add")
    pa.add_argument("--imagem", required=True)
    pa.add_argument("--imagem2", required=True)
    pa.add_argument("--out", help="(Opcional) caminho de saída; se ausente, será automático")

    # Geometria
    pg = sub.add_parser("geo", help="Operações geométricas")
    pg.add_argument("--gop", choices=["rotate", "translate", "flip"], default="rotate")
    pg.add_argument("--imagem", required=True)
    pg.add_argument("--angle", type=float, default=45.0)
    pg.add_argument("--tx", type=int, default=40)
    pg.add_argument("--ty", type=int, default=40)
    pg.add_argument("--mode", default="horizontal")
    pg.add_argument("--out", help="(Opcional) caminho de saída; se ausente, será automático")

    args = p.parse_args()
    if args.grupo == "arit":
        run_aritmetica(op=args.op, imagem=args.imagem, imagem2=args.imagem2, out=args.out)
    elif args.grupo == "geo":
        run_geometria(
            gop=args.gop,
            imagem=args.imagem,
            angle=args.angle,
            tx=args.tx,
            ty=args.ty,
            mode=args.mode,
            out=args.out
        )
    else:
        questionario()


if __name__ == "__main__":
    _cli()
