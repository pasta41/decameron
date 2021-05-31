from collections import defaultdict
from datetime import datetime
import math
from operator import itemgetter
import os
import random
import re

import numpy as np
import pandas as pd
import little_mallet_wrapper as lmw
import pdb
import seaborn as sns

import matplotlib.pyplot as plt

import constants

root = "/home/cooper/src/decameron/output_cached/"
output_path_topic_keys = root + "mallet.topic_keys.10"
output_path_topic_distributions = root + "mallet.topic_distributions.10"

topic_keys = lmw.load_topic_keys(output_path_topic_keys)
topic_distributions = lmw.load_topic_distributions(output_path_topic_distributions)

truncated_topics = [', '.join(x[:5]) for x in topic_keys]
truncated_topics_edited = truncated_topics[:5] + truncated_topics[6:8] + truncated_topics[9:]

decameron_path = "/home/cooper/src/decameron/data/csv/decameron.csv"

def group_wordcounts_by_attr(combined_df, attr):
	wordcounts = combined_df.groupby([attr])[['{}_unnorm'.format(i) for i in range(10)]].sum()
	for i in range(10):
		wordcounts['{}_norm'.format(i)] = wordcounts['{}_unnorm'.format(i)] / combined_df.groupby([attr])['Word Count'].sum()
	return wordcounts

def plot_heatmap(wordcounts, out_file_name, vmax, color):
	f, ax = plt.subplots(figsize=[10,10])
	sns.heatmap(wordcounts[['{}_norm'.format(i) for i in range(10)]].drop("8_norm", axis=1).drop("5_norm", axis=1), 
		vmax=vmax, cmap=sns.light_palette(color, as_cmap=True), 
		annot=True, fmt='.3f', cbar=False)
	sns.set_context('talk')

	plt.xticks(np.arange(8) + .5, truncated_topics_edited, rotation=45, ha="right")
	plt.tight_layout()
	plt.savefig("/home/cooper/src/decameron/fig/" + out_file_name)

def narrator_topics_barplot(narrator_wordcounts, narrator):
	f, ax = plt.subplots(figsize=[8,8])
	narrator_wordcounts_edited = narrator_wordcounts.drop("8_norm", axis=1).drop("5_norm", axis=1)
	cols = [0, 1, 2, 3, 4, 6, 7, 9]
	narrator_wordcounts_edited.loc[narrator][['{}_norm'.format(i) for i in cols]].plot(kind="bar")
	plt.title("Topic Proportions for " + narrator.capitalize())
	ax.set_xticklabels(truncated_topics_edited, rotation=45, ha='right')
	plt.tight_layout()
	#plt.show()
	plt.savefig("/home/cooper/src/decameron/fig/" + narrator + ".pdf")

decameron_df = pd.read_csv(decameron_path)

training_data = [lmw.process_string(t, 
	stop_words=constants.stop_words) for t in decameron_df[decameron_df['Day']==1]['Text'].values]
training_data = [d for d in training_data if d.strip()]

#word_count_per_story = [len(d.split(' ')) for d in training_data]
decameron_df['Word Count'] = decameron_df['Text'].str.split(' ').apply(lambda x: len(x))

# Compute unnormalized topic breakdown, based on per-story wordcount
combined_df = pd.concat([decameron_df, pd.DataFrame(topic_distributions)], axis=1)
for i in range(10):
    combined_df['{}_unnorm'.format(i)] = combined_df[i] * combined_df['Word Count']

# Analysis to give topic distributions by Day
day_wordcounts = group_wordcounts_by_attr(combined_df, 'Day')
plot_heatmap(day_wordcounts, "day_topics.pdf", .09, "#be0119")

# Analysis to give topic distributions by Narrator
narrator_wordcounts = group_wordcounts_by_attr(combined_df, 'Narrator')
plot_heatmap(narrator_wordcounts, "narrator_topics.pdf", .08, "#0b2a63")

# Analysis to give topic distributions by Gender of narrator
gender_wordcounts = group_wordcounts_by_attr(combined_df, 'Gender')
plot_heatmap(gender_wordcounts, "gender_topics.pdf", .05, "#0e5e24")

# Analysis to give bar plot for each narrator
for narrator in constants.narrators:
	narrator_topics_barplot(narrator_wordcounts, narrator)
