import pandas as pd
import json

fp = "./VEP_param_test.json"

with open(fp, 'r') as f:
    data = json.load(f)

print(data)
