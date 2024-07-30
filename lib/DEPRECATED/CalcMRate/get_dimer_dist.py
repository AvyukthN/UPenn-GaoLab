import numpy as np
from tqdm import tqdm
import multiprocessing as mp
from collections import Counter

def process_sequence(seq):
    dimer_counts = Counter()
    for i in range(1, len(seq)):
        dimer = seq[i-1] + seq[i]
        dimer.upper()

        if "N" not in dimer:
            dimer_counts[dimer] += 1
    return dimer_counts

def process_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().split('\n')
    
    seqs = []
    curr_seq = []
    total_length = 0
    for line in lines:
        if ">" not in line:
            curr_seq.append(line.upper())
        elif ">" in line:
            cseq = ''.join(curr_seq)
            cseq.upper()
            seqs.append(cseq)
            total_length += len(cseq)
            curr_seq = []
    
    if curr_seq:
        seqs.append(''.join(curr_seq))
        total_length += len(''.join(curr_seq))

    '''
    fseq = ''.join(seqs)
    print()
    print("UNKOWN NUCLEOTIDE DIST")
    print(round(fseq.count("N")/len(fseq), 3))
    print()
    '''
    
    with mp.Pool() as pool:
        results = list(tqdm(pool.imap(process_sequence, seqs), total=len(seqs)))
    
    dimer_dist = Counter()
    for result in results:
        dimer_dist.update(result)
    
    return dict(dimer_dist), total_length

if __name__ == '__main__':
    print("Processing reference genome...")
    ref_dimer_dist, total_length = process_file('./fasta_data/hg38.fa')
    for key in ref_dimer_dist:
        ref_dimer_dist[key] /= total_length
    print(ref_dimer_dist)
    print()

    print("Processing specific exomes...")
    spec_dimer_dist, total_length = process_file('./extraction_dir/extracted_exomes.txt')
    for key in spec_dimer_dist:
        spec_dimer_dist[key] /= total_length
    print(spec_dimer_dist)
