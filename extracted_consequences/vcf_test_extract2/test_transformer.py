import pandas as pd
import json
# from pandas.io.json import json_normalize

def flatten_json(nested_json):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

# Assuming your JSON data is in a file called 'data.json'
fp = "vcfTest.json"
with open(fp, 'r') as file:
    data = json.load(file)

# If data is a list of dictionaries
flat_data = [flatten_json(d) for d in data]
df = pd.DataFrame(flat_data)
df.to_csv("test_flatten.csv", index=False)

# If data is a single dictionary
# flat_data = flatten_json(data)
# df = pd.DataFrame([flat_data])
