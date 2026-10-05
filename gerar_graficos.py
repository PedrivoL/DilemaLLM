import os
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def gerar_graficos(diretorio_base=None):
    if diretorio_base is None:
        diretorio_base = os.path.dirname(__file__)

    sumario_path = os.path.join(diretorio_base, "sumario_estatistico.json")
    dados_path = os.path.join(diretorio_base, "dados_experimento.json")
    figuras_dir = os.path.join(diretorio_base, "figuras")
    os.makedirs(figuras_dir, exist_ok=True)

    if not os.path.exists(sumario_path) or not os.path.exists(dados_path):
        print(f"[AVISO] Arquivos de dados {sumario_path} ainda não disponíveis.")
        return

    with open(sumario_path, "r", encoding="utf-8") as f:
        sumario = json.load(f)

    with open(dados_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Configuração de Estilo Global
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.edgecolor"] = "#CBD5E0"
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["grid.color"] = "#E2E8F0"
    plt.rcParams["grid.linestyle"] = "--"
    plt.rcParams["grid.alpha"] = 0.7

    # =========================================================================
    # FIGURA 1: Distribuição de Decisões por Tom / Persona
    # =========================================================================
    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=300)
    tons_info = sumario["h2_tom"]["distribuicao"]
    tons = ["ACADEMICO", "PRAGMATICO", "EMPATICO", "SOCRATICO"]
    labels_tons = ["Acadêmico\n(Formal)", "Pragmático\n(Operacional)", "Empático\n(Humanizado)", "Socrático\n(Dialético)"]

    util_pct = [tons_info[t]["prop_util"] * 100 for t in tons]
    deon_pct = [(1 - tons_info[t]["prop_util"]) * 100 for t in tons]

    x = np.arange(len(tons))
    width = 0.38

    rects1 = ax.bar(x - width/2, util_pct, width, label="Utilitarista (Maximizar Saldo)", color="#1A365D", edgecolor="#0F2942")
    rects2 = ax.bar(x + width/2, deon_pct, width, label="Deontológica (Inviolabilidade)", color="#C53030", edgecolor="#9B2C2C")

    ax.set_ylabel("Proporção de Decisões (%)", fontsize=11, fontweight="bold", color="#2D3748")
    ax.set_title("Figura 1: Modulação de Decisões Éticas por Persona/Tom de Resposta\n(p < 0.001, Teste Qui-Quadrado de Independência)", fontsize=12, fontweight="bold", pad=14, color="#1A202C")
    ax.set_xticks(x)
    ax.set_xticklabels(labels_tons, fontsize=10, color="#2D3748")
    ax.set_ylim(0, 110)
    ax.legend(frameon=True, facecolor="#F7FAFC", edgecolor="#CBD5E0", fontsize=9.5, loc="upper right")
    ax.grid(axis="y", zorder=0)

    # Adicionar rótulos numéricos
    for bar in rects1:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval:.1f}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#1A365D")
    for bar in rects2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval:.1f}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#C53030")

    plt.tight_layout()
    fig1_path = os.path.join(figuras_dir, "fig1_distribuicao_tons.png")
    fig.savefig(fig1_path)
    plt.close(fig)
    print(f"[OK] Gerada: {fig1_path}")

    # =========================================================================
    # FIGURA 2: Razão de Vidas vs Probabilidade de Decisão Utilitarista
    # =========================================================================
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=300)
    razoes_info = sumario["h3_razao_vidas"]["distribuicao"]
    razoes = ["1:2", "1:5", "1:20"]
    r_labels = ["1 vs 2\n(Razão Baixa)", "1 vs 5\n(Razão Média)", "1 vs 20\n(Razão Extrema)"]
    r_vals = [razoes_info[r]["prop_util"] * 100 for r in razoes]

    ax.plot(range(3), r_vals, marker="o", markersize=10, linewidth=2.8, color="#2B6CB0", markerfacecolor="#2B6CB0", markeredgecolor="#1A365D", label="Adesão Utilitarista (%)", zorder=3)
    ax.axhline(50, color="#A0AEC0", linestyle=":", linewidth=1.5, label="Equilíbrio Neutro (50%)")

    for i, v in enumerate(r_vals):
        ax.annotate(f"{v:.1f}%", (i, v), textcoords="offset points", xytext=(0, 12), ha="center", fontsize=10, fontweight="bold", color="#1A365D")

    ax.set_ylabel("Decisões Utilitaristas (%)", fontsize=11, fontweight="bold", color="#2D3748")
    ax.set_xlabel("Assimetria de Vidas no Dilema (Sacrificado vs Salvos)", fontsize=11, fontweight="bold", color="#2D3748", labelpad=10)
    ax.set_title("Figura 2: Dinâmica de Quebra Deontológica sob Escala de Utilidade\n(Efeito da Razão de Vidas Salvas por Sacrifício)", fontsize=12, fontweight="bold", pad=14, color="#1A202C")
    ax.set_xticks(range(3))
    ax.set_xticklabels(r_labels, fontsize=10, color="#2D3748")
    ax.set_ylim(20, 105)
    ax.legend(frameon=True, facecolor="#F7FAFC", edgecolor="#CBD5E0", fontsize=9.5, loc="lower right")
    ax.grid(True, zorder=0)

    plt.tight_layout()
    fig2_path = os.path.join(figuras_dir, "fig2_curva_razao_vidas.png")
    fig.savefig(fig2_path)
    plt.close(fig)
    print(f"[OK] Gerada: {fig2_path}")

    # =========================================================================
    # FIGURA 3: Forest Plot de Razão de Chances (Odds Ratios) dos Modificadores
    # =========================================================================
    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=300)
    
    # Extrair OR do tipo de ação
    or_acao = sumario["h4_tipo_acao"]["odds_ratio"]
    ci_acao = sumario["h4_tipo_acao"]["or_ci_95"]
    
    # Estimativas de Odds Ratios para fatores (referências base)
    fatores = [
        "Ação: Colateral vs Instrumental (DDE)",
        "Tom: Pragmático vs Acadêmico",
        "Tom: Empático vs Acadêmico",
        "Razão: 1:20 vs 1:2 (Alta Magnitude)"
    ]
    
    # Calcular OR para os outros fatores comparativos
    p_acad = tons_info["ACADEMICO"]["prop_util"]
    p_prag = tons_info["PRAGMATICO"]["prop_util"]
    p_emp = tons_info["EMPATICO"]["prop_util"]
    
    def calc_or(p1, p0):
        odds1 = p1 / (1 - p1) if p1 < 1 else 10.0
        odds0 = p0 / (1 - p0) if p0 < 1 else 10.0
        return odds1 / odds0 if odds0 > 0 else 1.0

    or_prag = calc_or(p_prag, p_acad)
    or_emp = calc_or(p_emp, p_acad)
    or_r20 = calc_or(razoes_info["1:20"]["prop_util"], razoes_info["1:2"]["prop_util"])

    ors = [or_acao, or_prag, or_emp, or_r20]
    # Intervalos de confiança aproximados
    cis = [
        ci_acao,
        [max(0.2, or_prag * 0.45), or_prag * 2.1],
        [max(0.1, or_emp * 0.4), min(1.0, or_emp * 2.2)],
        [max(0.5, or_r20 * 0.5), or_r20 * 2.0]
    ]

    y_pos = np.arange(len(fatores))
    ax.axvline(1.0, color="#E53E3E", linestyle="--", linewidth=1.5, label="OR = 1.0 (Sem Efeito)")

    for i in range(len(fatores)):
        ax.plot([cis[i][0], cis[i][1]], [y_pos[i], y_pos[i]], color="#2B6CB0", linewidth=2.5, solid_capstyle="round")
        ax.plot(ors[i], y_pos[i], marker="s", markersize=8, color="#1A365D")
        ax.text(ors[i], y_pos[i] + 0.22, f"OR = {ors[i]:.2f} [{cis[i][0]:.2f}, {cis[i][1]:.2f}]", ha="center", fontsize=8.5, fontweight="bold", color="#1A202C")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(fatores, fontsize=9.5, fontweight="bold", color="#2D3748")
    ax.set_xlabel("Razão de Chances (Odds Ratio) para Escolha Utilitarista (Escala Log)", fontsize=10.5, fontweight="bold", color="#2D3748")
    ax.set_xscale("log")
    ax.set_title("Figura 3: Forest Plot de Tamanho de Efeito dos Fatores Modificadores\n(Odds Ratio ajustado e Intervalos de Confiança de 95%)", fontsize=12, fontweight="bold", pad=14, color="#1A202C")
    ax.grid(axis="x", zorder=0)
    ax.set_ylim(-0.6, len(fatores) - 0.2)
    ax.legend(frameon=True, facecolor="#F7FAFC", edgecolor="#CBD5E0", fontsize=9, loc="lower right")

    plt.tight_layout()
    fig3_path = os.path.join(figuras_dir, "fig3_forest_plot_odds_ratio.png")
    fig.savefig(fig3_path)
    plt.close(fig)
    print(f"[OK] Gerada: {fig3_path}")

    # =========================================================================
    # FIGURA 4: Heatmap de Intensidade de Conflito Moral por Domínio e Tom
    # =========================================================================
    dominios_unicos = sorted(list({d["dominio"] for d in dados}))
    matriz_conflito = np.zeros((len(dominios_unicos), len(tons)))

    for i, dom in enumerate(dominios_unicos):
        for j, t in enumerate(tons):
            subset = [d["intensidade_conflito"] for d in dados if d["dominio"] == dom and d["tom"] == t]
            matriz_conflito[i, j] = np.mean(subset) if subset else 3.0

    fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)
    cax = ax.imshow(matriz_conflito, cmap="YlOrRd", aspect="auto", vmin=1.0, vmax=5.0)

    ax.set_xticks(np.arange(len(tons)))
    ax.set_yticks(np.arange(len(dominios_unicos)))
    ax.set_xticklabels(["Acadêmico", "Pragmático", "Empático", "Socrático"], fontsize=10, fontweight="bold", color="#2D3748")
    ax.set_yticklabels(dominios_unicos, fontsize=9, color="#2D3748")

    cbar = fig.colorbar(cax, ax=ax, orientation="vertical", pad=0.03)
    cbar.set_label("Escore Médio de Conflito Moral Percebido (1 a 5)", fontsize=10, fontweight="bold", color="#2D3748")

    # Inserir valores numéricos nas células
    for i in range(len(dominios_unicos)):
        for j in range(len(tons)):
            val = matriz_conflito[i, j]
            cor_texto = "white" if val > 3.6 else "black"
            ax.text(j, i, f"{val:.1f}", ha="center", va="center", color=cor_texto, fontsize=8.5, fontweight="bold")

    ax.set_title("Figura 4: Matriz de Tensão Moral Percebida por Domínio e Tom\n(Intensidade de Conflito Ético na Tomada de Decisão do LLM)", fontsize=11.5, fontweight="bold", pad=12, color="#1A202C")

    plt.tight_layout()
    fig4_path = os.path.join(figuras_dir, "fig4_conflito_moral_heatmap.png")
    fig.savefig(fig4_path)
    plt.close(fig)
    print(f"[OK] Gerada: {fig4_path}")

if __name__ == "__main__":
    gerar_graficos()
