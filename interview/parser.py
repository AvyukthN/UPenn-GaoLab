import re
import numpy as np

class parseFASTA():
	def __init__(self, file_obj):
		self.__file_obj = file_obj
		self.__lines = []
		self.__sequences = []
		self.__parse_meta_data()
		self.__update_sequence_statistics()

	def get_sequences(self):
		return self.__sequences

	def get_sequence(self, identifier: str):
		sequence = ""
		for s in self.__sequences:
			if s['identifier'] == identifier:
				sequence = s['sequence']

		if len(sequence) == 0:
			raise Exception(f"Sequence W/ Identifier {identifier} NOT FOUND")

		return sequence

	def get_nucleotide_count(self, nucleotide: str, sequence: np.ndarray):
		return np.sum((sequence == nucleotide) * 1)

	def get_GC_content(self, sequence: np.ndarray):
		# 
		g_count = self.get_nucleotide_count(nucleotide='G', sequence=sequence)
		c_count = self.get_nucleotide_count(nucleotide='C', sequence=sequence)

		return 100 * ((g_count + c_count) / sequence.shape[0])

	def get_dinucleotide_counts(self, sequence: np.ndarray):
		dn_count_hash = {}

		for i in range(1, len(sequence)):
			dinucleotide = sequence[i-1] + sequence[i] 

			if dinucleotide in dn_count_hash:
				dn_count_hash[dinucleotide] += 1
			else:
				dn_count_hash[dinucleotide] = 1
	
		return dn_count_hash

	def get_reverse_complement(self, sequence: np.ndarray):
		reverse_hash = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

		return ''.join([reverse_hash[sequence[i]] for i in range(len(sequence))])

	def get_protein_sequence(self, sequence: np.ndarray):
		# TRANSCRIPTION
		dna_to_rna = {'A': 'U', 'T': 'A', 'C': 'G', 'G': 'C'}
		rna_seq = np.array([dna_to_rna[sequence[i]] for i in range(len(sequence))])

		# CODON SEPERATION
		codon_hash = {
			'UUU':'Phe','UUC':'Phe','UUA':'Leu','UUG':'Leu','CUU':'Leu',
			'CUC':'Leu','CUA':'Leu','CUG':'Leu','AUU':'Ile','AUC':'Ile',
			'AUA':'Ile','AUG':'Met','GUU':'Val','GUC':'Val','GUA':'Val',
			'GUG':'Val','UCU':'Ser','UCC':'Ser','UCA':'Ser','UCG':'Ser',
			'CCU':'Pro','CCC':'Pro','CCA':'Pro','CCG':'Pro','ACU':'Thr',
			'ACC':'Thr','ACA':'Thr','ACG':'Thr','GCU':'Ala','GCC':'Ala',
			'GCA':'Ala','GCG':'Ala','UAU':'Tyr','UAC':'Tyr','UAA':'STOP',
			'UAG':'STOP','CAU':'His','CAC':'His','CAA':'Gln','CAG':'Gln',
			'AAU':'Asn','AAC':'Asn','AAA':'Lys','AAG':'Lys','GAU':'Asp',
			'GAC':'Asp','GAA':'Glu','GAG':'Glu','UGU':'Cys','UGC':'Cys',
			'UGA':'STOP','UGG':'Trp','CGU':'Arg','CGC':'Arg','CGA':'Arg',
			'CGG':'Arg','AGU':'Ser','AGC':'Ser','AGA':'Arg','AGG':'Arg',
			'GGU':'Gly','GGC':'Gly','GGA':'Gly','GGG':'Gly'
		}
		
		protein_sequence = []
		for i in range(2, len(rna_seq)):
			codon = rna_seq[i-2] + rna_seq[i-1] + rna_seq[i]
			protein_sequence.append(codon_hash[codon])

		return '-'.join(protein_sequence)


	def __update_sequence_statistics(self):
		for i in range(len(self.__sequences)):
			sequence = np.array(list(self.__sequences[i]['sequence']))

			self.__sequences[i]['sequence_length'] = sequence.shape[0]
			self.__sequences[i]['gc_content'] = self.get_GC_content(sequence)
			self.__sequences[i]['a_count'] = self.get_nucleotide_count('A', sequence)
			self.__sequences[i]['t_count'] = self.get_nucleotide_count('T', sequence)
			self.__sequences[i]['g_count'] = self.get_nucleotide_count('G', sequence)
			self.__sequences[i]['c_count'] = self.get_nucleotide_count('C', sequence)
			self.__sequences[i]['dinucleotide_counts'] = self.get_dinucleotide_counts(sequence)
			self.__sequences[i]['reverse_complement_sequence'] = self.get_reverse_complement(sequence)
			self.__sequences[i]['protein_sequence'] = self.get_protein_sequence(sequence)

	def __parse_meta_data(self):
		lines = self.__file_obj.read().split('\n')
		self.__lines = lines

		curr_seq = {}
		count = 1
		for line in lines:
			if len(line) == 0:
				curr_seq["sequence_end"] = count-1
				self.__sequences.append(curr_seq)
				break
			if (line[0] == ">"):
				if curr_seq:
					curr_seq["sequence_end"] = count-1
					self.__sequences.append(curr_seq)
					curr_seq = {}
				pattern = r'\s(?![^\[]*[\]])'
				header_data = re.split(pattern, line)# line.split(' ')
				curr_seq.update({
					"identifier": header_data[0][1:],
					"gene_name": header_data[1],
					"organism": header_data[2].split('=')[1][:-1],
					"gene_id": header_data[3].split('=')[1][:-1],
					"chromosome_number": header_data[4].split('=')[1][:-1],
					"sequence_start": count+1,
					"sequence_end": -1,
					"sequence": ""
				})
			if (count > 1) and (line[0] != ">"):
				curr_seq["sequence"] += line.split(">")[0]

			count += 1

	def show_sequence_data(self):
		final_s = ""
		for s in self.__sequences:
			final_s += f"Sequence Identifier       {s['identifier']}\n"
			final_s += f"Organism                  {s['organism']}\n"
			final_s += f"Gene Name                 {s['gene_name']}\n"
			final_s += f"Gene ID                   {s['gene_id']}\n"
			final_s += f"Chromosome #              {s['chromosome_number']}\n"
			final_s += f"Sequence Length           {s['sequence_length']}\n"
			final_s += f"GC Content                {round(s['gc_content'], 3)}%\n"
			final_s += f"Nucleotide A Count        {s['a_count']}\n"
			final_s += f"Nucleotide T Count        {s['t_count']}\n"
			final_s += f"Nucleotide G Count        {s['g_count']}\n"
			final_s += f"Nucleotide C Count        {s['c_count']}\n\n"

		line_lens = [len(_) for _ in final_s.split('\n')]
		line_lens.sort(reverse=True)
		divider = ("-"*line_lens[0]) + "\n"
		final_s = divider + final_s + divider
		print(final_s)

