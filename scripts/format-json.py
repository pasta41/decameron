import json
import sys

json_doc = "../data/json/raw-decameron.json"

# TODO argparse library
if len(sys.argv) > 1:
	json_doc = sys.argv[1]

data = None

with open(json_doc) as f:
  data = json.load(f)

entries = data.items()

for key, value in entries:
	print(key)

