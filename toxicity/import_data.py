# Must install two things:
# pip install kaggle
# pip install datasets
import datasets
from datasets import load_dataset
import pandas as pd
import kaggle as kg







dataset = load_dataset("hate_speech18")

data2 = pd.DataFrame(dataset['train'])
data2 = data2.drop('user_id', axis=1)
data2 = data2.drop('subforum_id', axis=1)
data2 = data2.drop("num_contexts", axis=1)

data2.rename(columns={"label" : "class"}, inplace=True)








kg.api.dataset_download_file('mrmorj/hate-speech-and-offensive-language-dataset', file_name='labeled_data.csv',  path='data/')
rawData = pd.read_csv('data/labeled_data.csv.zip', usecols=[5,6])

data3 = pd.DataFrame(rawData)

for i in enumerate(data3["class"]):
    if i==2:
        data3['class'].replace(i, 0, inplace=True)
    else:
        data3['class'].replace(i, 1, inplace=True)

data3.rename(columns={"tweet" : "text"}, inplace=True)







dataset = load_dataset("tweets_hate_speech_detection")
data4 = pd.DataFrame(dataset['train'])

data4.rename(columns={"tweet" : "text"}, inplace=True)
data4.rename(columns={"label" : "class"}, inplace=True)







dataset = datasets.load_dataset('ucberkeley-dlab/measuring-hate-speech', 'binary')
df = dataset['train'].to_pandas()[['hatespeech','text']]

df['hatespeech'].replace(1,0, inplace=True)
df['hatespeech'].replace(2,1, inplace=True)

df.rename(columns={"hatespeech" : "class"}, inplace=True)

loose: pd.DataFrame = df[['text', 'class']]
medium: pd.DataFrame = pd.concat([data2[['text', 'class']], data4[['text', 'class']]])
strict: pd.DataFrame = data3[['text', 'class']]

strict = pd.concat([medium[medium['class'] == 0].sample(frac=0.8, random_state=5), strict])

medium = medium.drop(medium[medium['class'] == 0].sample(frac=0.4, random_state=5).index)
medium = pd.concat([medium, loose[loose['class'] == 1].sample(frac=0.4, random_state=5)])

#for the following models

#loose: df
loose.to_csv('../data/datasets/raw/loose.csv', index=False)
#Medium: data2, data4
medium.to_csv('../data/datasets/raw/moderate.csv', index=False)
#Strict: data3
strict.to_csv('../data/datasets/raw/strict.csv', index=False)