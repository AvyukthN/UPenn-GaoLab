import requests, sys
import pandas as pd
from tqdm import tqdm
import json
import os

def process_VEP_test(filename: str) -> list:
	if filename.split('.')[1] == "txt":
		with open(filename, 'r') as f:
			lines = [l.split('\t') for l in f.read().split('\n')][1:]

		variant_arr = []
		for line in lines:
			if len(''.join(line)) > 0:
				variant_arr.append(f"{line[0].strip()} {int(line[1]) - 1} {line[1]} {line[2]} {line[3]} . . .")	

		return variant_arr
	elif filename.split('.')[-1] == "vcf":
		with open(filename, 'r') as f:
			lines = f.read().split("\n")
			begin_idx = None
			for i in range(len(lines)):
				if lines[i][:6] == "#CHROM":
					begin_idx = i
			lines = lines[begin_idx+1:-1]

		variant_arr = []
		count = 0
		for line in lines:
			while "\t\t" in line:
				line = line.replace("\t\t", "\t")
			line = line.split("\t")
			chrom = line[0].split("r")[1]
			pos = line[1]
			snp_id = line[2]
			ref = line[3]
			alt = line[4]

			if snp_id == ".":
				snp_id = str(count)

			variant_arr.append(f"{chrom} {pos} {snp_id} {ref} {alt} . . .")
			count += 1
		return variant_arr

def process_variant_array(arr: list) -> str:
	arr_str = '['
	for i in range(len(arr)):
		variant = arr[i]
		if i < len(arr) - 1:
			arr_str += '"' + variant + '"' + ', '
		if i == len(arr) - 1:
			arr_str += '"' + variant + '"]'

	return arr_str

def get_response_data(params: list, extract_folder: str): 
	server = "https://rest.ensembl.org"
	ext = "/vep/homo_sapiens/region"
	headers={ "Content-Type" : "application/json", "Accept" : "application/json"}


	param_args = params[4:]

	variant_arr = process_VEP_test(params[1])

	payload = {
		"variants": variant_arr[:10]
	}

	# Define query parameters
	api_params = {}
	for arg in param_args:
		api_params[arg] = 1
	
	base_url = "https://rest.ensembl.org/vep/human/region"

	# Make the POST request
	r = requests.post(base_url, headers=headers, json=payload, params=api_params)

	"""
	print(variant_arr[-1])
	# print(variant_arr)

	dict_data = {"variants": variant_arr}
	# api_params = {}
	for param in param_args:
		# print(param)
		# api_params[param] = 1
		dict_data[param] = 1

	# api_params = json.dumps(api_params)
	# dict_data = json.dumps(dict_data)
	fdata = json.dumps(dict_data)
	# r = requests.post(server+ext, headers=headers, params=params, data='{ "variants" :' + converted_varr_string + '}')
	r = requests.post(server+ext, headers=headers, data=fdata)# '{ "variants" :' + converted_varr_string + '}')
	# r = requests.post(server+ext, headers=headers, json=dict_data, params=api_params)
	"""

	if not r.ok:
	  r.raise_for_status()
	  sys.exit()
	 
	decoded = r.json()

	# print(decoded)
	os.system(f"mkdir ./extracted_consequences/{extract_folder}/")
	with open(f'./extracted_consequences/{extract_folder}/{params[2]}', 'w') as f:
		json.dump(decoded, f)
		# f.write(str(decoded))
	# print(repr(decoded))

	api_params["vcf"] = 1
	r = requests.post(base_url, headers=headers, json=payload, params=api_params)

if __name__ == '__main__':
	get_response_data()
