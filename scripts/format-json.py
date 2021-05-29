import json
import sys

# each newline in the list is some weird stanza formatting; each element
# in the list is actually a new paragraph. I don't think we need to
# preserve either, but this is something to revisit later
def remove_stanza(stanza):
	return stanza.replace("\n", " ")

def join_and_space(list_of_paragraphs):
	return remove_stanza(''.join([(str(elem) + " ") for elem in list_of_paragraphs])).strip()

def join_and_space_flat(paragraphs):
	return remove_stanza(paragraphs).strip()

# combine rubric and body; TODO revisit this when add comma numbers
def combine_rubric_and_text(rubric, text):
	return rubric + " " + text

def get_conclusion_unformatted(remainder_unformatted, day_index_unformatted):
	# conclusion is the last (11th index) element of the day
	conclusion_unformatted = remainder_unformatted[day_index_unformatted]["div2"][11]
	day_index_formatted = str(day_index_unformatted + 1)
	day_conclusion_formatted = days_structure[day_index_formatted]["sections"]["conclusion"]
	return conclusion_unformatted, day_index_formatted, day_conclusion_formatted

def get_conclusion_song(conclusion_unformatted):
	conclusion_song = conclusion_unformatted['lg']['lg']

	# could do this with map, but don't care enough to
	song = ""
	for i in range(0, len(conclusion_song)):
		stanza = join_and_space(conclusion_song[i]['l'])
		song += stanza + " "

	song = song.strip()
	return song

def put_day_conclusion_and_song(remainder_unformatted, phrase_after_song, day_index_unformatted):
	conclusion_unformatted, day_index_formatted, day_conclusion_formatted = get_conclusion_unformatted(
		remainder_unformatted, day_index_unformatted)
	conclusion_body = join_and_space(conclusion_unformatted['p'])
	
	# splice song into the right spot
	x = conclusion_body.find(phrase_after_song)
	song = get_conclusion_song(conclusion_unformatted)
	conclusion_formatted = conclusion_body[:x] + song + " " + conclusion_body[x:]
	day_conclusion_formatted["text"] = conclusion_formatted

# for splicing text in with a space already there to mark it
def splice_phrase_in(text, phrase, phrase_after):
	x = text.find(phrase_after)
	formatted = (text[:x] + phrase).strip() + text[x:]
	return formatted

# splice latin in; stop at that point in p list; return flat text

def splice_latin_in(text_list, start_index, latin_index, phrase_after_latin):
	it_formatted = join_and_space(text_list[start_index:latin_index])
	latin = text_list[latin_index]['foreign']['#text']
	text_with_latin = join_and_space_flat(text_list[latin_index]['#text'])
	joined_latin = splice_phrase_in(text_with_latin, latin, phrase_after_latin)
	return it_formatted + " " + joined_latin

