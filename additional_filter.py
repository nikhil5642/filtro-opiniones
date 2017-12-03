from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string 
import pandas as pd
import numpy as np

exclude= set(string.punctuation)
exclude.remove('.')
exclude.remove(',')
def last_filter(sentence):
    try:
          sentence=list(sentence)
          answer=''.join(s for s in sentence if s not in exclude)
    except Exception:
          print('err')
          return
    return answer

def remove_duplicates(sentences,score):
    df=pd.DataFrame()
    df['sent']=sentences
    df['score']=score
    pz=df.sort_values('score')
    #pz=pz.set_index('score')
    final=pz.drop_duplicates(subset=None, keep='first', inplace=False)

    return np.array(final['sent']),np.array(final['score'])
