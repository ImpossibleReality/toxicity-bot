import numpy as np
import joblib
from constants import MODEL_PATH, VECTORIZER_PATH

vectorizer = joblib.load(VECTORIZER_PATH)
model = joblib.load(MODEL_PATH)


def _get_probability_from_pred(prob):
    return prob[1]


def predict(texts):
    return model.predict(vectorizer.transform(texts))


def predict_prob(texts):
    return np.apply_along_axis(_get_probability_from_pred, 1, model.predict_proba(vectorizer.transform(texts)))
