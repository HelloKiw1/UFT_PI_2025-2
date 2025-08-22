# 📌 UFT_PI_2025-2  
**Disciplina:** Processamento de Imagens — 2025/2  
**Professora:** Dra. Glenda Botelho  

Repositório destinado ao armazenamento e desenvolvimento dos trabalhos práticos da disciplina.  

---

## 👥 Grupo
- [Eduardo Henrique](https://github.com/HelloKiw1)  
- [Shayla Alves](https://github.com/shaylaalves)  

---

## 📝 Trabalho 01 — Interpolação
**Título:** *Interpolação por Vizinho Mais Próximo e Interpolação Bilinear (redução e ampliação)*  

📅 **Entrega:** 28/08/2025  
📧 **Submissão:** glendabotelho@uft.edu.br  
⚠️ **Observação:** É necessário apresentar o código no final da aula.  

---

## 📂 Estrutura do Repositório
```
UFT_PI_2025-2/
├─ index.py                 # Menu inicial para escolher e rodar os trabalhos
├─ requirements.txt         # Dependências do projeto
├─ README.md                # Este arquivo
├─ data/                    # Imagens de entrada para testes
├─ outputs/                 # Resultados gerados automaticamente
├─ src/
│  └─ trabalhos/
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

### 3. Executar pelo **índice interativo**
```powershell
python index.py
```
➡️ Aparecerá um menu perguntando qual trabalho deseja rodar, a imagem de entrada, o método e o fator de escala.  

---

## 📊 Saída
- Os resultados são salvos automaticamente em `outputs/` com timestamp no nome.  
- Uma janela será aberta exibindo **Original vs Resultado** para comparação.  

---

## ✅ Dependências
- [numpy](https://numpy.org/)  
- [pillow](https://pillow.readthedocs.io/en/stable/)  
- [matplotlib](https://matplotlib.org/) (visualização)  

---