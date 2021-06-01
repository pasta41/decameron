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
import json

import constants

root = "/home/cooper/src/decameron/output_cached/"
output_path_topic_keys = root + "mallet.topic_keys.10"
output_path_topic_distributions = root + "mallet.topic_distributions.10"
output_path_word_distributions = root + "mallet.word_weights.10"

topic_keys = lmw.load_topic_keys(output_path_topic_keys)
topic_distributions = lmw.load_topic_distributions(output_path_topic_distributions)
word_distributions = lmw.load_topic_word_distributions(output_path_word_distributions)


topics_edited_names = ['seafaring', 'peasants/farming', 'knights/nobility', 'courts/laws',
	'merchants/economy', "common1", 'courtesy', 'religion/sin', "common2", 'love/vengeance']

topics_dict = {}

for i in range(10):
	topics_dict[topics_edited_names[i]] = topic_keys[i]

print(json.dumps(topics_dict, indent=2, ensure_ascii=False))

for i in range(10):
	print(i)
	print(topic_keys[i])
	print()