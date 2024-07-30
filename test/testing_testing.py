import requests

# Define the URL endpoint
base_url = "https://rest.ensembl.org/vep/human/region"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"  # We'll get JSON back, which includes VCF-style data
}

# Define the payload with the variants
payload = {
    "variants": [
        "7 140453136 . T C",
        "7 140453136 . T G"
    ]
}

# Define query parameters
params = {
    "vcf": 1,  # This corresponds to the --vcf flag
    "canonical": 1
}

# Make the POST request
response = requests.post(base_url, headers=headers, json=payload, params=params)

# Check if the request was successful
if response.status_code == 200:
    print("Request was successful")
    vep_response = response.json()
    
    # The VCF-style output will be in the 'input' field of each variant result
    for variant in vep_response:
        print(variant['input'])
    
    # Optionally, save the VCF-style output to a file
    with open("output.vcf", "w") as vcf_file:
        vcf_file.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")  # VCF header
        for variant in vep_response:
            vcf_file.write(variant['input'] + "\n")
    print("VCF-style output saved to 'output.vcf'")
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
