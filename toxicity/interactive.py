import joblib
import os

model = input("Enter model name to load: ")
vectorizer = joblib.load(os.path.join("../data/model/", model + "/", "vectorizer.joblib"))
model = joblib.load(os.path.join("../data/model/", model + "/", "model.joblib"))

ip = " "
while ip != "":
    ip = input("Enter text to predict: ")
    if ip == "":
        break
    v = vectorizer.transform([ip])[0][0]
    print(model.pred(v.toarray()[0]))
