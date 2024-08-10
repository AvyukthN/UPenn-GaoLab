import os

def getFastaFromBED(fasta_fp: str, bed_fp: str, out_fp: str):
    os.system(f"bedtools getfasta -fi {fasta_fp} -bed {bed_fp} -fo {out_fp}")
