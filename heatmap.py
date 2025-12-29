#!/usr/bin/env python3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar o Mdb.csv
mdb = pd.read_csv('drep_out/data_tables/Mdb.csv')

# Criar matriz de ANI
ani_matrix = mdb.pivot(index='genome1', columns='genome2', values='similarity')

# Plot do heatmap
plt.figure(figsize=(12,10))
sns.heatmap(ani_matrix, cmap='viridis')
plt.title('Heatmap de ANI entre genomas')
plt.tight_layout()
plt.show()
