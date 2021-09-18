import csv
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

decameron_path = "/home/cooper/src/decameron/data/csv/decameron.csv"
decameron_df = pd.read_csv(decameron_path)


stories = decameron_df["Text"].tolist()

stories_string = ' '.join(stories)

vectorizer = CountVectorizer()

matrix = vectorizer.fit_transform([stories_string])
counts = pd.DataFrame(matrix.toarray(), columns=vectorizer.get_feature_names())

top_n_counts_df = counts.T.sort_values(by=0, ascending=False)

top_n_counts_df.to_csv("/home/cooper/src/decameron/data/csv/vocab-word-freqs.csv")
