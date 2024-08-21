import pandas as pd
# from topCatCounter import topCatCounter
import matplotlib.pyplot as plt
import numpy as np

def getFunctionalBiotypes(filepath: str):
    with open(filepath, "r") as f:
        fbiotypes = f.read().split("\n")
        return {bt: 1 for bt in fbiotypes}

def getRankHash(filepath: str):
    with open(filepath, "r") as f:
        lines = f.read().split("\n")[:-1]
        rank_hash = {term.split(" ")[0]: int(term.split(" ")[1]) for term in lines}

    return rank_hash

def getRank(consequence_term: str, rank_hash: dict):
    if consequence_term in rank_hash:
        return rank_hash[consequence_term]
    else:
        return min(list(map(lambda x: rank_hash[x], consequence_term.split(","))))

def filterGeneOfInterest(df: pd.DataFrame, gene_name: str):
    return df[df["SYMBOL"] == gene_name]

def filterCanonicalTranscripts(df: pd.DataFrame):
    return df[df["CANONICAL"] == "YES"]

def filterFunctionalBiotypes(df: pd.DataFrame, filepath="../data/classification_data/functional_biotypes.txt"):
    biotypes = list(df["BIOTYPE"])
    functional_biotypes = getFunctionalBiotypes(filepath)

    checked_biotypes = map(lambda x: x in functional_biotypes, biotypes)
    checked_biotypes = list(map(int, checked_biotypes))

    df.insert(0, "biotype_functional_check", checked_biotypes)

    df = df[df["biotype_functional_check"] == 1]
    return df

def filterTopConsequences(df: pd.DataFrame):
    consequences = list(df["Consequence"])

    rank_hash = getRankHash("../data/classification_data/consequence_terms.txt")
    consequence_ranks = list(map(lambda x: getRank(x, rank_hash), consequences))
    top_category = min(consequence_ranks)

    print(f"TOP CATEGORY | {top_category}")

    df.insert(0, "consequence_rank", consequence_ranks)

    df = df[df["consequence_rank"] == top_category]

    return df

if __name__ == '__main__':
    df = pd.read_csv("./BRCA2_annotated.tsv", sep="\t")
    df = filterFunctionalBiotypes(df)
    df = filterTopConsequences(df)
    df.to_csv("checkout.tsv", sep="\t")
    out = topCatCounter(df, "../data/BRCA_Exon_Regions.fa")

    trinlist, counts = out
    f, ax = plt.subplots(figsize=(32,5)) # set the size that you'd like (width, height)
    plt.bar(trinlist[:16], counts[:16])
    plt.bar(trinlist[16:], counts[16:])
    plt.xlabel('Trinucleotides')
    plt.ylabel('Frequency')
    ax.legend(["C Trinucleotide Frequencies", "T Trinucleotide Frequencies"], fontsize = 14)
    plt.show()

    
