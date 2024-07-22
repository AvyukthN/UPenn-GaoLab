import json
from functools import cmp_to_key

def compare_consequences(a, b, consequence_values):
    a_value = consequence_values.get(a['consequence_terms'], -1)# float('inf'))
    b_value = consequence_values.get(b['consequence_terms'], -1)# float('inf'))
    return a_value - b_value

def transformer(fp: str):
	with open(fp, 'r') as f:
		data = json.load(f)

	functional_biotypes = "protein_coding IG_C_gene IG_D_gene IG_J_gene IG_V_gene TR_C_gene TR_D_gene TR_J_gene TR_V_gene lncRNA ncRNA".split(" ")
	nonfunctional_biotypes = "pseudogene processed_pseudogene unprocessed_pseudogene transcribed_pseudogene nonsense_mediated_decay TEC"

	transformed_data = []
	for extract in data:
		curr_id = extract["id"]
		curr_hash = {}
		transformed_consequence_dict = {}
		for key in extract:
			if key != "transcript_consequences":
				transformed_consequence_dict[key] = extract[key]

		inter = []
		for consequence in extract["transcript_consequences"]:
			if "canonical" in consequence.keys():
				if consequence["biotype"] in functional_biotypes:
					# rank consequence terms
					inter.append(consequence)		
					

		if len(inter) == 0:
			inter.append(extract["transcript_consequences"][random.randint(0, len(extract["transcript_consequences"]) - 1)])

		for i in range(len(inter)):
			inter[i]["consequence_terms"] = inter[i]["consequence_terms"][0]

		# Define the arbitrary values for consequence terms
		
		consequence_values = {}
		truncation = "transcript_ablation frame_shift start_lost stop_gained stop_lost feature_elongation feature_truncation"
		missense = "inframe_insertion inframe_deletion missense_variant protein_altering_variant incomplete_terminal_codon_variant coding_sequence_variant"
		splice = "splice_acceptor_variant splice_donor_variant splice_donor_5th_base_variant splice_region_variant splice_donor_region_variant splice_polypyrimidine_tract_variant"
		regulatory = "NMD_transcript_variant 5_prime_UTR_variant 3_prime_UTR_variant transcript_amplification non_coding_transcript_exon_variant intron_variant non_coding_transcript_variant"
		lowest = "start_retained_variant stop_retained_variant synonymous_variant"

		for _ in truncation.split(" "):
			consequence_values[_] = 5
		for _ in missense.split(" "):
			consequence_values[_] = 4
		for _ in splice.split(" "):
			consequence_values[_] = 3
		for _ in regulatory.split(" "):
			consequence_values[_] = 2
		for _ in lowest.split(" "):
			consequence_values[_] = 1

		# sorted_list = sorted(inter, key=cmp_to_key(compare_consequences))
		sorted_list = sorted(inter, key=cmp_to_key(lambda x, y: compare_consequences(x, y, consequence_values)))

		transformed_consequence_dict["consequence_terms"] = sorted_list[-1]
		transformed_data.append(transformed_consequence_dict)

	return transformed_data

if __name__ == '__main__':
	fp = "./extracted_consequences/canonical_demo/VEP_canonical_data.json"

	tdata = transformer(fp)
	with open(fp, 'w') as f:
		json.dump(tdata, f, indent=4)
