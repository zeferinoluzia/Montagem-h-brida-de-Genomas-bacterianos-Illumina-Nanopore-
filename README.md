# Montagem-hibrida-de-Genomas-bacterianos-Illumina-Nanopore-

Pipeline completo e reprodutível para montagem híbrida de genomas bacterianos
utilizando **short reads (Illumina)** e **long reads (Oxford Nanopore)**,
incluindo avaliação de qualidade, scaffolding, resistência antimicrobiana,
tipagem molecular e análises comparativas.

Este repositório documenta integralmente o fluxo utilizado no projeto
**REVIRAE – Fiocruz Ceará**.

---

## 🎯 Objetivo

Validar o uso de montadores híbridos para obtenção de genomas completos de
isolados bacterianos do projeto REVIRAE, comparando montagens baseadas em
short reads, long reads e abordagem híbrida.

---

## 🧬 Workflow Geral

1. Controle de qualidade das reads
2. Montagem híbrida com Unicycler
3. Avaliação das montagens (QUAST, BUSCO)
4. Scaffolding com Medusa
5. Qualidade genômica (CheckM)
6. Desreplicação (dRep)
7. Análise de resistência antimicrobiana (Abricate)
8. Tipagem molecular (MLST)

---

## 📁 Estrutura do Repositório

```text
hybrid-genome-assembly-revirae/
├── data/
├── qc/
├── assembly/
├── evaluation/
├── scaffolding/
├── amr/
├── typing/
├── figures/
├── docs/
└── README.md
```

## 1️⃣ Controle de Qualidade das Reads
Short reads (Illumina) – FastQC

```bash
fastqc illumina_goods/*
```

As reads apresentaram bom padrão de qualidade, não sendo necessário trimming.

Long reads (Nanopore) – MinIONQC

```bash
Rscript MinIONQC.R \
  --input ~/WGS/data/nanopore_goods/ \
  --outputdirectory output_nanopore \
  --processors 2
```
## 2️⃣ Preparação dos Arquivos Illumina

Padronização dos nomes das reads para compatibilidade com o Unicycler:

```bash
for file in *.fastq.gz; do
  base=$(echo "$file" | cut -d'-' -f1)
  read=$(echo "$file" | grep -o '_R[12]_')
  new="${base}${read%.}_001.fastq.gz"
  mv "$file" "$new"
done
```
## 3️⃣ Montagem Híbrida – Unicycler
Ativação do ambiente:
```bash
conda activate assembly
```
Execução manual (exemplo)
```bash
unicycler \
 -1 illumina_f.fq \
 -2 illumina_r.fq \
 -l minion_2d.fq \
 -t 8 \
 -o unicycler_result
```

Script automatizado para múltiplas amostras
```bash
#!/bin/bash

ILLUMINA_DIR=~/WGS/data/illumina_goods
NANOPORE_DIR=~/WGS/data/nanopore_goods
OUTDIR=~/WGS/unicycler/results
THREADS=8

mkdir -p "$OUTDIR"

for nanopore_file in "$NANOPORE_DIR"/*.fastq; do
    sample=$(basename "$nanopore_file" .fastq)

    r1="$ILLUMINA_DIR/${sample}_R1__001.fastq.gz"
    r2="$ILLUMINA_DIR/${sample}_R2__001.fastq.gz"

    if [[ -f "$r1" && -f "$r2" && -f "$nanopore_file" ]]; then
        echo "Rodando Unicycler para $sample"
        unicycler -1 "$r1" -2 "$r2" -l "$nanopore_file" \
        -o "$OUTDIR/$sample" -t "$THREADS"
        echo "Finalizado: $sample"
    else
        echo "Arquivos faltando para $sample"
    fi
done
```

Execução:

```bash
./run_unicycler_all.sh
```
Exemplos individuais
```bash
unicycler -1 ~/WGS/data/illumina_goods/KP_0588_R1__001.fastq.gz \
 -2 ~/WGS/data/illumina_goods/KP_0588_R2__001.fastq.gz \
 -l ~/WGS/data/nanopore_goods/KP_0588.fastq \
 -t 12 -o results2/KP_0588
```

