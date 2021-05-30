import json
import sys
import csv

json_doc = "../data/json/decameron.json"

decameron = None
with open(json_doc) as f:
	decameron = json.load(f)


days = decameron['decameron']['days']

story_indexes = [str(i) for i in range(1,11)]


with open("../data/csv/decameron.csv", "w", encoding='utf8') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow(['Day', 'Story', 'Narrator', 'Text'])
	
	for day_index, day in days.items():
		sections = day['sections']
	
		for story_index in sections.keys():
			if story_index in story_indexes:
				story = sections[story_index]["text"]
				narrator = sections[story_index]["narrator"]
				writer.writerow([day_index, story_index, narrator, story])
