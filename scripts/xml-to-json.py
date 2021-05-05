import json
import xmltodict
import sys

xml_doc = "../data/xml/raw-decameron.xml"

# TODO argparse library
if len(sys.argv) > 1:
	xml_doc = sys.argv[1]

with open(xml_doc) as xml_file:
	data_dict = xmltodict.parse(xml_file.read())
	xml_file.close()
	json_data = json.dumps(data_dict, indent=4, ensure_ascii=False)
	# TODO make general
	with open("../data/json/raw-decameron.json", "w", encoding='utf8') as json_file:
		json_file.write(json_data)
		json_file.close()
