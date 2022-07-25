import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
import joblib

data = pd.read_csv('../data/cleaned_data.csv')
texts = data['text'].astype(str)
y = data['class']

# Bag Of Words Model
# (https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)
count_vectorizer = CountVectorizer(stop_words='english', min_df=0.0001)
x = count_vectorizer.fit_transform(texts)

# Train the model using linear SVC
# I looked at the scikit documentation and it seems to be the
# best option for fast nlp classification.
model = LinearSVC(class_weight="balanced", dual=False, tol=1e-2, max_iter=1e5)

# This allows us to get the probabilities of each class instead of just the class
# According to the documentation, this is the best way to calibrate the probabilities for SVC
# https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibratedClassifierCV.html
cclf = CalibratedClassifierCV(base_estimator=model)
cclf.fit(x, y)

# Save the model using joblib
# It has the benefit of being able to use joblib with scikit-learn models
# Unlike normal pickles.
joblib.dump(count_vectorizer, '../data/model/vectorizer.joblib')
joblib.dump(cclf, '../data/model/model.joblib')