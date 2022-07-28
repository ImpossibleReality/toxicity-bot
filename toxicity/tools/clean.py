import sys

sys.path.append("../..")

import pandas as pd
from tqdm import tqdm
from toxicity import dataset_clean
import os

if __name__ == '__main__':
    tqdm.pandas()
    for f in os.listdir('../../data/datasets/raw/'):
        print("Cleaning " + f + "...")
        data = pd.read_csv(os.path.join('../../data/datasets/raw/', f))

        # Remove all entries with empty text fields
        data = data[data['text'].apply(lambda x: len(str(x)) > 0)]

        # Remove all entries with text fields of 'nan'
        data = data[data['text'].apply(lambda x: str(x) != 'nan')]

        data['text'] = data['text'].progress_apply(lambda x: dataset_clean(str(x)))

        data.to_csv(os.path.join('../../data/datasets/cleaned/', f), index=False)

        print('Data summary for ' + f)
        # Print number of offensive and non offensive datapoints
        # Class 0 is non-offensive, class 1 is offensive
        print('Offensive:', data[data['class'] == 1].shape[0],
              "(" + str(round(data[data['class'] == 1].shape[0] / data.shape[0] * 100, 2)) + "%)")
        print('Non-offensive:', data[data['class'] == 0].shape[0],
              "(" + str(round(data[data['class'] == 0].shape[0] / data.shape[0] * 100, 2)) + "%)")
        print('Total:', data.shape[0])
        print('\n--------\n')