# for day 5 conclusion
def get_day_5_conclusion(remainder_unformatted, day_index_unformatted, phrase_after_song):
	conclusion_unformatted, day_index_formatted, day_conclusion_formatted = get_conclusion_unformatted(
		remainder_unformatted, day_index_unformatted)
	p_conclusion_unformatted = conclusion_unformatted['p']
	first_three = join_and_space(p_conclusion_unformatted[0:3])
	fourth_unformatted = p_conclusion_unformatted[3]
	fourth = join_and_space_flat(splice_phrase_in(fourth_unformatted["#text"], 
		fourth_unformatted["emph"], 
		". Di che tutte le donne cominciarono"))
	conclusion_without_song = first_three + " " + fourth

	fifth_unformatted = p_conclusion_unformatted[4]
	fifth_cur = splice_phrase_in(fifth_unformatted["#text"],
		fifth_unformatted["emph"][0], " o ")
	fifth_cur = splice_phrase_in(fifth_cur, fifth_unformatted["emph"][1], "; o voleste voi che")
	fifth_cur = splice_phrase_in(fifth_cur, fifth_unformatted["emph"][2], "? Ma io")
	fifth_cur = splice_phrase_in(fifth_cur, fifth_unformatted["emph"][3], "?–")
	fifth = join_and_space_flat(fifth_cur)
	conclusion_without_song += " " + fifth + " " + p_conclusion_unformatted[5]

	seventh_unformatted = p_conclusion_unformatted[6]
	seventh = join_and_space_flat(splice_phrase_in(seventh_unformatted["#text"], 
		seventh_unformatted["emph"], 
		".–"))
	conclusion_without_song += " " + seventh + " " + join_and_space_flat(p_conclusion_unformatted[7])

	ninth_unformatted = p_conclusion_unformatted[8]
	ninth_cur = splice_phrase_in(ninth_unformatted["#text"],
		ninth_unformatted["emph"][0], " o ")
	ninth_cur = splice_phrase_in(ninth_cur,
		ninth_unformatted["emph"][1], "  o")
	x = ninth_cur.find("Deh")
	ninth_cur = ninth_cur[:x] + " " + ninth_cur[x: ]
	ninth_cur = splice_phrase_in(ninth_cur,
		ninth_unformatted["emph"][2], "?–")
	x = ninth_cur.find("  o")
	ninth_cur = ninth_cur[:x] + ninth_cur[x+1: ]
	conclusion_without_song += " " + join_and_space_flat(ninth_cur)
	conclusion_without_song += " " + join_and_space_flat(p_conclusion_unformatted[9]) 
	conclusion_without_song += " "  + join_and_space_flat(p_conclusion_unformatted[10]) 
	conclusion_without_song += " " + join_and_space_flat(p_conclusion_unformatted[11])
	conclusion_body = conclusion_without_song
	# splice song into the right spot
	x = conclusion_body.find(phrase_after_song)
	song = get_conclusion_song(conclusion_unformatted)
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
	join_and_space_intro = ""
	# intros 2, 8, and 10 are not lists of lines; just all flat in one field
	if day_formatted_index in ["2", "8", "10"]:
		join_and_space_intro = join_and_space_flat(intro)
	elif day_formatted_index == "5":
		# there is latin in the 5th intro
		latin = intro["foreign"]["#text"]
		italian = intro["#text"]
		# italian is flat
		intro_flat = join_and_space_flat(italian)
		join_and_space_intro = splice_phrase_in(intro_flat, latin, ", verso Panfilo riguardando")
	else:
		join_and_space_intro = join_and_space(intro)

	intro = combine_rubric_and_text(day_rubric, join_and_space_intro)

	current_day_formatted["introduction"]["text"] = intro

	# get stories; inner loop for each of the 10; format
	# from 1 to 10, since those are the indices for the stories
	for story_index in range(1, 11):
		current_story_unformatted = day_body_unformatted[story_index]

		# get rubric
		current_story_rubric = remove_stanza(
			current_story_unformatted["argument"]["p"]["emph"])
		# get story, combine with rubric; format
		current_story_unformatted_p = current_story_unformatted["p"]
		
		# 1.6 has latin in it, in own dict
		if day_formatted_index == "1" and story_index == 6:
			current_story = current_story_rubric + " "
			current_story += splice_latin_in(current_story_unformatted_p, 0, 2, " impetuosissimamente")
			remainder_story = join_and_space(current_story_unformatted_p[3:])
			current_story += remainder_story
		# 1.9 has latin in it, in own dict	
		elif day_formatted_index == "1" and story_index == 9:
			current_story = current_story_rubric + " "
			current_story += splice_latin_in(current_story_unformatted_p, 0, 1, " detta, l'ha operato")
			remainder_story = join_and_space(current_story_unformatted_p[3:])
			current_story += remainder_story
		# 2.2 has a bunch of stuff going on in it	
		elif day_formatted_index == "2" and story_index == 2:
			current_story = current_story_rubric + " "
			
			flat_it_1 = join_and_space(current_story_unformatted_p[0:7])

			inner = current_story_unformatted_p[7]
			formatted_special = join_and_space_flat(inner['#text'])
			formatted_special =  splice_phrase_in(formatted_special, inner['foreign'][0]['#text'], " o la ")
			formatted_special = splice_phrase_in(formatted_special, inner['emph'], " o il ")
			formatted_special = splice_phrase_in(formatted_special, inner['foreign'][1]['#text'], ", che sono, secondo che una ")

			flat_it_2 = join_and_space(current_story_unformatted_p[8:])
			
			current_story += flat_it_1 + " " + formatted_special + " " + flat_it_2
		# 3.8 has latin in it, in own dict	
		elif day_formatted_index == "3" and story_index == 8:
			current_story = current_story_rubric + " "
			current_story += splice_latin_in(current_story_unformatted_p, 0, 58, ". Ferondo torn")
			remainder_story = join_and_space(current_story_unformatted_p[59:])
			current_story += remainder_story
		# 7.1 has latin in it, in own dict
		elif day_formatted_index == "7" and story_index == 1:
			current_story = current_story_rubric + " "
			flat_it_1 = join_and_space(current_story_unformatted_p[0:8])
			inner = current_story_unformatted_p[8]
			formatted_special = join_and_space_flat(inner['#text'])
			formatted_special =  splice_phrase_in(formatted_special, inner['foreign']['#text'], " e la ")
			formatted_special = splice_phrase_in(formatted_special, inner['emph'], " e tante altre buone")

			flat_it_2 = join_and_space(current_story_unformatted_p[9:])

			current_story += flat_it_1 + " " + formatted_special + " " + flat_it_2
		else:
			current_story = combine_rubric_and_text(current_story_rubric,
				join_and_space(current_story_unformatted_p))

			# 4.5  has a song in it with italicized text
			if day_formatted_index == "4" and story_index == 5:
				song = current_story_unformatted["lg"]["l"]
				# song is a list of 2 maps
				song_flattened = song[0]["emph"] + " " + song[1]["emph"] + " " + song[1]["#text"]
				#print(song_flattened) song at end of story
				current_story = current_story + " " + song_flattened

		current_day_formatted[str(story_index)]["text"] = current_story

# overwrite stories that have songs in them TODO

# clean up latin todo search for @

# write story conclusions (one at a time because of weird formatting)

# conclusion 1
put_day_conclusion_and_song(remainder_unformatted, "Questa ballatetta finita", 0)

# conclusion 2
put_day_conclusion_and_song(remainder_unformatted, "Appresso questa, più altre se ne cantarono e più", 1)

# conclusion 3
put_day_conclusion_and_song(remainder_unformatted, "Qui fece fine la Lauretta alla sua canzone", 2)

# conclusion 4
put_day_conclusion_and_song(remainder_unformatted, "Dimostrarono le parole di questa canzone", 3)

# conclusion 5 -- has lots of formatted text / is "special"
get_day_5_conclusion(remainder_unformatted, 4, "Da poi che Dioneo tacendo")

# conclusion 6
put_day_conclusion_and_song(remainder_unformatted, "Poi che con un sospiro assai", 5)

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

