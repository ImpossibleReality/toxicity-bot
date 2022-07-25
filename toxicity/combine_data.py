import pandas as pd
import datasets

hs_dataset = datasets.load_dataset('ucberkeley-dlab/measuring-hate-speech', 'binary')
hs = hs_dataset['train'].to_pandas()

hs = hs[['text', 'hate_speech_score']]
hs['class'] = hs['hate_speech_score'].apply(lambda x: 0 if x < 0 else 1)
hs = hs.drop(['hate_speech_score'], axis=1)

raw_labeled_data = pd.read_csv('../data/labeled-data.csv')
raw_discord_data = pd.read_csv('../data/discord-data.csv')

data = pd.DataFrame()

data['class'] = raw_labeled_data['class'].apply(lambda x: 0 if x == 2 else 1)

data = pd.concat([data, raw_discord_data, hs])

data.to_csv('../data/raw_data.csv', index=False)

