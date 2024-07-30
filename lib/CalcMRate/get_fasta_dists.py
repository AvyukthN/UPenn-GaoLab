import numpy as np
from tqdm import tqdm

with open('./fasta_data/hg38.fa', 'r') as f:
	lines = f.read().split('\n')
	seqs = []
	curr_seq = []
	for i in tqdm(range(len(lines))):
		if ">" not in lines[i]:
			curr_seq.append(lines[i])
		if ">" in line:
			seqs.append(''.join(curr_seq))
			curr_seq = []

	seqs = np.array(seqs)
	np.save('hg38_sequences.npy', seqs)

with open('./extraction_dir/extracted_exomes.txt', 'r') as f:
	lines = f.read().split('\n')
	seqs = []
	curr_seq = []
	for i in tqdm(range(len(lines))):
		if ">" not in lines[i]:
			curr_seq.append(lines[i])
		if ">" in line:
			seqs.append(''.join(curr_seq))
			curr_seq = []

	seqs = np.array(seqs)
	np.save('exome_sequences.npy', seqs)
