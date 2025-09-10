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

  # T03 – Operações
  python index.py --trabalho 3

  # T05 – Histogramas
  python index.py --trabalho 5

  # T06 – Filtro da Média
  python index.py --trabalho 6
"""
from __future__ import annotations
import argparse
import importlib

TRABALHOS = {
    "1": ("Interpolação (Vizinho + Bilinear)", "src.trabalhos.t01_interpolacao.main:run"),
    "2": ("Conectividade & Rotulação (4/8)",    "src.trabalhos.t02_rotulacao.main:run"),
    "3": ("Operações Aritméticas & Geométricas","src.trabalhos.t03_operacoes.main_t03:questionario"),
    "5": ("Processamento de Histogramas",       "src.trabalhos.t05_histogramas.main_t05:questionario"),
    "6": ("Filtro da Média (suavização)",       "src.trabalhos.t06_media.main_t06:questionario"),
}

def _resolver_callable(target: str):
    mod_name, func_name = target.split(":")
    mod = importlib.import_module(mod_name)
    return getattr(mod, func_name)

def main():
    parser = argparse.ArgumentParser(description="Índice dos Trabalhos de Processamento de Imagens")
    parser.add_argument("--trabalho", help="ID do trabalho (ex.: 1, 2, 3, 5 ou 6)")
    parser.add_argument("--menu", action="store_true", help="Abre o menu interativo de seleção")

    # ---- Parâmetros T01 ----
    parser.add_argument("--imagem", help="Caminho da imagem (T01/T02)")
    parser.add_argument("--metodo", help="vizinho | bilinear (T01)")
    parser.add_argument("--escala", type=float, help=">1 amplia; <1 reduz (T01)")

    # ---- Parâmetros T02 ----
    parser.add_argument("--thresh", type=int, help="Limiar de binarização (T02)")
    parser.add_argument("--conectividade", type=int, help="4 ou 8 (T02)")

    args = parser.parse_args()

    if args.menu or not args.trabalho:
        from src.menu import questionario_global
        questionario_global()
        return

    if args.trabalho not in TRABALHOS:
        raise SystemExit("Trabalho não encontrado. Use --menu para abrir o questionário.")

    nome, target = TRABALHOS[args.trabalho]
    print(f"Selecionado: {nome}\n")
    callable_ = _resolver_callable(target)

    if args.trabalho == "1":
        callable_(imagem=args.imagem, metodo=args.metodo, escala=args.escala)

    elif args.trabalho == "2":
        callable_(imagem=args.imagem, thresh=args.thresh, conectividade=args.conectividade)

    elif args.trabalho in {"3", "5", "6"}:
        callable_()

    else:
        raise SystemExit("Trabalho ainda não suportado neste índice.")

if __name__ == "__main__":
    print(">> Iniciando índice...\n")
    main()
