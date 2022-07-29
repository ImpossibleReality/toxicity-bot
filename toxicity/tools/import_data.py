# CSIII Group 3
# Johan N.
# Discord Bot, MongoDB, ZMQ Integration, debugging
# Daniel W.
# Model and debugging, hyperparameter tuning
# Rohan D.
# Math (loss and gradient calculations), data collection and manipulation
# Final Project
# Discord bot which detects and removes toxic messages

# Must install two things:
# pip install kaggle
# pip install datasets
from datasets import load_dataset #imports the library with datasets from hugging face
import pandas as pd # dataset manipulation
import kaggle as kg # imports the libarary with datasets from kaggle



print("loading data...")


# The First Dataset, from hugging face
dataset = load_dataset("hate_speech18") # loads dataset

data2 = pd.DataFrame(dataset['train']) # turns dataset into a data frame in pandas (easier to manipulate)

# removes unnecessary columns from the data
data2 = data2.drop('user_id', axis=1) 
data2 = data2.drop('subforum_id', axis=1)
data2 = data2.drop("num_contexts", axis=1)

# changes the name of the column "label" to "class" for consistency with other datasets
data2.rename(columns={"label" : "class"}, inplace=True)







# The second dataset, from kaggle
kg.api.dataset_download_file('mrmorj/hate-speech-and-offensive-language-dataset', file_name='labeled_data.csv',  path='data/') # downloads the requested file into a file inside of data
rawData = pd.read_csv('data/labeled_data.csv.zip', usecols=[5,6]) # gets the data as a csv to be used inside of pandas

data3 = pd.DataFrame(rawData) # turns data into a dataframe

# The classification used by the model is 0 for 'do not ban' and 1 for 'ban', but this dataset uses
# 0 for hate speech, so the numbers in the class column must be changed
data3['class'].replace(2,0, inplace=True)
data3['class'].replace(0,1, inplace=True)

data3.rename(columns={"tweet" : "text"}, inplace=True) # changes column name from tweet to text

        
        
        
    

# The third dataset, from hugging face
dataset = load_dataset("tweets_hate_speech_detection")
data4 = pd.DataFrame(dataset['train']) # turns data into a dataframe

data4.rename(columns={"tweet" : "text"}, inplace=True) # changes column name from tweet to text
data4.rename(columns={"label" : "class"}, inplace=True) # changes column name from label to class






# The fourth dataset, from hugging face
df = datasets.load_dataset('ucberkeley-dlab/measuring-hate-speech', 'binary')   
df = dataset['train'].to_pandas()[['hatespeech','text']] # turns data into a dataframe

# The classification used by the model is 0 for 'do not ban' and 1 for 'ban', but this dataset uses
# 0 for hate speech, so the numbers in the class column must be changed
df['hatespeech'].replace(1,0, inplace=True) 
df['hatespeech'].replace(2,1, inplace=True)

df.rename(columns={"hatespeech" : "class"}, inplace=True) # changes column name from hatespeech to class




#checks data:
print(data2)
print(data3)
print(data4)
print(df)




# Organizes and combines data into three different groups
loose: pd.DataFrame = df[['text', 'class']]
medium: pd.DataFrame = pd.concat([data2[['text', 'class']], data4[['text', 'class']]])
strict: pd.DataFrame = data3[['text', 'class']]

strict = pd.concat([medium[medium['class'] == 0].sample(frac=0.8, random_state=5), strict]) # the strict data was skewed (90% 1s) so some other data was added

# data mixing between the medium super-dataset and the loose dataset
medium = medium.drop(medium[medium['class'] == 0].sample(frac=0.4, random_state=5).index)
medium = pd.concat([medium, loose[loose['class'] == 1].sample(frac=0.4, random_state=5)])

#for the following models (turns all datasets into CSVs to be used in model training) and adds them to a raw datasets folder

#loose: df
loose.to_csv('../../data/datasets/raw/loose.csv', index=False)
#Medium: data2, data4
medium.to_csv('../../data/datasets/raw/moderate.csv', index=False)
#Strict: data3
strict.to_csv('../../data/datasets/raw/strict.csv', index=False)

print("Done.")
