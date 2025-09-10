#!/usr/bin/env python3
"""
Índice dos Trabalhos de Processamento de Imagens.

Usos:
  # 1) Modo menu (interativo)
  python index.py --menu

  # 2) Modo direto (sem menu)
  # T01 – Interpolação
  python index.py --trabalho 1 --imagem data/flor.png --metodo bilinear --escala 2.0

  # T02 – Rotulação
  python index.py --trabalho 2 --imagem data/manchas.png --thresh 127 --conectividade 4

  # T03 – Operações aritméticas
  python index.py --trabalho 3 --op add --imagem data/flor.png --imagem2 data/manchas.png --out outputs/t03_add.png

  # T03 – Operações geométricas
  python index.py --trabalho 3 --gop rotate --imagem data/flor.png --angle 45 --scale 1.0 --out outputs/t03_rotate_45.png
"""
from __future__ import annotations
import argparse
import importlib
from types import SimpleNamespace

# Mapeia IDs a descrições e targets (quando o trabalho expõe run()).
TRABALHOS = {
    "1": ("Interpolação (Vizinho + Bilinear)", "src.trabalhos.t01_interpolacao.main:run"),
    "2": ("Conectividade & Rotulação (4/8)",    "src.trabalhos.t02_rotulacao.main:run"),
    # "3" será tratado explicitamente (usa funções internas do módulo)
}

def _resolver_callable(target: str):
    """Recebe 'modulo.submod:func' e retorna o objeto chamável."""
    mod_name, func_name = target.split(":")
    mod = importlib.import_module(mod_name)
    return getattr(mod, func_name)

def main():
    parser = argparse.ArgumentParser(description="Índice dos Trabalhos de Processamento de Imagens")
    parser.add_argument("--trabalho", help="ID do trabalho (ex.: 1, 2 ou 3)")
    parser.add_argument("--menu", action="store_true", help="Abre o menu interativo de seleção")

    # --- Parâmetros gerais já existentes ---
    parser.add_argument("--imagem", help="Caminho da imagem principal")
    parser.add_argument("--metodo", help="vizinho | bilinear (Trabalho 1)")
    parser.add_argument("--escala", type=float, help=">1 amplia; <1 reduz (Trabalho 1)")
    parser.add_argument("--thresh", type=int, help="Limiar de binarização (Trabalho 2)")
    parser.add_argument("--conectividade", type=int, help="4 ou 8 (Trabalho 2)")

    # --- Novos parâmetros para T03 ---
    # Aritmética
    parser.add_argument("--op", choices=["add", "sub", "mul", "div"],
                        help="Operação aritmética (T03): add|sub|mul|div")
    parser.add_argument("--imagem2", help="Segunda imagem (T03 aritmética)")
    # Geometria
    parser.add_argument("--gop", choices=["rotate", "translate", "flip"],
                        help="Operação geométrica (T03): rotate|translate|flip")
    parser.add_argument("--angle", type=float, default=45.0, help="Ângulo p/ rotate (graus)")
    parser.add_argument("--scale", type=float, default=1.0, help="Escala p/ rotate")
    parser.add_argument("--tx", type=int, default=40, help="Translação em x (translate)")
    parser.add_argument("--ty", type=int, default=40, help="Translação em y (translate)")
    parser.add_argument("--mode", type=str, default="horizontal",
                        help="flip: horizontal | vertical | ambos")
    parser.add_argument("--out", help="Arquivo de saída (ex.: outputs/t03_out.png)")

    args = parser.parse_args()

    # MENU GLOBAL
    if args.menu or not args.trabalho:
        from src.menu import questionario_global
        questionario_global()
        return

    # DIRETO
    if args.trabalho == "1":
        run_callable = _resolver_callable(TRABALHOS["1"][1])
        run_callable(imagem=args.imagem, metodo=args.metodo, escala=args.escala)

    elif args.trabalho == "2":
        run_callable = _resolver_callable(TRABALHOS["2"][1])
        run_callable(imagem=args.imagem, thresh=args.thresh, conectividade=args.conectividade)

    elif args.trabalho == "3":
        # Integra com o T03 chamando diretamente as funções internas do módulo
        # para evitar depender do argparse do próprio T03.
        from src.trabalhos.t03_operacoes.main_t03 import run_aritmetica, run_geometria

        if args.op:
            # Aritmética requer: --imagem, --imagem2 e --out
            if not (args.imagem and args.imagem2 and args.out):
                raise SystemExit("T03 (arit): use --op {add|sub|mul|div} "
                                 "--imagem <arq> --imagem2 <arq> --out <arq>")
            ns = SimpleNamespace(op=args.op, img=args.imagem, img2=args.imagem2, out=args.out)
            run_aritmetica(ns)
        elif args.gop:
            # Geometria requer: --gop e --imagem e --out (angle/scale/tx/ty/mode conforme gop)
            if not (args.imagem and args.out):
                raise SystemExit("T03 (geo): use --gop {rotate|translate|flip} "
                                 "--imagem <arq> --out <arq> (e parâmetros específicos)")
            ns = SimpleNamespace(
                gop=args.gop, img=args.imagem, out=args.out,
                angle=args.angle, scale=args.scale, tx=args.tx, ty=args.ty, mode=args.mode
            )
            run_geometria(ns)
        else:
            raise SystemExit("T03: especifique --op (aritmética) ou --gop (geométrica).")

    else:
        raise SystemExit("Trabalho não encontrado. Use --menu para abrir o questionário.")

if __name__ == "__main__":
    print(">> Iniciando índice...\n")
    main()
