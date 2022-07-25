import os

# Constants for file paths

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(ROOT_DIR, 'data/model/model.joblib')
VECTORIZER_PATH = os.path.join(ROOT_DIR, 'data/model/vectorizer.joblib')

REPLACEMENTS_PATH = os.path.join(ROOT_DIR, 'data/replacements.csv')