#!/usr/bin/env python3
import re
import pandas as pd

# Arquivo de entrada
input_file = "mlst_all.txt"

# Genes de interesse
genes = ["gapA", "infB", "mdh", "pgi", "phoE", "rpoB", "tonB"]

# Dicionário para armazenar os dados
data = {}

with open(input_file, "r") as f:
    for line in f:
        # Pular linhas vazias
        if not line.strip():
            continue
        
        # Extrair nome da amostra (ex.: kp_588)
        match_sample = re.search(r"/(\d+_kp)/", line)
        if not match_sample:
            continue
        sample = "kp_" + match_sample.group(1).replace("_kp", "")
        
        # Extrair os valores dos genes
        values = {}
        for gene in genes:
            match_gene = re.search(rf"{gene}\(([\d~?]+)\)", line)
            if match_gene:
                # Remove caracteres não numéricos (~ e ?)
                val = re.sub(r"[^\d]", "", match_gene.group(1))
                values[gene] = int(val) if val.isdigit() else None
        
        # Salvar (se já existe, não sobrescreve)
        if sample not in data:
            data[sample] = values

# Converter para DataFrame
df = pd.DataFrame.from_dict(data, orient="index")
df.index.name = "Sample"
df.reset_index(inplace=True)

# Mostrar estrutura semelhante à que você pediu
print("data = {")
print('    "Sample":', df["Sample"].tolist(), ",")
for gene in genes:
    print(f'    "{gene}": {df[gene].tolist()},')
print("}")

# Gerar heatmap
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.heatmap(df.set_index("Sample")[genes], cmap="coolwarm", annot=True)
plt.title("MLST Allele Numbers per Sample")
plt.tight_layout()
plt.savefig("heatmap_mlst.png", dpi=300)
plt.show()
