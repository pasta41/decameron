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
import constants

path_to_mallet = "~/mallet-2.0.8/bin/mallet"
decameron_path = "/home/cooper/src/decameron/data/csv/decameron.csv"

decameron_df = pd.read_csv(decameron_path)


training_data = [lmw.process_string(t, 
	stop_words=constants.stop_words) for t in decameron_df['Text'].tolist()]
training_data = [d for d in training_data if d.strip()]

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
