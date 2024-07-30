import json

def intermediate_preprocessor(param: str, json_fp: str):
	with open(json_fp, 'r') as f:
		data = json.load(f)

	for i in range(len(data)):
		consequences = data[i]["transcript_consequences"]
		final_consequences = []
		for cons in consequences:
			if param in cons.keys():
				final_consequences.append(cons)

		data[i]["transcript_consequences"] = final_consequences

	with open(json_fp, 'w') as f:
		json.dump(data, f)

if __name__ == '__main__':
	intermediate_preprocessor("canonical", "VEP_canonical_data.json")
