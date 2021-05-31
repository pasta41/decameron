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

root = "/home/cooper/src/decameron/output_cached/"
output_path_topic_keys = root + "mallet.topic_keys.10"
output_path_topic_distributions = root + "mallet.topic_distributions.10"

topic_keys = lmw.load_topic_keys(output_path_topic_keys)
topic_distributions = lmw.load_topic_distributions(output_path_topic_distributions)

decameron_path = "/home/cooper/src/decameron/data/csv/decameron.csv"

decameron_df = pd.read_csv(decameron_path)
#print(decameron_df.sample(5))
#(len(decameron_df.index))


stop_words = ['il', 'lo', 'la', 'i', 'le', 'gli', 'è', 'tu', 'tuo', 'tua', 'suo', 'sue',
			  'suoi', 'sua', 'loro', 'lei', 'quale', 'quali', 'questa', 'questo', 'cosa',
			  'che', 'non', 'per', 'come', 'egli', 'voi', 'del', 'della', 'così',  'più',
			  'con', 'col', 'cui', 'una', 'qual', 'fu', 'fosse', 'era', 'lui', 'quello',
			  'senza', 'alla', 'dove', 'già', 'ogni', 'vostra', 'vostro', 'vostri', 'vostre',
			  'nostro', 'nostra', 'nostre', 'nostri', 'altro', 'altra', 'altre', 'altri',
			  'molto', 'molta', 'molte', 'molti', 'nel', 'ciò', 'quella', 'bene', 'ben',
			  'ella', 'disse', 'sopra', 'noi', 'alessandro', 'ruggieri', 'cimone', 'saladino',
			  'nicostrato', 'bernabò', 'ser', 'ciappelletto', 'esser', 'essere', 'fa', 'fare',
			  'alcuna', 'alcun', 'alcuno', 'ora', 'far', 'quando', 'natan', 'pietro', 'mitridanes',
			  'gualtieri', 'filippo', 'alberto', 'ferondo', 'gianni', 'fatto', 'tito', 'currado',
			  'guiscardo', 'ché', 'ricciardo', 'nastagio', 'riccardo', 'chichibio', 'tedaldo',
			  'bruno', 'gisippo', 'federigo', 'mai', 'ma', 'poi', 'aveva', 'mio', 'mia', 'masetto',
			  'rinaldo', 'ambruogiuolo', 'nella', 'nello', 'lor', 'erano', 'lor', 'gerbino', 
			  'andreuccio', 'gabriotto', 'tanto', 'tanti', 'tante', 'tanta', 'cose', 'delle',
			  'calandrino', 'buffalmacco', 'rustico', 'arriguccio', 'tancredi', 'giosefo',
			  'melisso', 'quanto', 'dentro', 'aldobrandino', 'tutto', 'tutta', 'tutti', 'tutte',
			  'nelle', 'giù', 'assai', 'avea', 'dire', 'avendo', 'essendo', 'guiglielmo',
			  'anichino', 'fece', 'sia', 'ancora', 'martuccio', 'efigenia', 'antigono', 'giannetta',
			  'uno', 'avessi', 'egano', 'salabaetto', 'quivi', 'sofronia', 'chi', 'spinelloccio',
			  'giacomino', 'ghino', 'allora', 'angiulieri', 'catella', 'zima', 'geri', 'pavia',
			  'puccio', 'quindi', 'pirro' , 'perché', 'salabaetto', 'giannotto', 'dico', 'griselda', 'niccolosa',
			  'dall']

#training_data = lmw.process_string(t, stop_words=stop_words), for t in decameron_df[decameron_df['Day'=='1']]['Text'].values
training_data = [lmw.process_string(t, stop_words=stop_words) for t in decameron_df[decameron_df['Day']==1]['Text'].values]
#decameron_df[decameron_df['Day']=='10']['Text'].values

training_data = [d for d in training_data if d.strip()]

word_count_per_story = [len(d.split(' ')) for d in training_data]
word_count_per_story

decameron_df['Word Count'] = decameron_df['Text'].str.split(' ').apply(lambda x: len(x))
decameron_df['Word Count']

combined_df = pd.concat([decameron_df, pd.DataFrame(topic_distributions)], axis=1)

for i in range(10):
    combined_df['{}_unnorm'.format(i)] = combined_df[i] * combined_df['Word Count']

combined_df

combined_df.groupby(['Day'])[['{}_unnorm'.format(i) for i in range(10)]].sum()
#combined_df.groupby(['Narrator'])[['{}_unnorm'.format(i) for i in range(10)]].sum()

day_wordcounts = combined_df.groupby(['Day'])[['{}_unnorm'.format(i) for i in range(10)]].sum()
for i in range(10):
    day_wordcounts['{}_norm'.format(i)] = day_wordcounts['{}_unnorm'.format(i)] / combined_df.groupby(['Day'])['Word Count'].sum()

f, ax = plt.subplots(figsize=[10,10])
sns.heatmap(day_wordcounts[['{}_norm'.format(i) for i in range(10)]], vmax=.1, cmap=sns.light_palette("#be0119", as_cmap=True), annot=True, fmt='.2f', cbar=False)
sns.set_context('talk')

truncated_topics = [', '.join(x[:5]) for x in topic_keys]

plt.xticks(np.arange(10) + .5, truncated_topics,rotation=45, ha="right")
plt.tight_layout()

narrator_wordcounts = combined_df.groupby(['Narrator'])[['{}_unnorm'.format(i) for i in range(10)]].sum()
for i in range(10):
    narrator_wordcounts['{}_norm'.format(i)] = narrator_wordcounts['{}_unnorm'.format(i)] / combined_df.groupby(['Narrator'])['Word Count'].sum()


f, ax = plt.subplots(figsize=[10,10])
sns.heatmap(narrator_wordcounts[['{}_norm'.format(i) for i in range(10)]].drop("8_norm", axis=1).drop("5_norm", axis=1), vmax=.06, cmap=sns.light_palette("#be0119", as_cmap=True), annot=True, fmt='.2f', cbar=False)
sns.set_context('talk')

truncated_topics = [', '.join(x[:5]) for x in topic_keys]

truncated_topics_edited = truncated_topics[:5] + truncated_topics[6:8] + truncated_topics[9:]

plt.xticks(np.arange(8) + 0.5, truncated_topics_edited, rotation=45, ha="right")
plt.tight_layout()
plt.savefig("/home/cooper/src/decameron/fig/narrator_topics.pdf")

f, ax = plt.subplots(figsize=[8,8])
narrator_wordcounts.ix['dioneo'][['{}_norm'.format(i) for i in range(10)]].plot(kind="bar")
plt.title("Dioneo")
truncated_topics = [', '.join(x[:5]) for x in topic_keys]

ax.set_xticklabels(truncated_topics, rotation=45, ha='right')

