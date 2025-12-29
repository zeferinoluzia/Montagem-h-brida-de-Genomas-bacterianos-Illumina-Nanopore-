#!/usr/bin/env python3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------
# Carregar tabelas do dRep
# -------------------------------
widb = pd.read_csv('drep_out/data_tables/Widb.csv')
clusters = pd.read_csv('drep_out/data_tables/Cdb.csv')
mdb = pd.read_csv('drep_out/data_tables/Mdb.csv')

# -------------------------------
# Scatterplot: Completude vs Contaminação
# -------------------------------
widb['cluster'] = widb['cluster'].astype(str)  # garantir categórico
plt.figure(figsize=(10,7))

ax = sns.scatterplot(
    data=widb,
    x='completeness',
    y='contamination',
    hue='cluster',
    palette='tab20',
    s=100,
    edgecolor='black'
)

plt.axvline(90, color='red', linestyle='--')
plt.axhline(5, color='blue', linestyle='--')
plt.title('Completude vs Contaminação por Cluster', fontsize=16)
plt.xlabel('Completude (%)')
plt.ylabel('Contaminação (%)')

# Ajustar legenda corretamente usando ax
ax.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# -------------------------------
# Histograma de ANI por cluster
# -------------------------------

# Adicionar cluster de genome1
mdb = mdb.merge(
    clusters[['genome','primary_cluster']],
    left_on='genome1',
    right_on='genome',
    how='left'
)
mdb.rename(columns={'primary_cluster':'cluster1'}, inplace=True)
mdb.drop(columns='genome', inplace=True)
mdb['cluster1'] = mdb['cluster1'].astype(str)  # categórico

plt.figure(figsize=(10,7))
ax = sns.histplot(
    data=mdb,
    x='similarity',
    hue='cluster1',
    bins=30,
    palette='tab20',
    multiple='stack'
)

plt.title('Distribuição de ANI entre pares de genomas por Cluster', fontsize=16)
plt.xlabel('ANI')
plt.ylabel('Frequência')

# Ajustar legenda corretamente usando ax
ax.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
