## LDA

# for mallet
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

path_to_mallet = "~/mallet-2.0.8/bin/mallet"

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

training_data = [lmw.process_string(t, stop_words=stop_words) for t in decameron_df['Text'].tolist()]
training_data = [d for d in training_data if d.strip()]

#print(len(training_data))



lmw.print_dataset_stats(training_data)

num_topics = 10
output_directory_path = '/home/cooper/src/decameron/output'

topic_keys, topic_distributions = lmw.quick_train_topic_model(path_to_mallet,
															  output_directory_path,
															  num_topics,
															  training_data)

assert(len(topic_distributions) == len(training_data))

for i, t in enumerate(topic_keys):
	print(i, '\t', ' '.join(t[:10]))

