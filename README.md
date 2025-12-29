# Montagem-h-brida-de-Genomas-bacterianos-Illumina-Nanopore-

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
