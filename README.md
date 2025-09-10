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

### 🔹 Trabalho 05 — Processamento de Histogramas  
**Título:** *Equalização de Histograma e Alargamento de Contraste (Contrast Stretching)*  

📅 **Entrega:** 18/09/2025  

---

### 🔹 Trabalho 06 — Filtro da Média  
**Título:** *Filtro de Suavização pela Média com diferentes estratégias de borda*  

📅 **Entrega:** 25/09/2025  

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
│     ├─ t03_operacoes/           # Trabalho 03 - Operações Aritméticas & Geométricas
│     │   ├─ main_t03.py
│     │   ├─ aritmetica.py
│     │   ├─ geometria.py
│     │   └─ io_utils.py
│     ├─ t05_histogramas/         # Trabalho 05 - Processamento de Histogramas
│     │   ├─ main_t05.py
│     │   ├─ algorithms.py
│     │   └─ __init__.py
│     └─ t06_media/               # Trabalho 06 - Filtro da Média
│         ├─ main_t06.py
│         ├─ algorithms.py
│         └─ __init__.py
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
.\.venv\Scriptsctivate
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

### 4. Rodar diretamente (sem menu)
- **Trabalho 01 (Interpolação):**
```powershell
python index.py --trabalho 1 --imagem data/flor.png --metodo bilinear --escala 2.0
```

- **Trabalho 02 (Rotulação):**
```powershell
python index.py --trabalho 2 --imagem data/manchas.png --thresh 127 --conectividade 4
```

- **Trabalho 03 (Operações):**
```powershell
# Aritmética
python -m src.trabalhos.t03_operacoes.main_t03 arit --op add --imagem data/flor.png --imagem2 data/manchas.png

# Geometria
python -m src.trabalhos.t03_operacoes.main_t03 geo --gop rotate --imagem data/flor.png --angle 45
```

- **Trabalho 05 (Histogramas):**
```powershell
# Equalização (L=256)
python -m src.trabalhos.t05_histogramas.main_t05 eq --imagem data/flor.png

# Contrast Stretching (c/d automáticos)
python -m src.trabalhos.t05_histogramas.main_t05 stretch --imagem data/flor.png --a 0 --b 255
```

- **Trabalho 06 (Filtro da Média):**
```powershell
# Janela 3x3, borda zero
python -m src.trabalhos.t06_media.main_t06 media --imagem data/flor.png --k 3 --border zero

# Janela 5x5, borda periódica
python -m src.trabalhos.t06_media.main_t06 media --imagem data/flor.png --k 5 --border wrap
```

---

## 📊 Saídas

- Todos os resultados são salvos automaticamente em `outputs/` com **timestamp** no nome.  
- **Trabalho 01:** mostra **Original vs Resultado (Interpolação)**.  
- **Trabalho 02:** mostra **Imagem Grayscale, Binária e Rotulada (cores aleatórias por componente)**.  
- **Trabalho 03:** mostra **Original vs Resultado (operação escolhida)**.  
- **Trabalho 05:** mostra **Original vs Equalizada/Contrast Stretching + histogramas**.  
- **Trabalho 06:** mostra **Original vs Resultado (média k×k, borda escolhida)**.  

---

## ✅ Dependências
- [numpy](https://numpy.org/)  
- [pillow](https://pillow.readthedocs.io/en/stable/)  
- [matplotlib](https://matplotlib.org/)  