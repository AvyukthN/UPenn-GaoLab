import os

def runMutator(fasta_fp: str, out_vcf_fp: str):
    os.system(f"./synthetic_mutation_pipeline/insilico_mutator {fasta_fp} {out_vcf_fp}")
