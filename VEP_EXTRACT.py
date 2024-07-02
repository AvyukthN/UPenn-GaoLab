import sys
import os
from VEP_params_api import get_response_data
from intermediate_preprocessor import intermediate_preprocessor
from parse_VEP_json import summarize_VEP_response, tablize_response

if __name__ == '__main__':
	'''
	params

	arg0	VEP_EXTRACT.py
	arg1	*SNP DATA TEXT FILE*
	arg2	*OUT JSON FILEPATH*
	arg3	*EXTRACT FOLDER NAME*
	arg4+	*VEP API params*
	'''

	out_json_fp = sys.argv[2]
	extract_folder = sys.argv[3]
	try:
		param = sys.argv[4]
	except IndexError:
		param = ""

	full_VEP_jsonfp = f'./extracted_consequences/{extract_folder}/{out_json_fp}'

	get_response_data(list(sys.argv), extract_folder)
	if param != "":
		intermediate_preprocessor(param, full_VEP_jsonfp) 
	SNP_summary_df, consequences_dict = summarize_VEP_response(full_VEP_jsonfp)
	tablize_response(SNP_summary_df, consequences_dict, extract_folder)
