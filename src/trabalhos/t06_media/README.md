## Filtro da Média — Implementação, comportamento e tratamento de bordas

Este documento descreve a lógica da implementação do Filtro da Média presente em
`src/trabalhos/t06_media/algorithms.py`. Está escrito em Português e explica o que o
filtro faz, o que deveria fazer, como foi implementado (passo-a-passo) e o efeito dos
modos de borda disponíveis.

## O que o filtro da média faz

O filtro da média (box filter) substitui cada pixel pela média dos valores em uma
janela k×k centrada naquele pixel. O efeito principal é suavização — redução de ruído
de alta frequência — e aumento do desfoque conforme `k` aumenta.

- Entrada: imagem 2D (grayscale) como `np.ndarray` com valores esperados em 0..255.
- Parâmetros: `k` (tamanho da janela, ímpar e ≥ 1) e `border` (modo de tratamento de bordas).
- Saída: imagem 2D `uint8` do mesmo tamanho em que cada pixel é a média local.

O filtro deveria:

- Preservar o mesmo tamanho da imagem de entrada.
- Tratar corretamente pixels próximos às bordas (ver seção de bordas abaixo).
- Ser eficiente (complexidade aceitável para janelas grandes) e numérica estável.

## Contrato simplificado

- Função: `mean_filter(img: np.ndarray, k: int = 3, border: str = "zero") -> np.ndarray`
- Pré-condições: `img` é 2D; `k` é ímpar e >= 1; `border` ∈ {`zero`,`replicate`,`reflect`,`wrap`}.
- Pós-condições: retorna um `np.ndarray` `uint8` com os valores entre 0 e 255.

Se você precisar de suporte a imagens coloridas, aplique o filtro por canal (R,G,B) ou
faça a conversão prealável para grayscale.

## Como a implementação atual funciona (passo-a-passo)

Esta versão do repositório usa a implementação direta (ingênua) do filtro da
média — isto é, a média k×k é calculada somando explicitamente os pixels da janela
para cada posição. É simples e didática, porém menos eficiente que a versão com
imagem integral.

1. Normalização do tipo de dado

   - `ensure_u8(img)` garante que os valores estejam entre 0 e 255 e converte para
     `np.uint8` quando necessário. Isso evita problemas de overflow/underflow ao final.

2. Validação de `k`

   - O código valida que `k` seja ímpar e ≥ 1. Janelas pares não têm um único pixel
     central, portanto não são permitidas.

3. Padding / tratamento de bordas

   - Calcula-se `pad = k // 2`.
   - `_pad(img, pad, border)` usa `numpy.pad` com modos mapeados:
     - `zero` → `mode="constant"`, preenche com zero (borda preta).
     - `replicate` → `mode="edge"`, repete o píxel mais externo.
     - `reflect` → `mode="reflect"`, espelha a imagem ao redor da borda.
     - `wrap` → `mode="wrap"`, trata a imagem como periódica (torna a borda conectada à outra extremidade).

   - O padding permite calcular janelas centradas nos pixels na vizinhança das bordas
     sem sair dos limites do array.

4. Cálculo ingênuo das médias

   - Para cada pixel `(y,x)` da imagem original, o algoritmo soma os valores de
     `padded[y : y+k, x : x+k]` (janela k×k) usando loops explícitos e depois divide
     pela área `k*k` para obter a média.

5. Conversão e retorno

   - O resultado (float) é convertido com `ensure_u8()` para `uint8` e retornado.

## Complexidade

- Implementação direta (somando k×k por pixel) tem custo O(H·W·k²).
- Com imagem integral, o custo passa a O(H·W) (quatro acessos por pixel), o que é
  muito mais eficiente para janelas grandes.

## Tratamento de borda (fixo: zero)

Esta implementação utiliza apenas o tratamento de borda `zero` (padding com
zeros). Ou seja, regiões fora da imagem são tratadas como valor 0 ao computar a
média das janelas k×k. Esse método é simples e determinístico, mas introduz um
halo escuro nas margens para janelas grandes.

Resumo do efeito:

- Preenche externamente com zeros (borda preta).
- Efeito: bordas tendem a ficar mais escuras, especialmente com janelas maiores.

## Exemplo de uso (linha de comando)

Executar sem visualização (gera arquivo em `outputs/`):

```powershell
# usando o venv do projeto (criado pela configuração automática)
C:/Users/eduar/Documents/GitHub/UFT_PI_2025-2/.venv/Scripts/python.exe -m src.trabalhos.t06_media.main_t06 media --imagem data/flor.png --k 3 --border zero --no-show
```

Ou, em ambiente onde `python` já aponta para o interpretador correto:

```powershell
python -m src.trabalhos.t06_media.main_t06 media --imagem data/flor.png --k 5 --border replicate
```

Os arquivos gerados são salvos em `outputs/` com nome automático que inclui timestamp.

## Testes rápidos para validar

1. k = 1 na imagem qualquer deve retornar a própria imagem (sem alteração).
2. Imagem constante: qualquer k deve retornar a mesma imagem constante.
3. Pequena imagem conhecida (por exemplo 3×3 com valores definidos) e k=3 — calcule
   manualmente a média e compare com o resultado do `mean_filter`.

## Possíveis melhorias

- Suporte nativo a imagens coloridas (aplicar por canal).
- Opção para retornar `float32` normalizado (0..1) em vez de quantizar para `uint8`.
- Comparação de desempenho com implementações em OpenCV / SciPy ou com convolução
  separável (1D horizontal + 1D vertical).

---

Se quiser, eu posso:

- Implementar suporte RGB no `mean_filter` e adicionar testes automáticos.
- Adicionar um pequeno notebook que mostra visualmente a diferença entre os modos de borda.

Escolha uma das opções acima ou peça para eu ajustar o texto do README.
