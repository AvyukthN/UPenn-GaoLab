import requests, sys
 
server = "https://rest.ensembl.org"
gene_id = "ENSG00000169174"
transcript_id = "ENST00000710286"
ext = f"/sequence/id/{gene_id}?" 
ext = f"/sequence/id/{transcript_id}?type=cds"
 
r = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
 
if not r.ok:
  r.raise_for_status()
  sys.exit()
 
 
print(r.text)

'''
import requests
import json

def get_variants_for_gene(gene_id):
    server = "https://rest.ensembl.org"
    ext = "/vep/human/id"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {"ids": [gene_id]}

    response = requests.post(f"{server}{ext}", headers=headers, data=json.dumps(data))
    
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

# Example usage
gene_id = "ENSG00000169174"
variants = get_variants_for_gene(gene_id)

# Process the results to find variant sequences
for variant in variants:
    if 'seq_region_name' in variant and 'start' in variant and 'end' in variant:
        print(f"Variant on chromosome {variant['seq_region_name']}, position {variant['start']}-{variant['end']}")
        if 'allele_string' in variant:
            print(f"Allele string: {variant['allele_string']}")
    print("---")

print(json.dumps(variants, indent=2))
'''

'''
import requests
from dotenv import load_dotenv
import os

load_dotenv('./authentication.env')
api_key = os.environ.get("NCBI_API_KEY")

base_url = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/"
gene_id = "ENSG00000169174"
endpoint = "gene/id/{gene_id}/download"

headers = {	
	"accept": "application/zip",
	"api-key": api_key
}

res = requests.get(base_url + endpoint, headers=headers)
print(res)
'''
