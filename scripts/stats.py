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
output_path_word_distributions = root + "mallet.word_weights.10"

topic_keys = lmw.load_topic_keys(output_path_topic_keys)
topic_distributions = lmw.load_topic_distributions(output_path_topic_distributions)
word_distributions = lmw.load_topic_word_distributions(output_path_word_distributions)

for i in range(10):
	print(str(i) + ":\t" + ''.join(str(e) + ", " for e in topic_keys[i]))
	print()
