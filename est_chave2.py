#!/usr/bin/env python3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Carregar dados
mdb = pd.read_csv('drep_out/data_tables/Mdb.csv')

# Mapas de estado e mês
state_map = {
    'kp_588': 'GO', 'kp_644': 'GO', 'kp_645': 'GO', 'kp_646': 'GO',
    'kp_686': 'PE', 'kp_692': 'PE'
}
month_map = {
    'kp_588': 'Jan/2025', 'kp_644': 'Feb/2025', 'kp_645': 'Mar/2025', 'kp_646': 'Mar/2025',
    'kp_686': 'Apr/2025', 'kp_692': 'Mar/2025'
}

state_palette = {'GO': '#FFA500', 'PE': '#00CED1'}  # cores dos estados
month_palette = {'Jan/2025':'#FF9999','Feb/2025':'#99FF99','Mar/2025':'#9999FF','Apr/2025':'#FFCC99'}

# Função para plotar heatmap
def plot_group_heatmap(df, prefixes, title):
    mask = df['genome1'].str[:6].isin(prefixes) & df['genome2'].str[:6].isin(prefixes)
    ani_matrix = df[mask].pivot(index='genome1', columns='genome2', values='similarity')
    
    # Linhas coloridas
    row_colors = ani_matrix.index.map(lambda x: state_palette[state_map[x[:6]]])
    row_month_colors = ani_matrix.index.map(lambda x: month_palette[month_map[x[:6]]])
    col_colors = ani_matrix.columns.map(lambda x: state_palette[state_map[x[:6]]])
    col_month_colors = ani_matrix.columns.map(lambda x: month_palette[month_map[x[:6]]])
    
    # clustermap
    g = sns.clustermap(
        ani_matrix,
        cmap='viridis',
        row_cluster=False,
        col_cluster=False,
        row_colors=[row_colors, row_month_colors],
        col_colors=[col_colors, col_month_colors],
        figsize=(10,10),
        linewidths=0.5
    )
    g.fig.suptitle(title, fontsize=16)
    
    # Legenda para meses
    month_patches = [Patch(facecolor=color, label=month) for month, color in month_palette.items()]
    # Legenda para estados (apenas cores, sem rótulo)
    state_patches = [Patch(facecolor=color, label='') for color in state_palette.values()]
    
    # Combina legendas
    all_patches = state_patches + month_patches
    g.ax_heatmap.legend(handles=all_patches, bbox_to_anchor=(1.05, -0.05), loc='best', title="Legenda", frameon=False)
    
    plt.show()

# Heatmap geral
all_prefixes = list(state_map.keys())
plot_group_heatmap(mdb, all_prefixes, "Heatmap ANI - Todos os Genomas")

# Heatmaps separados por estado
GO_prefixes = [k for k,v in state_map.items() if v=='GO']
PE_prefixes = [k for k,v in state_map.items() if v=='PE']

plot_group_heatmap(mdb, GO_prefixes, "Heatmap ANI - GO")
plot_group_heatmap(mdb, PE_prefixes, "Heatmap ANI - PE")
