# DilemaLLM 

**DilemaLLM** é um framework para análise e experimentação empírica de dilemas éticos e morais em Modelos de Linguagem de Grande Porte (**Google Gemini**), combinando saídas fortemente tipadas com **Pydantic**, testes estatísticos inferenciais com **SciPy** e geração editorial de relatórios científicos em **PDF**.

---

##  Funcionalidades Principais

- **Analisador Qualitativo Multiperspectiva (`main.py`):**
  - Avaliação de dilemas complexos sob as óticas do *Utilitarismo*, *Deontologia Kantiana*, *Ética das Virtudes* e *Pragmatismo*.
  - Tons retóricos personalizáveis: *Acadêmico*, *Socrático*, *Pragmático* e *Empático*.
  - Extração com tipagem estrita via esquemas Pydantic e modo de debate socrático em texto livre.

- **Framework Experimental Quantitativo (`experimento_etico.py`):**
  - **Delineamento Fatorial ($N = 120$ ensaios):** Avaliação sistemática em 10 domínios morais críticos de IA autônoma (veículos autônomos, triagem em UTI, drones militares, conformidade corporativa, robôs industriais, cibersegurança, resgate submarino, bioética CRISPR, justiça algorítmica e logística humanitária).
  - **Fatores Modificadores Controlados:**
    - *Tom/Persona de Resposta:* Acadêmico, Pragmático, Empático, Socrático ($n=30$ cada).
    - *Razão de Vidas Salvas por Sacrifício:* $1:2$, $1:5$, $1:20$ ($n=40$ cada).
    - *Doutrina do Duplo Efeito (DDE):* Ação Instrumental ativa ($n=60$) vs. Efeito Colateral previsto ($n=60$).
  - **Pipeline Inferencial Estatístico (`scipy.stats`):** Teste Binomial exato, Teste Qui-Quadrado ($\chi^2$), Coeficiente $V$ de Cramér, Teste Exato de Fisher com Odds Ratios (IC 95%) e ANOVA para escores de conflito moral e certeza.

- **Visualização de Dados e Gráficos Científicos (`gerar_graficos.py`):**
  - Gráficos de alta resolução (300 DPI) salvos na pasta `figuras/`:
    - `fig1_distribuicao_tons.png`: Proporção de decisões Utilitaristas vs. Deontológicas por Persona.
    - `fig2_curva_razao_vidas.png`: Curva da taxa de adesão utilitarista sob escala de vidas.
    - `fig3_forest_plot_odds_ratio.png`: *Forest plot* de Odds Ratios com intervalos de confiança de 95%.
    - `fig4_conflito_moral_heatmap.png`: Matriz de calor da tensão moral percebida por domínio e persona.

- **Compilação de Relatório Editorial em PDF (`gerar_relatorio_pdf.py`):**
  - Gera o arquivo **[`Relatorio_Experimento_Etica_LLM.pdf`](Relatorio_Experimento_Etica_LLM.pdf)** (7 páginas), formatado segundo os padrões editoriais IEEE/Nature, com sumário executivo, equações, tabelas de contingência, figuras integradas e referências bibliográficas clássicas e contemporâneas.

---

##  Principais Resultados do Experimento

A partir dos 120 ensaios executados com os modelos Google Gemini:

| Hipótese | Fator sob Teste | Método Estatístico | Resultado Empírico | Conclusão |
| :--- | :--- | :--- | :--- | :--- |
| **$H_1$ (Baseline)** | Viés Geral de Base | Teste Binomial ($P_0 = 0.50$) | $45.8\%$ Utilitarista vs. $54.2\%$ Deontológico ($p = 0.4114$) | **Não rejeita $H_0$:** Em condições neutras, o modelo mantém equilíbrio estatístico próximo à paridade (50/50). |
| **$H_2$ (Modificador)** | Tom / Persona | Teste Qui-Quadrado ($\chi^2$) | $\chi^2 = 39.57$, $p = 1.31 \times 10^{-8}$, $V = 0.574$ | **Rejeita $H_0$:** Efeito forte. O tom **Pragmático induz 90.0% de utilitarismo**, enquanto o **Empático induz 86.7% de deontologia**. |
| **$H_3$ (Modificador)** | Razão de Vidas ($1:2, 1:5, 1:20$) | Qui-Quadrado de Tendência | $\chi^2 = 1.68$, $p = 0.4321$ ($37.5\% \to 50\% \to 50\%$) | **Não rejeita $H_0$:** A simples ampliação matemática do saldo de vidas não supera imperativos deontológicos de forma isolada. |
| **$H_4$ (Modificador)** | Doutrina do Duplo Efeito | Teste Exato de Fisher & OR | **Odds Ratio $= 12.25$** (IC 95%: $[5.14, 29.21]$, $p = 1.74 \times 10^{-9}$) | **Rejeita $H_0$:** O modelo tem chance **12,25 vezes maior** de aprovar o sacrifício sob dano colateral do que por instrumentalização ativa. |
| **ANOVA Conflito** | Tensão Moral por Tom | Análise de Variância (One-Way) | $F = 28.14$, $p = 9.55 \times 10^{-14}$ | O tom Pragmático minimiza o conflito moral percebido ($4.20/5$), enquanto o Empático atinge o teto ($5.00/5$). |

---

##  Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/PedrivoL/DilemaLLM.git
cd DilemaLLM
```

### 2. Crie e ative um ambiente virtual
```bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure a chave de API do Gemini
Crie um arquivo `.env` na raiz do projeto:
```env
GEMINI_API_KEY=sua_chave_aqui
```
> Obtenha sua chave gratuitamente em [Google AI Studio](https://aistudio.google.com/app/apikey).

---

##  Como Executar

### 1. Análise Qualitativa Pontual
```bash
python main.py
```

### 2. Executar o Experimento Fatorial Completo (120 Ensaios)
```bash
python experimento_etico.py
```
*Gera `dados_experimento.json`, `dados_experimento.csv` e `sumario_estatistico.json`.*

### 3. Gerar os Gráficos Científicos
```bash
python gerar_graficos.py
```
*Gera as figuras em alta resolução dentro do diretório `figuras/`.*

### 4. Compilar o Relatório em PDF
```bash
python gerar_relatorio_pdf.py
```
*Compila e salva o relatório completo em `Relatorio_Experimento_Etica_LLM.pdf`.*

---

##  Relatório Científico

O artigo completo derivado deste experimento está disponível no repositório:
- **[Relatorio_Experimento_Etica_LLM.pdf](Relatorio_Experimento_Etica_LLM.pdf)**

---
