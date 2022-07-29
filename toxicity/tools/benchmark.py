import timeit

import joblib
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

sensitivities = ['loose', 'moderate', 'strict']

BENCHMARK_XES = 100
BENCHMARK_INDIVIDUAL = 1000

for s in sensitivities:
    print("Loading data for: " + s)
    data = pd.read_csv(os.path.join("../../data/datasets/cleaned/", s + ".csv"))
    _, test = train_test_split(data, test_size=0.2, random_state=5)

    test_x = test['text'].astype(str).to_numpy()
    test_y = test['class']

    print("Loading model for: " + s)
    vectorizer = joblib.load(os.path.join("../../data/model/", s + "/", "vectorizer.joblib"))
    model = joblib.load(os.path.join("../../data/model/", s + "/", "model.joblib"))

    res = 0
    for i in range(BENCHMARK_XES):
        x = test_x[np.random.randint(0, test_x.shape[0])]


        def run():
            v = vectorizer.transform([x])[0][0]
            model.pred(v.toarray()[0])

        res += timeit.timeit(run, number=BENCHMARK_INDIVIDUAL)
    print("{} takes about {} seconds per prediction ({}s per {}).".format(s, res / BENCHMARK_XES, res, BENCHMARK_XES))