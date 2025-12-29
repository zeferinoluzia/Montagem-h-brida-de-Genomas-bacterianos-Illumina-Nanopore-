#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os

# =====================
# 1. Encontrar todos os arquivos CSV dentro das pastas kp_*
# =====================
arquivos = glob.glob("kp_*/*.csv")
print(f"Total de arquivos encontrados: {len(arquivos)}")

dfs = []

for arquivo in arquivos:
    # Extrair o nome da pasta (cepa)
    cepa = os.path.basename(os.path.dirname(arquivo))  # exemplo: kp_644
    
    # Ler CSV e corrigir espaços no cabeçalho
    df = pd.read_csv(arquivo, sep=",")
    df.columns = df.columns.str.strip()
    
    if "GENE" not in df.columns:
        raise ValueError(f"A coluna 'GENE' não foi encontrada no arquivo {arquivo}. Colunas disponíveis: {df.columns.tolist()}")
    
    # Adicionar coluna com nome da cepa
    df["CEPA"] = cepa
    
    # Adicionar apenas CEPA e GENE
    dfs.append(df[["CEPA", "GENE"]])

# =====================
# 2. Concatenar todos os dados
# =====================
df_genes = pd.concat(dfs, ignore_index=True)

# =====================
# 3. Criar matriz presença/ausência
# =====================
matriz_genes = (df_genes.assign(presente=1)
                .pivot_table(index="CEPA", columns="GENE", values="presente", fill_value=0))

# Garantir ordem alfabética dos genes
todos_os_genes = sorted(df_genes["GENE"].unique())
matriz_genes = matriz_genes.reindex(columns=todos_os_genes, fill_value=0)

# Salvar matriz
matriz_genes.to_csv("matriz_genes_todas_cepas.csv")
print("Arquivo 'matriz_genes_todas_cepas.csv' gerado com sucesso!")

# =====================
# 4. Gerar Heatmap
# =====================
plt.figure(figsize=(20, 10))
sns.heatmap(matriz_genes, cmap="Reds", cbar_kws={'label': 'Presença (1) / Ausência (0)'}, 
            linewidths=0.5, linecolor="gray")

plt.title("Perfil de Genes de Resistência - Todas as Cepas", fontsize=16)
plt.xlabel("Genes")
plt.ylabel("Cepas")

plt.xticks(ticks=range(len(matriz_genes.columns)), labels=matriz_genes.columns, 
           rotation=90, ha="center", fontsize=8)

plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig("heatmap_genes_todas_cepas.png", dpi=300, bbox_inches="tight")
plt.show()
