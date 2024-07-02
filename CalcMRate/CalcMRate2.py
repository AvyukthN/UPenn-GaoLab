import os
from pathlib import Path
import time
import datetime
from Bio import SeqIO
import numpy as np
from tqdm import tqdm
import re

class CalcMRate:
	def __init__(self, bfile_fp: str, fasta_fp: str, extraction_dir: str, extraction_fname: str, mutational_signature: np.ndarray):
		self.bfile_fp = bfile_fp
		self.fasta_fp = fasta_fp
		self.extraction_dir = extraction_dir
		self.extraction_fname = extraction_fname
		self.mutational_signature = mutational_signature

		self.specific_genome, self.reference_genome = self.process_bed(bfile_fp, fasta_fp, extraction_dir, extraction_fname)

		seqs = [pair[1] for pair in self.specific_genome]

		# counts = [len(re.findall("ACG", seq.upper())) for seq in seqs]
		# counts2 = [len(re.findall("CCG", seq.upper())) for seq in seqs]
		# counts3 = [len(re.findall("GCG", seq.upper())) for seq in seqs]
		# counts4 = [len(re.findall("TCG", seq.upper())) for seq in seqs]
		# final_sum = sum(counts) + sum(counts2) + sum(counts3) + sum(counts4)
		# print("nCG Count " + str(final_sum))

		self.spec_arr = None
		self.ref_arr = None

	def get_specific_ndist(self):
		return self.specific_genome_ndist
	def get_reference_ndist(self):
		return self.reference_genome_ndist

	def get_specific_genome(self):
		return self.specific_genome
	def get_reference_genome(self):
		return self.reference_genome

	def get_spec32(self):
		seqs = [pair[1] for pair in self.specific_genome]

		return self.get_count_vec(seqs, "EXTRACTED SEQUENCES")

	def get_ref32(self):
		return self.get_count_vec([self.reference_genome], "REFERENCE GENOME")


	def get_count_vec(self, sequence_list: list, calc_name: str):
		_, clist, tlist = self.populate_trin()

		clist.sort()
		tlist.sort()

		final_list = clist + tlist
		count_list = [0 for _ in final_list]

		nucleotide_dist = {}

		print(f"GENERATION OF 32-vec DESCRIPTOR | {calc_name}")
		for i in tqdm(range(len(sequence_list))):
			curr_seq = sequence_list[i].upper()

			# rev_comp_seq = self.get_reverse_complement(curr_seq)

			# for codon in final_list:
			# 	num_matches = len(re.findall(codon, curr_seq))

			# 	count_list[final_list.index(codon)] += num_matches

			# for codon in final_list:
			# 	num_matches = len(re.findall(codon, rev_comp_seq))

			# 	count_list[final_list.index(codon)] += num_matches

			try:
				if curr_seq[0] != "N":
					nucleotide_dist[curr_seq[0]] = 1
				if curr_seq[1] != "N":
					if curr_seq[1] not in nucleotide_dist:
						nucleotide_dist[curr_seq[1]] = 1
					else:
						nucleotide_dist[curr_seq[1]] += 1
			except IndexError:
				pass

			for j in range(2, len(curr_seq)):
				codon = curr_seq[j-2] + curr_seq[j-1] + curr_seq[j]

				if codon[-1] in nucleotide_dist:
					nucleotide_dist[codon[-1]] += 1
				else:
					nucleotide_dist[codon[-1]] = 1

				if "N" not in codon:
					reverse_complement = self.get_reverse_complement(codon)
					# print(codon, reverse_complement)
					if codon[1] in ['C', 'T']:
						# if codon in final_list:
						count_list[final_list.index(codon)] += 1
					elif reverse_complement[1] in ['C', 'T']:
						# if reverse_complement in final_list:
						count_list[final_list.index(reverse_complement)] += 1

			# print()	
			# print(final_list)
			# print(count_list)
			# print("-------------------------------------------------------")
			# break
		if calc_name == "REFERENCE GENOME":
			self.reference_genome_ndist = nucleotide_dist
		if calc_name == "EXTRACTED SEQUENCES":
			self.specific_genome_ndist = nucleotide_dist

		return final_list, count_list



	def get_reverse_complement(self, seq: str):
		comp_hash = {
			"A": "T",
			"C": "G",
			"G": "C",
			"T": "A"
		}

		new_seq = ""
		for n in seq[::-1]:
			new_seq += comp_hash[n]

		return new_seq

	"""
	Creates a hashmap to track counts of all possible _C_ and _T_ nucleotides
	Did it by treating each nucleotide as a digit in base 4 (later realized this was extremely over engineered)
		- since a nested for loop will also run in constant time smh
	"""
	def populate_trin(self):
		nuc_hash = {
			0: "A",
			1: "C",
			2: "G",
			3: "T"
		}

		trinhash = {}
		C_list = []
		T_list = []
		for i in range(4**2):
			C_string = f"{nuc_hash[i // 4]}C{nuc_hash[i % 4]}"
			T_string = f"{nuc_hash[i // 4]}T{nuc_hash[i % 4]}"
			trinhash.update({C_string: 0})
			trinhash.update({T_string: 0})
			C_list.append(C_string)
			T_list.append(T_string)

		return trinhash, C_list, T_list

	def process_bed(self, bfile_fp: str, fasta_fp: str, extraction_dir: str, extraction_fname: str):
		### ERROR HANDLING - File I/O
		bfile = Path(bfile_fp)
		fasta_file = Path(fasta_fp)
		ex_dir = Path(extraction_dir)

		if not bfile.is_file():
			raise Exception(f"INPUT BED FILE @ {bfile_fp} NOT FOUND | Please provide a valid file path")
		if not fasta_file.is_file():
			raise Exception(f"INPUT FASTA FILE @ {fasta_fp} | NOT FOUND | Please provide a valid file path")
		if not ex_dir.is_dir():
			raise Exception(f"EXTRACTION DIRECTORY {extraction_dir} | NOT FOUND | Please provide a valid extraction directory")
		if "." in extraction_fname:
			# if extraction_fname.split('.')[1] != "txt":
				# raise Exception(F"EXTRACTION FILE {extraction_fname} MUST BE A .txt FILE")
			raise Exception(F"EXTRACTION FILE {extraction_fname} MUST NOT HAVE A FILE EXTENSION")
		###

		# bedtools command to extract specific sequences from reference genome
		os.system(f'bedtools getfasta -fi {fasta_fp} -bed {bfile_fp} -fo {extraction_dir}/{extraction_fname}.txt')

		extracted_sequence = self.process_bedout(f"{extraction_dir}/{extraction_fname}.txt")
		genome_sequence = self.process_fasta(fasta_fp)

		return extracted_sequence, genome_sequence

	def process_fasta(self, fasta_fp: str):
		sequence = []
		for record in SeqIO.parse(fasta_fp, "fasta"):
			sequence.append(str(record.seq))
		
		return ''.join(sequence)

	# gets sequences after bed file extraction is performed on the reference genome
	def process_bedout(self, extraction_fp: str):
		with open(extraction_fp, 'r') as f:
			lines = f.read().split('\n')

		extracted_arr = []
		for i in range(1, len(lines), 2):
			extracted_arr.append([lines[i-1], lines[i]])
		
		return np.array(extracted_arr)

'''
if __name__ == '__main__':
	args = sys.
'''
