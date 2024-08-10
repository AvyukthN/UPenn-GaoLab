import pandas as pd
import os

def getRowMatch(matcher: str, term: str, df: pd.DataFrame):
    return df.loc[df[matcher] == term]

def stripVersion(name: str):
    return name.split('.')[0]

def geneNameToEnsemblID(gene_name: str):
    gencode = pd.read_csv("../data/GENCODE_v46_hg38.tsv", sep="\t")
    glookup = pd.read_csv("../data/gene_lookup.tsv", sep="\t")

    return getRowMatch("Gene name", gene_name, glookup)["Transcript stable ID"].iloc[0]

def makeBedFile(gene_name: str, bed_filepath: str):
    gencode = pd.read_csv("../data/GENCODE_v46_hg38.tsv", sep="\t")
    glookup = pd.read_csv("../data/gene_lookup.tsv", sep="\t")

    names = list(gencode["#name"])
    new_names = list(map(stripVersion, names))
    gencode["#name"] = new_names

    tid = getRowMatch("Ensembl Canonical", 1, getRowMatch("Gene name", gene_name, glookup))["Transcript stable ID"].iloc[0]
    print(tid)
    gencode_match = getRowMatch("#name", tid, gencode)

    exon_starts = gencode_match["exonStarts"].iloc[0].split(",")
    exon_ends = gencode_match["exonEnds"].iloc[0].split(",")
    chrom = gencode_match["chrom"].iloc[0]
    name = gencode_match["#name"].iloc[0]

    with open(bed_filepath, "w") as f:
        for estart, eend in list(zip(exon_starts, exon_ends)):
            f.write(f"{chrom}\t{estart}\t{eend}\t{name}\n")

