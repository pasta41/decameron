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

train_set_story_ids = random.sample(story_ids, 80)
test_set_story_ids = [x for x in story_ids if x not in train_set_story_ids]

print(len(test_set_story_ids))
#print(len(story_ids))

# first, we want to split into train and test datasets

# for training, we want to make sure that we have chunked into
# small pieces of text. We are going to divide the text into 100-word
# pieces (and not worry about leftover for simplicity)

# we also want to make sure that the train chunks come from stories
# that do not overlap with the test stories
# so to start, we will sample 80% (80) of the stories for train,
# 20% for test, and then we will chunk them


train_texts = []
train_labels = []

test_texts = []
test_labels = []

