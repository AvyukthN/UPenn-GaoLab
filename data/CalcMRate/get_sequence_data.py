import numpy as np
from tqdm import tqdm

ref_dimer_dist = {}
with open('./fasta_data/hg38.fa', 'r') as f:
	lines = f.read().split('\n')
	seqs = []
	curr_seq = []
	for i in tqdm(range(len(lines))):
		if ">" not in lines[i]:
			curr_seq.append(lines[i])
		if ">" in lines[i]:
			seqs.append(''.join(curr_seq))
			curr_seq = []
			for i in range(1, len(seqs[-1])):
				dimer = seqs[-1][i-1] + seqs[-1][i]
				if dimer in ref_dimer_dist:
					ref_dimer_dist[dimer] += 1
				else:
					ref_dimer_dist[dimer] = 1

	# seqs = np.array(seqs)
	# np.save('hg38_sequences.npy', seqs)

print(ref_dimer_dist)
print()

spec_dimer_dist = {}
with open('./extraction_dir/extracted_exomes.txt', 'r') as f:
	lines = f.read().split('\n')
	seqs = []
	curr_seq = []
	for i in tqdm(range(len(lines))):
		if ">" not in lines[i]:
			curr_seq.append(lines[i])
		if ">" in lines[i]:
			seqs.append(''.join(curr_seq))
			curr_seq = []
			for i in range(1, len(seqs[-1])):
				dimer = seqs[-1][i-1] + seqs[-1][i]
				if dimer in spec_dimer_dist:
					spec_dimer_dist[dimer] += 1
				else:
					spec_dimer_dist[dimer] = 1

	# seqs = np.array(seqs)
	# np.save('exome_sequences.npy', seqs)

print(spec_dimer_dist)
