# YOU NEED TO DO THE FOLLOWING BEFORE RUNNING THIS:
# pip install datasets
# pip install kaggle


import pandas as pd
from datasets import load_dataset


dataset = load_dataset("hate_speech18")
huggingFaceData1 = pd.read_csv(dataset, usecols=[0,4])


kaggleData2 = pd.read_excel("data/labeled_data.xls",sheetname="labeled_data",usecols=[5,6])

for i in df.iterrows():
  identifierColumn = pd.DataFrame(kaggleData2, index












#print first 5 lines of the data
huggingFaceData1.head()

