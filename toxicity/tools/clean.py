import pandas as pd
from tqdm import tqdm
from constants import REPLACEMENTS_PATH
import re
import os

replacements = []

replacement_words = pd.read_csv(REPLACEMENTS_PATH)
for i, x in replacement_words.iterrows():
    if x['initial'] == '#':
        continue
    if x['regex'] == '1':
        r = x['initial']
        if x['isword'] == '1':
            r = '\\b' + r + '\\b'
        r = "\\s*".join(r.split())
        replacements.append([r, x['replacement'], x['isword']])
    else:
        r = re.escape(x['initial'])
        if x['isword'] == '1':
            r = '\\b' + x['initial'] + '\\b'
        r = "\\s*".join(r.split())

        replacements.append([r, x['replacement'], x['isword']])


def twitter_clean(text):
    # Twitter-specific cleaning (should NOT be used for Discord input)

    text = re.sub(r'@\S+', 'you', text)
    text = re.sub(r'&#\d+;', '', text)
    text = re.sub(r'#\S+', '', text)

    return clean_text(text)

def clean_text(text):
    # Standardize text (can be used for Discord input)
    text = str(text).lower()

    # Remove URLs
    text = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9('
                  r')@:%_\+.~#?&//=]*)', '', text)

    # Replace discord mentions with the word 'you'
    text = re.sub(r'<@!?\d+>', 'you', text)

    # use replacements file
    for r in replacements:
        if r[2] == '1':
            text = re.sub(r[0], r[1], " " + text + " ")
        else:
            text = re.sub(r[0], r[1], text)

    # Remove all non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Replace common contractions with full words
    text = re.sub(r'\bdon ?t\b', 'do not', text)
    text = re.sub(r'\bdoesn ?t\b', 'does not', text)
    text = re.sub(r'\bhadn ?t\b', 'had not', text)
    text = re.sub(r'\bcouldn ?t\b', 'could not', text)
    text = re.sub(r'\bdidn ?t\b', 'did not', text)
    text = re.sub(r'\bcan ?t\b', 'cannot', text)
    text = re.sub(r'\bain ?t\b', 'is not', text)
    text = re.sub(r'\bwouldn ?t\b', 'would not', text)
    text = re.sub(r'\by ?all\b', 'you all', text)
    text = re.sub(r'\bi ?m\b', 'i am', text)
    text = re.sub(r'\bi ?ve\b', 'i have', text)
    text = re.sub(r'\bi d\b', 'i would', text)
    text = re.sub(r'\bhe ?s\b', 'he is', text)
    text = re.sub(r'\bshe ?s\b', 'she is', text)
    text = re.sub(r'\bit ?s\b', 'it is', text)
    text = re.sub(r'\bthat ?s\b', 'that is', text)
    text = re.sub(r'\bwe re\b', 'we are', text)
    text = re.sub(r'\byou ?re\b', 'you are', text)
    text = re.sub(r'\bwe d\b', 'we would', text)
    text = re.sub(r'\bthinkin\b', 'thinking', text)
    text = re.sub(r' ll ', ' will ', text)

    # Numbers and Dates
    text = re.sub(r'\bth\b', '', text)
    text = re.sub(r'\bst\b', '', text)
    text = re.sub(r'\bnd\b', '', text)
    text = re.sub(r'\brd\b', '', text)

    # Reply tweet remove
    text = re.sub(r'rtyou', 'you', text)
    text = re.sub(r'\brt\b', ' ', text)

    # Extra mentions
    text = re.sub(r'(you ?)+', ' you ', text)

    # Remove all extra whitespace characters
    text = re.sub(r'\s+', ' ', text)

    return text

if __name__ == '__main__':
    tqdm.pandas()
    for f in os.listdir('../../data/datasets/raw/'):
        print("Cleaning " + f + "...")
        data = pd.read_csv(os.path.join('../../data/datasets/raw/', f))

        # Remove all entries with empty text fields
        data = data[data['text'].apply(lambda x: len(str(x)) > 0)]

        # Remove all entries with text fields of 'nan'
        data = data[data['text'].apply(lambda x: str(x) != 'nan')]

        data['text'] = data['text'].progress_apply(lambda x: twitter_clean(str(x)))

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
