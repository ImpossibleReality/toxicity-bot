# YOU NEED TO DO THE FOLLOWING BEFORE RUNNING THIS:
# pip install datasets
# pip install kaggle


import pandas as pd
from datasets import load_dataset


from datasets import load_dataset
import pandas as pd


dataset = load_dataset("hate_speech18")

data2 = pd.DataFrame(dataset['train'])
data2 = data2.drop('user_id', axis=1)
data2 = data2.drop('subforum_id', axis=1)
data2 = data2.drop("num_contexts", axis=1)














#print first 5 lines of the data
data2.head()

