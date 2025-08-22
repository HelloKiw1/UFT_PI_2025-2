#!/usr/bin/env python3
import argparse
import importlib

TRABALHOS = {
    "1": ("Interpolação (Vizinho + Bilinear)", "src.trabalhos.t01_interpolacao.main:run"),
}

def _resolver_callable(target: str):
    mod_name, func_name = target.split(":")
    mod = importlib.import_module(mod_name)
    return getattr(mod, func_name)

def _questionario():
    print("=== Questionário — Selecione o trabalho ===")
    for k, (nome, _) in TRABALHOS.items():
        print(f"[{k}] {nome}")
    escolha = input("Digite o número do trabalho: ").strip()
    if escolha not in TRABALHOS:
        print("Opção inválida.")
        return
    nome, target = TRABALHOS[escolha]
    print(f"Selecionado: {nome}\n")

    imagem = input("Caminho da imagem (ex: data/flor.jpg): ").strip() or "data/flor.jpg"
    metodo = input("Método (vizinho/bilinear) [bilinear]: ").strip().lower() or "bilinear"
    escala = float(input("Escala (>1 amplia, <1 reduz) [2.0]: ").strip() or "2.0")

    callable_ = _resolver_callable(target)
    callable_(imagem=imagem, metodo=metodo, escala=escala)

def main():
    parser = argparse.ArgumentParser(description="Índice dos Trabalhos de Processamento de Imagens")
    parser.add_argument("--trabalho", help="ID do trabalho (ex: 1)")
    parser.add_argument("--imagem", help="Caminho da imagem")
    parser.add_argument("--metodo", help="vizinho | bilinear")
    parser.add_argument("--escala", type=float, help=">1 amplia; <1 reduz")
    parser.add_argument("--menu", action="store_true", help="Força o questionário interativo")
    args = parser.parse_args()

    if args.menu or not args.trabalho:
        _questionario()
        return

    if args.trabalho not in TRABALHOS:
        raise SystemExit("Trabalho não encontrado. Use --menu para abrir o questionário.")

    _, target = TRABALHOS[args.trabalho]
    callable_ = _resolver_callable(target)
    callable_(imagem=args.imagem, metodo=args.metodo, escala=args.escala)

if __name__ == "__main__":
    print(">> Iniciando índice...\n")  # debug visível
    main()
