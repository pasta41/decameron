import json
import sys

# open raw converted from xml decameron json
json_doc = "../data/json/raw-decameron.json"

data = None
with open(json_doc) as f:
  data = json.load(f)

# open json structure we want
structure_doc = "../data/json/decameron_structure.json"

structure = None
with open(structure_doc) as f:
  structure = json.load(f)


# process raw json to get text; put in the format we want

# skip metadata; this will subset to json with 2
# top-level keys, "front" (which contains the proem)
# and "body" which contains everything else, including
# the author's conclusion 
decameron = data["TEI.2"]["text"]


# Proem

proem = decameron["front"]["div1"]
proem_rubric = proem["argument"]["p"]

# remove stanza formatting
proem_rubric = proem_rubric.replace("\n", " ")

proem_body = proem["p"] # this is a list that preserves new paragraphs

# each newline in the list is some weird stanza formatting; each element
# in the list is actually a new paragraph. I don't think we need to
# preserve either, but this is something to revisit later

# convert list to one long string
proem_body_str = ''.join([str(elem) for elem in proem_body])
# remove stanza formatting
proem_body_str = proem_body_str.replace("\n", " ")


# combine rubric and body; TODO revisit this when add comma numbers
proem_flattened = proem_rubric + " " + proem_body_str

# put proem in desired format location

text = structure["decameron"]

text["proem"]["text"] = proem_flattened


print(text["proem"])

#for k,v in text.items():
#	print(k)
