from Bio import SeqIO
from parser import parseFASTA

# fasta_sequences = SeqIO.parse(open('./gene.fna'), 'fasta')
# print(type(fasta_sequences))

with open('./gene.fna', 'r') as f:
	pf = parseFASTA(f)

pf.show_sequence_data()
seqs = pf.get_sequences()

# sequence_str = pf.get_sequence('NC_000017.11:c43170327-43044295')
