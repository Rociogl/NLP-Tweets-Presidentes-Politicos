import pandas as pd
from collections import defaultdict
import csv
import matplotlib.pyplot as plt

def average_tweets(nombre_usuarios=None,politico=None):
    
    assert isinstance(nombre_usuarios, list)
    assert isinstance(politico, list)
    
    media_tweet=defaultdict(float)
    
    for p in range(len(politico)):
        
        por_dia=defaultdict(int)
        
        data=pd.read_csv('data/' + nombre_usuarios[p])
        
        date=data['Date Created']
        
        for d in date:
            por_dia[d]+=1
        media=sum(por_dia.values())/len(por_dia.keys())
        media_tweet[politico[p]]=media
        
    key=list(media_tweet.keys())
    plt.bar(key, media_tweet.values(), color='#72CCD4')
    plt.xticks(key, rotation='30', fontsize= 12)
    plt.ylabel('Número medio de tweets publicados por día', fontsize= 15)
    plt.tight_layout()
    plt.grid(color='k', linestyle='--', linewidth=0.2)
    plt.show()
    plt.rcParams['figure.figsize']=(50,50)
    return

if __name__ == '__main__':
    nombre_usuarios=['pablocasado__tweets.csv','santi_ABASCAL_tweets.csv','sanchezcastejon_tweets.csv','PabloIglesias_tweets.csv','InesArrimadas_tweets.csv']
    politico=['Pablo Casado','Santiago Abascal','Pedro Sanchez','Pablo Iglesias','Ines Arrimadas']
    
    average_tweets(nombre_usuarios,politico)