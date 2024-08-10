def process_VEP_test(filename: str) -> list:
	with open(filename, 'r') as f:
		lines = [l.split('\t') for l in f.read().split('\n')][1:]

	variant_arr = []
	for line in lines:
		if len(''.join(line)) > 0:
			variant_arr.append(f"{line[0].strip()} {int(line[1]) - 1} {line[1]} {line[2]} {line[3]} . . .")	

	return variant_arr

print(process_VEP_test("./VCF_tsv.tsv"))
