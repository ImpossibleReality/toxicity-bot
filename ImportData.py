# YOU NEED TO DO THE FOLLOWING BEFORE RUNNING THIS:
# pip install datasets
# pip install kaggle


import pandas as pd
from datasets import load_dataset


dataset = load_dataset("hate_speech18")
huggingFaceData1 = pd.read_csv(dataset, usecols=[0,4])





kagglaData1 = pd.read_csv("https://www.kaggle.com/datasets/mrmorj/hate-speech-and-offensive-language-dataset/












#print first 5 lines of the data
huggingFaceData1.head()

