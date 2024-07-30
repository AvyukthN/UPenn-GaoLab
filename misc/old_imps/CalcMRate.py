import os
from pathlib import Path
import time
import datetime
from Bio import SeqIO
import numpy as np
from tqdm import tqdm

class CalcMRate:
	def __init__(self, bfile_fp: str, fasta_fp: str, extraction_dir: str, extraction_fname: str, mutational_signature: np.ndarray):
		self.bfile_fp = bfile_fp
		self.fasta_fp = fasta_fp 
		self.extraction_dir = extraction_dir 
		self.extraction_fname = extraction_fname 
		self.mutational_signature = mutational_signature

		self.specific_genome, self.reference_genome = self.process_bed(bfile_fp, fasta_fp, extraction_dir, extraction_fname)
	
		'''	
		print("GETTING SPEC GENOME 32 VECTOR")
		self.spec_vector = self.get_spec_vector(self.specific_genome, self.populate_trin()[0])
		print("GETTING REFERENCE GENOME 32 VECTOR")
		self.ref_vector = self.get_ref_vector(self.reference_genome, self.populate_trin()[0])

		ref_filename = fasta_fp.split("/")[-1].split('.')[0]

		ref_names, ref_counts = self.sorter(self.ref_vector.keys(), self.ref_vector.values())
		spec_names, spec_counts = self.sorter(self.spec_vector.keys(), self.spec_vector.values())
		
		np.save(f"{ref_filename}-32vec.npy", ref_counts)
		np.save(f"{extraction_fname}-32vec.npy", spec_counts)

		self.proportion_vec = np.divide(np.array(spec_counts), np.array(ref_counts))

		self.proportion_vec_96 = np.repeat(self.proportion_vec, 3)

		self.derived_mutational_signature = np.multiply(self.mutational_signature, self.proportion_vec_96)
		np.save(f"derived_mutational_signature.npy", self.derived_mutational_signature)
		'''

	def get_ref_32vec(self):
		print("GETTING REFERENCE GENOME 32 VECTOR")
		return self.get_ref_vector(self.reference_genome, self.populate_trin()[0])
	def get_spec_32vec(self):
		print("GETTING SPEC GENOME 32 VECTOR")
		self.spec_vector = self.get_spec_vector(self.specific_genome, self.populate_trin()[0])

	def sorter(self, tosort: list, toarrange: list):
		list1, list2 = zip(*sorted(zip(tosort, toarrange)))

		return list1, list2

	def get_ref_vector(self, ref_seq: str, trinhash: dict):
		ref_filename = self.fasta_fp.split("/")[-1].split('.')[0]
		if f"{ref_filename}.npy" in os.listdir('./'):
			return np.load(f"{ref_filename}.npy")
		return self.get_count_hash(ref_seq, trinhash, True)

	def get_spec_vector(self, spec_seqs: list, trinhash: dict):
		if self.extraction_fname + ".npy" in os.listdir('/'):
			return np.load(f"{self.extraction_fname}.npy")
		for i in tqdm(range(len(spec_seqs))):
			trinhash = self.get_count_hash(spec_seqs[i], trinhash, False)

		return trinhash

	def get_count_hash(self, sequence: str, trinhash: dict, ref: bool):
		if ref:
			for i in tqdm(range(2, len(sequence))):
				codon = (sequence[i-2] + sequence[i-1] + sequence[i]).upper()

				if "N" in codon:
					continue

				complement = self.get_complement(codon)
				if codon in trinhash:
					trinhash[codon] += 1
				if complement in trinhash:
					trinhash[complement] += 1
		if not ref:
			for i in range(2, len(sequence)):
				codon = (sequence[i-2] + sequence[i-1] + sequence[i]).upper()

				if "N" in codon:
					continue

				complement = self.get_complement(codon)
				if codon in trinhash:
					trinhash[codon] += 1
				if complement in trinhash:
					trinhash[complement] += 1

		return trinhash

	def get_complement(self, seq: str):
		comp_hash = {
			"A": "T",
			"C": "G",
			"G": "C",
			"T": "A"
		}

		new_seq = ""	
		for n in seq:
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
		trinlist = []
		for i in range(4**2):
			C_string = f"{nuc_hash[i // 4]}C{nuc_hash[i % 4]}"
			T_string = f"{nuc_hash[i // 4]}T{nuc_hash[i % 4]}"
			trinhash.update({C_string: 0})
			trinhash.update({T_string: 0})
			trinlist.append(C_string)
			trinlist.append(T_string)

		return trinhash, trinlist

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
