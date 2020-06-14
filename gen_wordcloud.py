import pandas as pd
import numpy as np
from textblob import TextBlob
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import sys
import stylecloud


def gen_wordcloud(df=None):
    
    assert isinstance(df, pd.DataFrame)
    
    pos_list = []
    neg_list = []
    
    for i in range(len(df)): 
        if df.loc[i].Polarity > 0: 
            pos_list.extend(df.loc[i]['Tweet_limpio'].split(' ')) 
        elif df.loc[i].Polarity < 0:
            neg_list.extend(df.loc[i]['Tweet_limpio'].split(' '))
            
    pwc = WordCloud(width=1500, height=1000, random_state=21, max_font_size=110, colormap="spring").generate(' '.join([word for word in pos_list]))
    nwc = WordCloud(width=1500, height=1000, random_state=21, max_font_size=110, colormap="cool").generate(' '.join([word for word in neg_list]))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,20))
    ax1.imshow(pwc, interpolation='bilinear')
    ax1.axis('off')
    ax1.set_title('Word Cloud de Tweets Positivos:   ', color='white', fontsize= 25)
    ax2.imshow(nwc, interpolation='bilinear')
    ax2.axis('off')
    ax2.set_title('Word Cloud de Tweets Negativos:', color='white', fontsize= 25)
    fig.patch.set_facecolor('xkcd:black')
    fig.show()
    return

if __name__ == '__main__':
    tweet_df = dict()
    with open('nombre_usuarios.txt') as f:
        polit_list = f.read().rstrip('\n').split('\n')
    for i in polit_list:
        tweet_df[i] = pd.read_csv(i + '_tweets.csv')
    gen_wordcloud(tweet_df[str(sys.argv[1])])