import pandas as pd
import json
import requests

# Function to flatten the VEP JSON output
def flatten_vep_json(vep_data):
    flattened_data = []
    
    for variant in vep_data:
        base_info = {
            'input': variant.get('input'),
            'id': variant.get('id'),
            'assembly_name': variant.get('assembly_name'),
            'seq_region_name': variant.get('seq_region_name'),
            'start': variant.get('start'),
            'end': variant.get('end'),
            'strand': variant.get('strand'),
            'allele_string': variant.get('allele_string'),
            'most_severe_consequence': variant.get('most_severe_consequence')
        }
        
        # Handle transcript consequences
        transcript_consequences = variant.get('transcript_consequences', [])
        if not transcript_consequences:
            flattened_data.append(base_info)
        else:
            for consequence in transcript_consequences:
                row = base_info.copy()
                row.update({
                    'transcript_id': consequence.get('transcript_id'),
                    'gene_id': consequence.get('gene_id'),
                    'gene_symbol': consequence.get('gene_symbol'),
                    'consequence_terms': ','.join(consequence.get('consequence_terms', [])),
                    'impact': consequence.get('impact'),
                    'biotype': consequence.get('biotype'),
                    # Add more fields from transcript_consequences as needed
                })
                flattened_data.append(row)
    
    return flattened_data

# Assuming you have the VEP API response stored in a variable called 'vep_response'
# If not, you would need to make the API call first, for example:
# response = requests.get('https://rest.ensembl.org/vep/homo_sapiens/region/1:6524705-6524705:1/C', headers={"Content-Type": "application/json"})
# vep_response = response.json()

# For this example, let's assume vep_response is already available
with open("./vcfTest.json", "r") as f:
    vep_response = json.load(f)

# Flatten the VEP JSON
flattened_data = flatten_vep_json(vep_response)

# Create a pandas DataFrame
df = pd.DataFrame(flattened_data)

# Display the DataFrame
print(df)
df.to_csv("test_flatten2.csv")
