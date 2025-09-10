# src/menu.py
from __future__ import annotations
import importlib

TRABALHOS = {
    "1": ("Interpolação (Vizinho + Bilinear)", "src.trabalhos.t01_interpolacao.main:questionario"),
    "2": ("Conectividade & Rotulação (4/8)",    "src.trabalhos.t02_rotulacao.main:questionario"),
    "3": ("Operações Aritméticas & Geométricas","src.trabalhos.t03_operacoes.main_t03:questionario"),
    "5": ("Processamento de Histogramas",       "src.trabalhos.t05_histogramas.main_t05:questionario"),
    "6": ("Filtro da Média (suavização)",       "src.trabalhos.t06_media.main_t06:questionario"),
}

def _resolver_callable(target: str):
    mod_name, func_name = target.split(":")
    mod = importlib.import_module(mod_name)
    return getattr(mod, func_name)

def questionario_global():
    print("=== Questionário — Selecione o trabalho ===")
    for k, (nome, _) in TRABALHOS.items():
        print(f"[{k}] {nome}")
    escolha = input("Digite o número do trabalho: ").strip()

    if escolha not in TRABALHOS:
        print("Opção inválida.")
        return

    nome, target = TRABALHOS[escolha]
    print(f"Selecionado: {nome}\n")

    callable_ = _resolver_callable(target)
    callable_()
