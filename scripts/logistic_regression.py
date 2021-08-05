from collections import defaultdict
import random
import pickle
import json
import pandas as pd
import numpy as np

# scikit learn
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# For plotting and data visualization
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker

import constants
import sys

sns.set(style='ticks', font_scale=1.2)

# load the data
decameron_path = "/home/cooper/src/decameron/data/csv/decameron.csv"

# horrible, disgusting use of globals
decameron_df = pd.read_csv(decameron_path)
story_ids = decameron_df["ID"].tolist()
chunk_size = 80
train_set_story_ids = []
test_set_story_ids = []
classify_by_gender = False
debug = True

# first, we want to split into train and test datasets
# for training, we want to make sure that we have chunked into
# small pieces of text. We are going to divide the text into 100-word
# pieces (and not worry about leftover for simplicity)
# we also want to make sure that the train chunks come from stories
# that do not overlap with the test stories

# so to start, we will sample 80% (80) of the stories for train,
# 20% for test, and then we will chunk them

# num_train is the number of stories that will be used for training; 
# 10 - num_train is number used for test, per storyteller
def storyteller_train_test_split(storyteller, num_train=8):
	# get story ids for the story teller
	storyteller_ids =  decameron_df[decameron_df['Narrator']==storyteller]['ID'].tolist()
	train_set_story_ids = random.sample(storyteller_ids, 8)
	test_set_story_ids = [x for x in storyteller_ids if x not in train_set_story_ids]
	return train_set_story_ids, test_set_story_ids

# 30 stories by men, 70 by women
# so for 80/20 train/test, we want 24 of men, 56 of the women for train
def gender_test_train_split(gender, prop_train=.8):
	gender_ids =  decameron_df[decameron_df['Gender']==gender]['ID'].tolist()
	num_train = int(prop_train * len(gender_ids))
	train_gender_ids = random.sample(gender_ids, num_train)
	test_gender_ids = [x for x in gender_ids if x not in train_gender_ids]
	return train_gender_ids, test_gender_ids

def pair_test_train_split(storyteller1, storyteller2, num_train=8):
	train_1, test_1 = storyteller_train_test_split(storyteller1, num_train)
	train_2, test_2 = storyteller_train_test_split(storyteller2, num_train)
	train_1.extend(train_2)
	test_1.extend(test_2)
	return train_1, test_1

# construct the training and test sets. We will chunk each story
# into n words (not caring about the remainder) and each chunk will
# be a data point. The corresponding label will be the storyteller for
# to story to which the chunk belongs 
def chunk_story(story_id, n):
	story = decameron_df[decameron_df['ID']==story_id]
	text = story['Text'].item()

	# there has to be a better way to do this, but whatever
	words = text.split()
	# rejoin words every n words, put into list
	story_chunks = [" ".join(words[i:i+n]) for i in range(0, len(words), n)]
	return story_chunks, story['Narrator'].item(), story['Gender'].item()

# iterate through train story ids, chunk story, put into train set; same
# for test set
def create_data_set(story_ids, chunk_size, use_gender):
	texts = []
	labels = []
	for story_id in story_ids:
		# heinous factoring...whatever
		story_chunks, storyteller, gender = chunk_story(story_id, chunk_size)
		for chunk in story_chunks:
			# add each chunk as a traing put for that storyteller
			texts.append(chunk)
			if use_gender:
				labels.append(gender)
			else:
				labels.append(storyteller)
	return texts, labels

# run logistic regression
def run_logistic_regression(chunk_size, train_set_story_ids, test_set_story_ids):
	train_texts, train_labels = create_data_set(train_set_story_ids, chunk_size, classify_by_gender)
	test_texts, test_labels = create_data_set(test_set_story_ids, chunk_size, classify_by_gender)

	# run logistics regression
	vectorizer = TfidfVectorizer()
	X_train = vectorizer.fit_transform(train_texts)
	X_test = vectorizer.transform(test_texts)

	model = LogisticRegression(max_iter=5000).fit(X_train, train_labels)
	predictions = model.predict(X_test)
	return test_labels, predictions

