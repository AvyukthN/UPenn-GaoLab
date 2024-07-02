import requests, sys
import pandas as pd
from tqdm import tqdm
import json
import os

def process_VEP_test(filename: str) -> list:
	with open(filename, 'r') as f:
		lines = [l.split('\t') for l in f.read().split('\n')][1:]

	variant_arr = []
	for line in lines:
		if len(''.join(line)) > 0:
			variant_arr.append(f"{line[0].strip()} {int(line[1]) - 1} {line[1]} {line[2]} {line[3]} . . .")	

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
	# print(variant_arr)

	dict_data = {"variants": variant_arr}
	for param in param_args:
		dict_data[param] = 1

	fdata = json.dumps(dict_data)
	# r = requests.post(server+ext, headers=headers, params=params, data='{ "variants" :' + converted_varr_string + '}')
	r = requests.post(server+ext, headers=headers, data=fdata)# '{ "variants" :' + converted_varr_string + '}')

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

if __name__ == '__main__':
	get_response_data()
