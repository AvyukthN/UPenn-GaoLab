from StrategyInterfaces import ExtractStrategy, TransformStrategy, LoadStrategy
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import os
import numpy as np
from helper_functions.geneNameSearch import geneNameToEnsemblID
from helper_functions.geneNameSearch import makeBedFile 
from helper_functions.runMutator import runMutator
from helper_functions.bedtoolWrapper import getFastaFromBED
from helper_functions.filterTranscripts import filterGeneOfInterest
from helper_functions.filterTranscripts import filterFunctionalBiotypes
from helper_functions.filterTranscripts import filterTopConsequences
from helper_functions.filterTranscripts import filterCanonicalTranscripts
from helper_functions.topCatCounter import topCatCounter
import matplotlib.pyplot as plt
import time

class CSVExtractStrategy(ExtractStrategy):
    def extract(self, source):
        # CSV EXTRACTION LOGIC
        # takes in csv of gene names and COSMIC sig.s and returns list of them for transform strategies
        df = pd.read_csv(source)
        gene_names = list(df[df.columns[0]])
        ensembl_ids = list(map(geneNameToEnsemblID, gene_names))

        df.insert(0, "EnsembleID", ensembl_ids, True)

        return df

class TSVExtractStrategy(ExtractStrategy):
    def extract(self, source):
        # TSV EXTRACTION LOGIC
        # takes in tsv of gene names and COSMIC sig.'s and returns list of them for transform strategies
        df = pd.read_csv(source, sep='\t')
        gene_names = list(df[df.columns[0]])
        ensembl_ids = list(map(geneNameToEnsemblID, gene_names))

        df.insert(0, "EnsembleID", ensembl_ids, True)

        return df

class UniversalTransformStrategy(TransformStrategy):
    def transform(self, extracted_data):
        # take in list of gene names & COSMIC sig.'s
        # transform into list of lists
        # [[*gene_name*, *COSMIC sig.*, *Susceptibility Score*, ...], ...]
        ensembl_tids = list(extracted_data[extracted_data.columns[0]])
        gene_names = list(extracted_data[extracted_data.columns[1]])
        mutsigs = list(map(self.siginToArray,list(extracted_data[extracted_data.columns[2]])[1:]))

        joined_datetime = "-".join(str(datetime.now()).split(" "))
        extract_folder = f"../data/extracts/{joined_datetime}_extract/"
        self.extract_folder = extract_folder

        os.mkdir(extract_folder)
        os.mkdir(f"{extract_folder}geneBEDs/")
        os.mkdir(f"{extract_folder}geneFASTAs/")
        os.mkdir(f"{extract_folder}geneVCFs/")
        os.mkdir(f"{extract_folder}geneFigures/")
        os.mkdir(f"{extract_folder}geneTrimerVecs/")
        os.mkdir(f"{extract_folder}finalTranscripts/")
        os.mkdir(f"{extract_folder}curatedTranscripts/")
        os.mkdir(f"{extract_folder}originalTranscripts/")

        for i in tqdm(range(len(gene_names))):
            name = gene_names[i]
            bedfile_fp = f"{extract_folder}geneBEDs/{name}.bed"
            fasta_fp = f"{extract_folder}geneFASTAs/{name}.fa"
            vcf_fp = f"{extract_folder}geneVCFs/{name}.vcf"

            makeBedFile(name, bedfile_fp)
            getFastaFromBED("../data/fasta_data/hg38.fa", bedfile_fp, fasta_fp)
            runMutator(fasta_fp, vcf_fp)

            ##########################################################
            #             CODE BLOCK FOR VEP ANNOTATION             #
            ##########################################################

            vep_results_fname = f"../data/VEP_annotations/{name}.tsv"

            df = pd.read_csv(vep_results_fname, sep="\t")
            self.dataSaver(f"originalTranscripts/{name}_filter=NONE.tsv", df)
            df = filterGeneOfInterest(df, name)
            df = filterCanonicalTranscripts(df)
            df = filterFunctionalBiotypes(df)
            self.dataSaver(f"curatedTranscripts/{name}_filter=biotype,canonical,GOI.tsv", df)
            df = filterTopConsequences(df)
            self.dataSaver(f"finalTranscripts/{name}_filter=ALL.tsv", df)

            out = topCatCounter(df, fasta_fp)

            trinlist, counts = out
            f, ax = plt.subplots(figsize=(32,5)) # set the size that you'd like (width, height)
            plt.bar(trinlist[:16], counts[:16])
            plt.bar(trinlist[16:], counts[16:])
            plt.xlabel('Trinucleotides')
            plt.ylabel('Frequency')
            ax.legend(["C Trinucleotide Frequencies", "T Trinucleotide Frequencies"], fontsize = 14)
            self.dataSaver(f"geneFigures/{name}_TopCategory_Trimer_Frequency.png", plt)
            self.dataSaver(f"geneTrimerVecs/{name}_TopCategory_Trimer_Frequency_Vec.npy", counts)

    def dataSaver(self, filename: str, data):
        filepath = f"{self.extract_folder}{filename}"
        match filename.split(".")[-1]:
            case "tsv":
                data.to_csv(filepath, sep="\t")
            case "txt":
                with open(filepath, "r") as f:
                    f.write(data)
            case "png":
                data.savefig(filepath)
            case "npy":
                np.save(filepath, data)
            case _:
                raise Exception(f"Unsupported File Type for \"{filename}\"")

    def siginToArray(self, mutsig: str):
        return list(map(float, mutsig.split(" ")))

class CSVLoadStrategy(LoadStrategy):
    def load(self, transformed_data, destination):
        # takes in output list of lists defined in Universal Transform Strategy and saves in CSV format at destination filepath
        print("LOADING CSV")

class TSVLoadStrategy(LoadStrategy):
    def load(self, transformed_data, destination):
        # takes in output list of lists defined in Universal Transform Strategy and saves in TSV format at destination filepath
        print("LOADING TSV")
