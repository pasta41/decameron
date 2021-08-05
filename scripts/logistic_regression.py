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
sns.set(style='ticks', font_scale=1.2)

# load the data
decameron_path = "/home/cooper/src/decameron/data/csv/decameron.csv"

decameron_df = pd.read_csv(decameron_path)
story_ids = decameron_df["ID"].tolist()


# first, we want to split into train and test datasets

# for training, we want to make sure that we have chunked into
# small pieces of text. We are going to divide the text into 100-word
# pieces (and not worry about leftover for simplicity)
# we also want to make sure that the train chunks come from stories
# that do not overlap with the test stories

# so to start, we will sample 80% (80) of the stories for train,
# 20% for test, and then we will chunk them

train_set_story_ids = random.sample(story_ids, 80)
test_set_story_ids = [x for x in story_ids if x not in train_set_story_ids]

# next, construct the training and test sets. We will chunk each story
# into 100 words (not caring about the remainder) and each chunk will
# be a data point. The corresponding label will be the storyteller for
# to story to which the chunk belongs 

def chunk_story(story_id, n):
	story = decameron_df[decameron_df['ID']==story_id]
	text = story['Text'].item()

	# there has to be a better way to do this, but whatever
	words = text.split()
	# rejoin words every n words, put into list
	story_chunks = [" ".join(words[i:i+n]) for i in range(0, len(words), n)]
	return story_chunks, story['Narrator'].item()

# iterate through train story ids, chunk story, put into train set; same
# for test set

def create_data_set(story_ids, chunk_size):
	texts = []
	labels = []
	for story_id in story_ids:
		story_chunks, storyteller = chunk_story(story_id, chunk_size)
		for chunk in story_chunks:
			# add each chunk as a traing put for that storyteller
			texts.append(chunk)
			labels.append(storyteller)
	return texts, labels


chunk_size = 50

train_texts, train_labels = create_data_set(train_set_story_ids, chunk_size)
test_texts, test_labels = create_data_set(test_set_story_ids, chunk_size)

print(test_texts)
print(test_labels)
