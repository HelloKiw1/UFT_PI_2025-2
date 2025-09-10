# 📌 UFT_PI_2025-2  
**Disciplina:** Processamento de Imagens — 2025/2  
**Professora:** Dra. Glenda Botelho  

Repositório destinado ao armazenamento e desenvolvimento dos trabalhos práticos da disciplina.  

---

## 👥 Grupo
- [Eduardo Henrique](https://github.com/HelloKiw1)  
- [Shayla Alves](https://github.com/shaylaalves)  

---

## 📝 Trabalhos  

### 🔹 Trabalho 01 — Interpolação  
**Título:** *Interpolação por Vizinho Mais Próximo e Interpolação Bilinear (redução e ampliação)*  

📅 **Entrega:** 28/08/2025  

---

### 🔹 Trabalho 02 — Conectividade & Rotulação  
**Título:** *Rotulação de Componentes Conectados (4 e 8-conectividade)*  

📅 **Entrega:** 04/09/2025  

---

### 🔹 Trabalho 03 — Operações Aritméticas & Geométricas  
**Título:** *Adição, Subtração, Multiplicação, Divisão e Transformações (Rotação, Translação, Espelhamento)*  

📅 **Entrega:** 11/09/2025  

---

## 📂 Estrutura do Repositório
```
UFT_PI_2025-2/
├─ index.py                       # Menu inicial para escolher e rodar os trabalhos
├─ src/
│  ├─ menu.py                     # Questionário global (seleção do trabalho)
│  └─ trabalhos/
│     ├─ t01_interpolacao/        # Trabalho 01 - Interpolação
│     │   ├─ main.py
│     │   ├─ algorithms/          # Algoritmos de interpolação
│     │   └─ io_utils.py
│     ├─ t02_rotulacao/           # Trabalho 02 - Conectividade & Rotulação
│     │   ├─ main.py
│     │   └─ algorithms/          # Algoritmos de rotulação
│     └─ t03_operacoes/           # Trabalho 03 - Operações Aritméticas & Geométricas
│         ├─ main_t03.py          # Execução (run_aritmetica, run_geometria, questionário, CLI)
│         ├─ aritmetica.py        # Implementação das operações aritméticas
│         ├─ geometria.py         # Implementação das operações geométricas
│         └─ io_utils.py          s
├─ data/                          # Imagens de entrada para testes
├─ outputs/                       # Resultados gerados automaticamente
├─ requirements.txt               # Dependências do projeto
└─ README.md                      # Este arquivo
```

---

## 🚀 Como rodar

### 1. Criar ambiente virtual
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Instalar dependências
```powershell
pip install -r requirements.txt
```

### 3. Rodar o menu interativo
```powershell
python index.py --menu
```
➡️ Será exibido um menu perguntando **qual trabalho** deseja executar.  
Cada trabalho possui seu **questionário próprio** (parâmetros específicos).  

---

## 📊 Saídas

- Todos os resultados são salvos automaticamente em `outputs/` com **timestamp** no nome.  
- **Trabalho 01:** mostra **Original vs Resultado (Interpolação)**.  
- **Trabalho 02:** mostra **Imagem Grayscale, Binária e Rotulada (cores aleatórias por componente)**.  
- **Trabalho 03:** mostra **Original vs Resultado (operação escolhida)** e gera nomes descritivos, ex.:  
  ```
  outputs/t03_add__flor__manchas__20250910_174500.png
  outputs/t03_rotate__flor__ang45__20250910_175200.png
  ```

---

## ✅ Dependências
- [numpy](https://numpy.org/)  
- [pillow](https://pillow.readthedocs.io/en/stable/)  
- [matplotlib](https://matplotlib.org/)  
