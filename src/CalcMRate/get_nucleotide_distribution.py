from Bio import SeqIO

ref_nucleotide_dist = {
	"A": 0,
	"C": 0,
	"G": 0,
	"T": 0
}
ref_dimer_dist = {}

ref_length = 0
for seq_record in SeqIO.parse("./fasta_data/hg38.fa", "fasta"):
	seq = (seq_record.seq)

	a_count  = seq.count('A')
	c_count  = seq.count('C')
	g_count  = seq.count('G')
	t_count  = seq.count('T')

	ref_length += len(seq) # (a_count + c_count + g_count + t_count)

	ref_nucleotide_dist['A'] += a_count
	ref_nucleotide_dist['C'] += c_count
	ref_nucleotide_dist['G'] += g_count
	ref_nucleotide_dist['T'] += t_count

	for i in range(1, len(seq)):
		dimer = seq[i-1] + seq[i]	
		if "N" not in dimer:
			if dimer in ref_dimer_dist:
				ref_dimer_dist[dimer] += 1
			else:
				ref_dimer_dist[dimer] = 1

spec_nucleotide_dist = {
	"A": 0,
	"C": 0,
	"G": 0,
	"T": 0
}
spec_dimer_dist = {}

spec_length = 0
for seq_record in SeqIO.parse("./extraction_dir/extracted_exomes.fa", "fasta"):
	seq = (seq_record.seq)

	a_count  = seq.count('A')
	c_count  = seq.count('C')
	g_count  = seq.count('G')
	t_count  = seq.count('T')

	spec_length += len(seq) # (a_count + c_count + g_count + t_count)

	spec_nucleotide_dist['A'] += a_count
	spec_nucleotide_dist['C'] += c_count
	spec_nucleotide_dist['G'] += g_count
	spec_nucleotide_dist['T'] += t_count

	for i in range(1, len(seq)):
		dimer = seq[i-1] + seq[i]	
		if "N" not in dimer:
			if dimer in spec_dimer_dist:
				spec_dimer_dist[dimer] += 1
			else:
				spec_dimer_dist[dimer] = 1

ref_nucleotide_dist['A'] /= ref_length
ref_nucleotide_dist['C'] /= ref_length
ref_nucleotide_dist['G'] /= ref_length
ref_nucleotide_dist['T'] /= ref_length

spec_nucleotide_dist['A'] /= spec_length
spec_nucleotide_dist['C'] /= spec_length
spec_nucleotide_dist['G'] /= spec_length
spec_nucleotide_dist['T'] /= spec_length

print(ref_nucleotide_dist)
print()
print(spec_nucleotide_dist)

print()
print(ref_length)
print()
print(spec_length)
print()

print(ref_dimer_dist)
print(spec_dimer_dist)
