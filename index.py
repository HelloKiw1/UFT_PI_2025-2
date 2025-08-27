#!/usr/bin/env python3
"""
Índice dos Trabalhos de Processamento de Imagens.

Usos:
  # 1) Modo menu (interativo): escolhe o trabalho e o questionário específico roda
  python index.py --menu

  # 2) Modo direto (sem menu): chama o run() do trabalho escolhido
  # Interpolação (Trabalho 1)
  python index.py --trabalho 1 --imagem data/flor.png --metodo bilinear --escala 2.0

  # Rotulação (Trabalho 2)
  python index.py --trabalho 2 --imagem data/manchas.png --thresh 127 --conectividade 4
"""
from __future__ import annotations
import argparse
import importlib

# Para execução DIRETA (sem menu), mapeamos o ID -> função run()
TRABALHOS = {
    "1": ("Interpolação (Vizinho + Bilinear)", "src.trabalhos.t01_interpolacao.main:run"),
    "2": ("Conectividade & Rotulação (4/8)",    "src.trabalhos.t02_rotulacao.main:run"),
}

def _resolver_callable(target: str):
    """
    Recebe 'modulo.submod:func' e retorna o objeto chamável.
    """
    mod_name, func_name = target.split(":")
    mod = importlib.import_module(mod_name)
    return getattr(mod, func_name)

def main():
    parser = argparse.ArgumentParser(description="Índice dos Trabalhos de Processamento de Imagens")
    parser.add_argument("--trabalho", help="ID do trabalho (ex.: 1 ou 2)")
    # Parâmetros possíveis (alguns serão ignorados dependendo do trabalho)
    parser.add_argument("--imagem", help="Caminho da imagem")
    parser.add_argument("--metodo", help="vizinho | bilinear (Trabalho 1)")
    parser.add_argument("--escala", type=float, help=">1 amplia; <1 reduz (Trabalho 1)")
    parser.add_argument("--thresh", type=int, help="Limiar de binarização (Trabalho 2)")
    parser.add_argument("--conectividade", type=int, help="4 ou 8 (Trabalho 2)")
    parser.add_argument("--menu", action="store_true", help="Abre o menu interativo de seleção")
    args = parser.parse_args()

    # Modo MENU GLOBAL: delega para src.menu.questionario_global()
    if args.menu or not args.trabalho:
        from src.menu import questionario_global
        questionario_global()
        return

    # Modo DIRETO: chama o run() do trabalho escolhido
    if args.trabalho not in TRABALHOS:
        raise SystemExit("Trabalho não encontrado. Use --menu para abrir o questionário.")

    _, target = TRABALHOS[args.trabalho]
    run_callable = _resolver_callable(target)

    # Encaminha somente os argumentos relevantes; os demais podem ser None
    if args.trabalho == "1":
        # Trabalho 1 — Interpolação
        run_callable(imagem=args.imagem, metodo=args.metodo, escala=args.escala)
    elif args.trabalho == "2":
        # Trabalho 2 — Conectividade & Rotulação
        run_callable(imagem=args.imagem, thresh=args.thresh, conectividade=args.conectividade)
    else:
        # Se futuramente adicionar novos trabalhos, trate aqui
        raise SystemExit("Trabalho ainda não suportado neste índice.")

if __name__ == "__main__":
    print(">> Iniciando índice...\n")
    main()
