import json
import sys

# each newline in the list is some weird stanza formatting; each element
# in the list is actually a new paragraph. I don't think we need to
# preserve either, but this is something to revisit later
def remove_stanza(stanza):
	return stanza.replace("\n", " ")

def join_and_space(list_of_paragraphs):
	return remove_stanza(''.join([str(elem) for elem in list_of_paragraphs]))

# combine rubric and body; TODO revisit this when add comma numbers
def combine_rubric_and_text(rubric, text):
	return rubric + " " + text

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
proem_rubric = remove_stanza(proem_rubric)

proem_body = proem["p"] # this is a list that preserves new paragraphs
proem_flattened = combine_rubric_and_text(proem_rubric, 
	join_and_space(proem_body))

# put proem in desired format location
text = structure["decameron"]
text["proem"]["text"] = proem_flattened

# grab the remainder of the decameron; conclusion is also in here

# a list of 11 things -- the ten days and the author's conclusion
remainder_unformatted = decameron["body"]["div1"]

# the new structure for the 10 days of stories
days_structure = text["days"]

# for 0 through 9, grab the day
for day_unformatted_index in range(0, 10):
	
	day_unformatted = remainder_unformatted[day_unformatted_index]
	
	# put intro into new day format
	day_formatted_index = str(day_unformatted_index + 1)
	current_day_formatted = days_structure[day_formatted_index]["sections"]

	# get rubric
	day_rubric = remove_stanza(day_unformatted["argument"]["p"])

	# get sections of the day; this is list of intro, 10 stories, conclusion
	# not going to loop / automate the conclusion because they use out-of-order
	# formatting in order to encode metadata about the songs
	# will add story conclusions at the end of the script

	day_body_unformatted = day_unformatted["div2"]

	# get intro; in 0th index; format 
	intro = day_body_unformatted[0]["p"]
	intro = combine_rubric_and_text(day_rubric, join_and_space(intro))
	current_day_formatted["introduction"]["text"] = intro

	# get stories; inner loop for each of the 10; format
	# from 1 to 10, since those are the indices for the stories TODO
	for story_index in range(1, 11):
		current_story_unformatted = day_body_unformatted[story_index]

		# get rubric
		current_story_rubric = remove_stanza(
			current_story_unformatted["argument"]["p"]["emph"])
		# get story, combine with rubric; format
		current_story_unformatted = current_story_unformatted["p"]
		current_story = combine_rubric_and_text(current_story_rubric,
			join_and_space(current_story_unformatted))

		current_day_formatted[str(story_index)]["text"] = current_story

# TODO write conclusions (manually, because of weird formatting)

# write out decameron in formatted structure
with open("../data/json/decameron.json", "w", encoding='utf8') as json_file:
		json.dump(structure, json_file, indent=4, ensure_ascii=False)

# get conclusion; format
#conclusion = day_body_unformatted[11]["p"]
#for k,v in current_story_unformatted.items():
#	print(k)