# print and run
def print_and_run(train_set_story_ids, test_set_story_ids, chunk_size):
	if debug:
		# write this to save to a file so that can re-run exact config
		print("Train story ids:")
		print(decameron_df[decameron_df['ID'].isin(train_set_story_ids)][['ID', 'Narrator', 'Gender']])
		print()
		print("Test story ids:")
		print(decameron_df[decameron_df['ID'].isin(test_set_story_ids)][['ID', 'Narrator', 'Gender']])
		print()
	test_labels, predictions = run_logistic_regression(chunk_size, train_set_story_ids, test_set_story_ids)
	print(classification_report(test_labels, predictions))

# this is hideous but i forgot python and arg parser and this works

# valid arguments: random gender | random storyteller
if sys.argv[1]=='random':
	classify_by_gender = sys.argv[2] == 'gender'
	train_set_story_ids = random.sample(story_ids, 80)
	test_set_story_ids = [x for x in story_ids if x not in train_set_story_ids]
	print("Using random representation of {} in train/test split.\n\n".format(sys.argv[2]))
	print_and_run(train_set_story_ids, test_set_story_ids, chunk_size)

# valid arguments: representative gender | representative storyteller
elif sys.argv[1]=='representative':
	classify_by_gender = sys.argv[2] == 'gender'
	# make sure that we are getting equal representation in the train/test split
	if sys.argv[2] == 'storyteller':
		for storyteller in constants.narrators:
			storyteller_train_ids, storyteller_test_ids = storyteller_train_test_split(storyteller)
			train_set_story_ids.extend(storyteller_train_ids)
			test_set_story_ids.extend(storyteller_test_ids)
	elif classify_by_gender:
		women_train_ids, women_test_ids = gender_test_train_split("woman")
		men_train_ids, men_test_ids = gender_test_train_split("man")
		train_set_story_ids.extend(women_train_ids)
		train_set_story_ids.extend(men_train_ids)
		test_set_story_ids.extend(women_test_ids)
		test_set_story_ids.extend(men_test_ids)
	else:
		print("Second argument after 'representative' must be 'storyteller' or 'gender'.")
		exit(1)
	print("Using representative representation of {} in train/test split.\n\n".format(sys.argv[2]))
	print_and_run(train_set_story_ids, test_set_story_ids, chunk_size)

# valid arguments: pair <storyteller1> <storyteller2> (storyteller1 != storyteller2)	
elif sys.argv[1] == 'pair':
	if len(sys.argv) != 4:
		print("Must supply two different storyteller names when running in 'pair' mode.")
		exit(1)

	storyteller1 = sys.argv[2]
	storyteller2 = sys.argv[3]

	if storyteller1 not in constants.narrators:
		print("First storyteller 1 invalid: {}; must be in {}", storyteller1, constants.narrators)
		exit(1)

	if storyteller2 not in constants.narrators:
		print("First storyteller 2 invalid: {}; must be in {}", storyteller2, constants.narrators)
		exit(1)

	if storyteller1 == storyteller2:
		print("Storytellers must be different.")
		exit(1)

	train_set_story_ids, test_set_story_ids = pair_test_train_split(storyteller1, storyteller2)
	print("Using representative representation of {} and {} in train/test split.\n\n".format(storyteller1, storyteller2))
	print_and_run(train_set_story_ids, test_set_story_ids, chunk_size)
elif sys.argv[1] == 'all-pairs':
	debug = False
	# store results? they kinda suck
	for storyteller1 in constants.narrators:
		for storyteller2 in constants.narrators:
			if storyteller1 != storyteller2:
				train_set_story_ids, test_set_story_ids = pair_test_train_split(storyteller1, storyteller2)
				print("Using representative representation of {} and {} in train/test split.\n\n".format(storyteller1, storyteller2))
				print_and_run(train_set_story_ids, test_set_story_ids, chunk_size)
else:
	print("Invalid argument: {}. Supply 'random' or 'representative', 'pair' or 'all-pairs' as first argument.".format(sys.argv[1]))

