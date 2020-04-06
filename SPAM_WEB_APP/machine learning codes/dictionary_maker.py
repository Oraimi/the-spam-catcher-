import pandas as pd
import nltk
import string
import pickle
from nltk.corpus import stopwords
from tqdm import tqdm

nltk.download('stopwords')


def mapper(txt):
  return [word for word in ''.join([char for char in txt if char not in string.punctuation]).split() if word.lower() not in stopwords.words('english')]


def index_words():
    keeper = set()
    df = pd.read_csv('machintosh HD//users//Aya_al3rimi//Downloads//emails.csv')
    for index, row in tqdm(df.iterrows()):
        for i in mapper(row.text):
            keeper.add(i)
    keeper = list(keeper)
    pickle.dump(keeper, open('dict', 'wb'))


if __name__ == '__main__':
    index_words()