## 4️⃣ Avaliação da Montagem
QUAST
```bash
quast montagem.fasta -R ref.fasta -o quast_comparacao
```

BUSCO
Listar datasets:

```bash
busco --list-datasets
```

Execução:

```bash
busco -m genome \
 -i ../assemble_fasta/kp_588.long.fasta \
 -l enterobacteriaceae_odb12 \
 -o long_results_588
```

Plot comparativo:

```bash
busco --plot plots/
```

## 5️⃣ Scaffolding – Medusa

```bash
conda activate medusa_env

java -jar ~/WGS/medusa/medusa.jar \
 -f ~/WGS/medusa_refs \
 -i ~/WGS/assemble_fasta/644_kp/kp_644.hib.fasta \
 -v
```

## 6️⃣ Qualidade Genômica – CheckM

Preparação:

```bash
mkdir -p ~/WGS/checkM/tmp_588_kp
cp ../assemble_fasta/588_kp/scafold_medusa/kp_588.hib.medusa.fasta \
~/WGS/checkM/tmp_588_kp/
```

Execução:

```bash
checkm lineage_wf ~/WGS/checkM/tmp_588_kp \
~/WGS/checkM/results/588_kp -x fasta
```

Todos os genomas:

```bash
cp ../assemble_fasta/*/scafold_medusa/*.fasta tmp_all/
checkm lineage_wf tmp_all results/all -x fasta
```

GC plot:

```bash
checkm gc_plot ../assemble_fasta/588_kp/scafold_medusa/ \
results/588_kp/gc_plot 100 -x fasta --image_type png --dpi 300
```

QA:

```bash
checkm qa results/all/lineage.ms results/all/ > qa_all.txt
```

## 7️⃣ Desreplicação – dRep

Arquivo genomeInfo.csv:

genome,completeness,contamination
~/WGS/checkM/tmp_all/kp_692.long.medusa.fasta,100.00,1.71
~/WGS/checkM/tmp_all/kp_692.hib.medusa.fasta,100.00,1.71


Execução:

```bash
dRep dereplicate drep_out \
 -g ~/WGS/checkM/tmp_all/*.fasta \
 -p 8 \
 --genomeInfo genomeInfo.csv \
 --S_algorithm fastANI \
 -comp 70 -con 5
```

## 8️⃣ Resistência Antimicrobiana – Abricate

```bash
conda activate AMR
abricate --list
```

Execução:

```bash
abricate kp_692.long.medusa.fasta --db ncbi --csv > kp_692_long.csv
```

Script para Heatmap AMR:

```python 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os

arquivos = glob.glob("kp_*/*.csv")
dfs = []

for arquivo in arquivos:
    cepa = os.path.basename(os.path.dirname(arquivo))
    df = pd.read_csv(arquivo)
    df.columns = df.columns.str.strip()
    df["CEPA"] = cepa
    dfs.append(df[["CEPA", "GENE"]])

df_genes = pd.concat(dfs, ignore_index=True)

matriz = (df_genes.assign(presente=1)
          .pivot_table(index="CEPA", columns="GENE",
                       values="presente", fill_value=0))

matriz.to_csv("matriz_genes_todas_cepas.csv")

plt.figure(figsize=(20,10))
sns.heatmap(matriz, cmap="Reds")
plt.savefig("heatmap_genes_todas_cepas.png", dpi=300)
plt.show()
```

## 9️⃣ MLST

```bash
conda activate mlst-env
mlst ../assemble_fasta/*/scafold_medusa/*.fasta > mlst_all.txt
```

## 🧠 Observações Importantes

Montagens híbridas apresentaram maior fragmentação em alguns isolados

Montagens long-read apresentaram melhor alinhamento no BRIG

BUSCO indicou maior completude para montagens long-read
