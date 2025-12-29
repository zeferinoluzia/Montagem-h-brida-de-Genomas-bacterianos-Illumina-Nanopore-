#!/usr/bin/env python3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------
# Carregar dados
# -------------------------------
mdb = pd.read_csv('drep_out/data_tables/Mdb.csv')

# Função para filtrar por prefixos de genoma
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
# Heatmaps por estado
# -------------------------------
# Definir prefixos
GO_prefixes = ['kp_588','kp_644','kp_645','kp_646']
PE_prefixes = ['kp_686','kp_692']

# Filtrar
mdb_GO = filter_genomes(mdb, GO_prefixes)
mdb_PE = filter_genomes(mdb, PE_prefixes)

# Criar matrizes
ani_matrix_GO = mdb_GO.pivot(index='genome1', columns='genome2', values='similarity')
ani_matrix_PE = mdb_PE.pivot(index='genome1', columns='genome2', values='similarity')

# Plot GO
plt.figure(figsize=(10,8))
sns.heatmap(ani_matrix_GO, cmap='viridis')
plt.title('Heatmap ANI - GO (kp_588, 644, 645, 646)')
plt.tight_layout()
plt.show()

# Plot PE
plt.figure(figsize=(10,8))
sns.heatmap(ani_matrix_PE, cmap='viridis')
plt.title('Heatmap ANI - PE (kp_686, 692)')
plt.tight_layout()
plt.show()
