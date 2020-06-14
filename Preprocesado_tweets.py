from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import pandas as pd
import numpy as np
from time import sleep
import os
import nltk

def traducir_tweets(df=None):
    
    assert isinstance(df, pd.DataFrame)

    try:
        for i in range(len(df)):
            if(df.loc[i].Language == 'es'):
                df.at[i, 'Tweet_limpio'] = df.loc[i].Tweet
            else:
                continue
                print(i)
                temp = blob(df['Tweet'][i])
                df.at[i, 'Tweet_limpio'] = temp.translate(to='es')  #API Google
                sleep(5)
        return True
    except Exception as e:
        print("Error al traducir en " + str(i) + " : " +str(e))
        return False

    
def solo_español(df=None):
    
    assert isinstance(df, pd.DataFrame)

    for entry in range(len(df)):
        if df['Language'][entry] != 'es':
            df = df.drop([entry])
    df.reset_index(inplace=True)
    return df


def eliminar_menciones(tweet=None):                                      
    
    assert isinstance(tweet, str)

    r = re.findall('@[\w]*', tweet)
    for i in r:                         
        tweet = re.sub(i, '', tweet)
    return tweet


def limpieza_texto(df=None, min_len=None):

    assert isinstance(df, pd.DataFrame)
    assert isinstance(min_len, int)
    assert min_len > 2 # palabras con menos de 2 letras en español no tienen significado

    df['Tweet_limpio'] = df['Tweet_limpio'].str.lower()
    df['Tweet_limpio'] = df['Tweet_limpio'].str.replace("https?://[A-Za-z0-9./]+","")
    df['Tweet_limpio'] = df['Tweet_limpio'].str.replace("http?://[A-Za-z0-9./]+","")
    df['Tweet_limpio'] = df['Tweet_limpio'].str.replace("[\.\,\!\¡\¿\?\:\;\-\=\"\'\$\%\&\()\*\+\<\>\[\\]\[\]\^\_\´\{\}\|\~\'#\(\)]", "")
    df['Tweet_limpio'] = df['Tweet_limpio'].str.replace("\d+", "") # nº 
    df['Tweet_limpio'] = df['Tweet_limpio'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>min_len]))
    df['Tweet_limpio'] = df['Tweet_limpio'].apply(lambda x : ' '.join([tweet for tweet in x.split()if not tweet.startswith("@")]))
    return


def limpiar_stopwords(texto):
    tokens = re.split('\W+', texto) 
    texto = [i for i in tokens if i not in stopwords] 
    texto = " ".join([i for i in texto])
    return texto


def analiza_sentimiento(Tweet_limpio=None):

    assert isinstance(Tweet_limpio, str)

    analyzer = SentimentIntensityAnalyzer()
    blob = TextBlob(Tweet_limpio)
    polarity, subjectivity = blob.sentiment
    if polarity == 0:
        vader_op = analyzer.polarity_scores(Tweet_limpio)
        polarity = vader_op['compound']
    return polarity, subjectivity


if __name__ == '__main__':
    
    remove_other_langs = True
    tweet_df = dict()
    
    with open('nombre_usuarios.txt') as f:
        polit_list = f.read().rstrip('\n').split('\n')
        
    for i in polit_list:
        tweet_df[i] = pd.read_csv('data/' + i + '_tweets.csv')
        if 'Tweet_limpio' in tweet_df[i].columns:
            continue
        tweet_df[i].insert(3, 'Tweet_limpio', None)
        tweet_df[i].insert(4, 'Polarity', None)
        tweet_df[i].insert(5, 'Subjectivity', None)

        print('Preprocesando tweets de ' + str(i))
        
        if(remove_other_langs == True):
            #filter out tweets that are not english
            tweet_df[i] = solo_español(tweet_df[i])
        else:
            #translate tweets
            if not traducir_tweets(tweet_df[i]):
                print("Error al traducir")
        
        #limpieza menciones
        tweet_df[i]['Tweet_limpio'] = np.vectorize(eliminar_menciones)(tweet_df[i]['Tweet'])

        #limmpieza del texto 
        limpieza_texto(tweet_df[i], 3)
        
        #limpieza stopwords
        stopwords = nltk.corpus.stopwords.words('spanish')
        tweet_df[i]['Tweet_limpio'] = np.vectorize(limpiar_stopwords)(tweet_df[i]['Tweet_limpio'])

        print('Calculando el score del sentimiento de ' + str(i))
        
        #Polaridad y sujbetividad
        tweet_df[i]['Polarity'], tweet_df[i]['Subjectivity'] = np.vectorize(analiza_sentimiento)(tweet_df[i]['Tweet_limpio'])

        print('Actualizando csv de ' + str(i))
        os.remove('data/' + str(i) + '_tweets.csv')
        tweet_df[i].to_csv('data/' + str(i) + '_tweets.csv', index=False, mode='w+', line_terminator='\n')
        print('Csv actualizado: ' + str(i) + '_tweets.csv')
