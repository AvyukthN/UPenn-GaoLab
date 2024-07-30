import json
import pandas as pd
import os
import pprint
import requests, sys

def get_transcript_sequence(transcript_id: str): 
	server = "https://rest.ensembl.org"
	# gene_id = "ENSG00000169174"
	# transcript_id = "ENST00000710286"
	# ext = f"/sequence/id/{gene_id}?" 
	ext = f"/sequence/id/{transcript_id}?type=cds"
	 
	r = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
	 
	if not r.ok:
	  r.raise_for_status()
	  sys.exit()

	return r.text

def summarize_VEP_response(json_fp: str):
	with open(json_fp, 'r') as f:
		data = json.load(f)

	SNP_summary_df = {}
	consequences_dict = {}

	for SNP in data:
		curr_id = SNP["id"]
		for header in SNP:
			if type(SNP[header]) != list:
				if header in SNP_summary_df:
					SNP_summary_df[header].append(SNP[header])
				else:
					SNP_summary_df[header] = [SNP[header]]
			if type(SNP[header]) == list:
				if curr_id in consequences_dict:
					consequences_dict[curr_id][header] = SNP[header]
				else:
					consequences_dict[curr_id] = {
						"regulatory_feature_consequences": [],
						"transcript_consequences": []
					}
					consequences_dict[curr_id][header] = SNP[header]
	return SNP_summary_df, consequences_dict

def dict_to_string(dict_list: dict, title: str):
	seperator = f"{title}\n------------------------------------------------"
	final_str = seperator + "\n"
	for cdict in dict_list:
		all_keys = list(cdict.keys())
		all_keys.sort()
		for key in all_keys:
			space_seperator = " " * (18 - len(key)) + "\t"
			val = cdict[key]
			if type(val) == list:
				val = ' & '.join(val)
			final_str += f"{key}{space_seperator}{val}\n"
		final_str += "\n"

	return final_str + "\n"

def tablize_response(SNP_summary_df: dict, consequences_dict: dict, extract_name: str):
	os.system(f"mkdir ./extracted_consequences/{extract_name}/")
	# os.system(f"touch ./extracted_consequences/{extract_name}/VEP_Table.txt")
	SNP_summary_df = pd.DataFrame(SNP_summary_df)
	print(SNP_summary_df)
	SNP_summary_df.to_csv(f"./extracted_consequences/{extract_name}/SNP_summary.csv")

	final_txt = ""
	for seqid in consequences_dict:
		newseqid = seqid
		while "/" in newseqid:
			newseqid.replace("/", "")
		seqid = newseqid
		os.system(f"mkdir ./extracted_consequences/{extract_name}/{seqid}")
		# os.system(f"touch ./extracted_consequences/{extract_name}/{seqid}/reg_cons.json")
		# os.system(f"touch ./extracted_consequences/{extract_name}/{seqid}/transcript_cons.json")

		cdict_list = consequences_dict[seqid]['regulatory_feature_consequences']
		cdict_json = json.dumps(cdict_list)
		tdict_list = consequences_dict[seqid]['transcript_consequences']
		tdict_json = json.dumps(tdict_list)

		space_seperator = " " * (18 - len("SEQUENCE ID")) + "\t"
		final_txt += f"===============================================\nSEQUENCE ID{space_seperator}{seqid}\n\n"
		final_txt += dict_to_string(cdict_list, "Regulatory Feature Consequences")
		final_txt += dict_to_string(tdict_list, "Transcript Consequences")
		final_txt += "\n"

		with open(f"./extracted_consequences/{extract_name}/{seqid}/reg_cons.json", "w") as f:
			json.dump(cdict_json, f)
		with open(f"./extracted_consequences/{extract_name}/{seqid}/transcript_cons.json", "w") as f:
			'''
			for cons in tdict_list:
				if "cdna_start" in cons and "non_coding_transcript_exon_variant" not in cons["consequence_terms"]:
					transcript_id = cons['transcript_id']
					transcript_sequence = get_transcript_sequence(transcript_id)
					with open(f"{transcript_id}.txt", "w") as t:
						t.write(transcript_sequence)
			'''
			json.dump(tdict_json, f)

	print(final_txt)
	with open(f"./extracted_consequences/{extract_name}/VEP_Table.txt", "w") as f:
		f.write(final_txt)

if __name__ == '__main__':
	SNP_summary_df, consequences_dict = summarize_VEP_response("./VEP_data.json")
	tablize_response(SNP_summary_df, consequences_dict, "norm")
