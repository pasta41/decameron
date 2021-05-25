import json
import sys

# each newline in the list is some weird stanza formatting; each element
# in the list is actually a new paragraph. I don't think we need to
# preserve either, but this is something to revisit later
def remove_stanza(stanza):
	return stanza.replace("\n", " ")

def join_and_space(list_of_paragraphs):
	return remove_stanza(''.join([(str(elem) + " ") for elem in list_of_paragraphs])).strip()

# combine rubric and body; TODO revisit this when add comma numbers
def combine_rubric_and_text(rubric, text):
	return rubric + " " + text

def put_day_conclusion_and_song(remainder_unformatted, phrase_after_song):
	day_index_unformatted = 0
	# conclusion is the last (11th index) element of the day
	conclusion_unformatted = remainder_unformatted[day_index_unformatted]["div2"][11]
	day_index_formatted = str(day_index_unformatted + 1)
	day_conclusion_formatted = days_structure[day_index_formatted]["sections"]["conclusion"]

	conclusion_body = join_and_space(conclusion_unformatted['p'])
	conclusion_song = conclusion_unformatted['lg']['lg']

	# could do this with map, but don't care enough to
	song = ""
	for i in range(0, len(conclusion_song)):
		stanza = join_and_space(conclusion_song[i]['l'])
		song += stanza + " "

	song = song.strip()

	# splice song into the right spot
	x = conclusion_body.find(phrase_after_song)
	conclusion_formatted = conclusion_body[:x] + song + " " + conclusion_body[x:]
	day_conclusion_formatted["text"] = conclusion_formatted

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
	print(day_formatted_index)
	print(intro)
	print()
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

# overwrite stories that have songs in them TODO

# clean up latin todo search for @

# write story conclusions (one at a time because of weird formatting)

# conclusion 1
put_day_conclusion_and_song(remainder_unformatted, "Questa ballatetta finita")

# conclusion 2

# conclusion 3

# conclusion 4

# conclusion 5

# conclusion 6

# conclusion 7

# conclusion 8

# conclusion 9

# conclusion 10

# write authors conclusion out
conclusion_unformatted = remainder_unformatted[10]
# get conclusion body; put into new structure
conclusion_body = join_and_space(conclusion_unformatted["p"])
conclusion_trailer = join_and_space(conclusion_unformatted["trailer"])
conclusion = combine_rubric_and_text(conclusion_body, conclusion_trailer)
text["conclusion"]["text"] = conclusion

# write out decameron in formatted structure
with open("../data/json/decameron.json", "w", encoding='utf8') as json_file:
	json.dump(structure, json_file, indent=2, ensure_ascii=False)

