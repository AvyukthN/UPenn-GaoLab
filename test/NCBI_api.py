import requests, sys
 
server = "https://rest.ensembl.org"
gene_id = "ENSG00000169174"
ext = f"/sequence/id/{gene_id}?"
 
r = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
 
if not r.ok:
  r.raise_for_status()
  sys.exit()
 
print(r.json())

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
