#!/usr/bin/env python3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------
# Carregar dados
# -------------------------------
mdb = pd.read_csv('drep_out/data_tables/Mdb.csv')

# -------------------------------
# Função para filtrar por prefixos
# -------------------------------
def filter_genomes(df, prefixes):
    mask = df['genome1'].str[:6].isin(prefixes) & df['genome2'].str[:6].isin(prefixes)
    return df[mask]

# -------------------------------
# Heatmap geral (todos os genomas)
# -------------------------------
ani_matrix_all = mdb.pivot(index='genome1', columns='genome2', values='similarity')

plt.figure(figsize=(12,10))
sns.heatmap(ani_matrix_all, cmap='viridis')
plt.title('Heatmap geral de ANI entre genomas')
plt.tight_layout()
plt.show()

# -------------------------------
# Heatmaps por estado com meses
# -------------------------------
# Definir prefixos
GO_prefixes = ['kp_588','kp_644','kp_645','kp_646']
PE_prefixes = ['kp_686','kp_692']

# Meses correspondentes
month_map = {
    'kp_588': 'Jan/2025',
    'kp_644': 'Feb/2025',
    'kp_645': 'Mar/2025',
    'kp_646': 'Mar/2025',
    'kp_686': 'Apr/2025',
    'kp_692': 'Mar/2025'
}

# Filtrar
mdb_GO = filter_genomes(mdb, GO_prefixes)
mdb_PE = filter_genomes(mdb, PE_prefixes)

# Criar matrizes
ani_matrix_GO = mdb_GO.pivot(index='genome1', columns='genome2', values='similarity')
ani_matrix_PE = mdb_PE.pivot(index='genome1', columns='genome2', values='similarity')

# Adicionar meses nos labels do eixo
ani_matrix_GO.index = [f"{g}\n({month_map[g[:6]]})" for g in ani_matrix_GO.index]
ani_matrix_GO.columns = [f"{g}\n({month_map[g[:6]]})" for g in ani_matrix_GO.columns]

ani_matrix_PE.index = [f"{g}\n({month_map[g[:6]]})" for g in ani_matrix_PE.index]
ani_matrix_PE.columns = [f"{g}\n({month_map[g[:6]]})" for g in ani_matrix_PE.columns]

# Plot GO
plt.figure(figsize=(10,8))
sns.heatmap(ani_matrix_GO, cmap='viridis')
plt.title('Heatmap ANI - GO')
plt.tight_layout()
plt.show()

# Plot PE
plt.figure(figsize=(8,6))
sns.heatmap(ani_matrix_PE, cmap='viridis')
plt.title('Heatmap ANI - PE')
plt.tight_layout()
plt.show()
