import tweepy
import json
import csv
import sys
import os

def buscador_tweets(consumer_key=None, consumer_secret=None, access_key=None, access_secret=None, nombre_usuario=None):
    
    assert isinstance(consumer_key, str)
    assert isinstance(consumer_secret, str)
    assert isinstance(access_key, str)
    assert isinstance(access_secret, str)
    assert isinstance(nombre_usuario, str) 
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_key, access_secret) 
    api = tweepy.API(auth) 

    all_tweets = [] #contador
    new_tweets = api.user_timeline(screen_name=nombre_usuario, count=200, tweet_mode='extended')
    print("__________Descargando tweets__________")
    while(len(new_tweets) > 0):
        all_tweets.extend(new_tweets)
        last_id = all_tweets[-1].id - 1 #truco
        new_tweets = api.user_timeline(screen_name=nombre_usuario, count=200, max_id=last_id, tweet_mode='extended')
        print("_______ %d tweets descargados ______" % len(all_tweets))
        
    print(" Número máximo posible de tweets descargados ")
    tweet_data = [[  tweet.id_str, str(tweet.created_at).split(' ')[0], tweet.full_text, tweet.retweet_count, 
                    tweet.favorite_count, tweet.lang, tweet.user.id_str, tweet.user.name, tweet.user.screen_name, 
                    tweet.user.followers_count, tweet.user.friends_count, tweet.user.location, 
                    tweet.user.verified ] for tweet in all_tweets]
    return tweet_data
  
def guardar_csv(tweet_data=None, nombre_usuario=None): 

    assert isinstance(tweet_data, list)
    assert all(isinstance(i, list) for i in tweet_data)
    assert isinstance(nombre_usuario, str)

    try:
        with open(os.path.join('data', nombre_usuario + '_tweets.csv'), 'w', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['Tweet ID', 'Date Created', 'Tweet', 'Retweets', 'Favorites', 'Language', 'User ID', 
                            'User Name', 'User Twitter Handle', 'Follower Count', 'Friend Count',
                            'Location', 'Verified'])
            writer.writerows(tweet_data)
        print(' ' + nombre_usuario + '_tweets.csv creado')
        return True
    except:
        return False


if __name__ == '__main__':
    with open('credenciales_twitter.json') as cred_data: #json con las claves 
        login_info = json.load(cred_data)
    consumer_key = login_info['CONSUMER_KEY']
    consumer_secret = login_info['CONSUMER_SECRET']
    access_key = login_info['ACCESS_KEY']
    access_secret = login_info['ACCESS_SECRET']
    nombre_usuario = str(sys.argv[1])

    tweet_data = buscador_tweets(consumer_key=consumer_key, consumer_secret=consumer_secret, access_key=access_key, access_secret=access_secret, nombre_usuario=nombre_usuario)
    if(guardar_csv(tweet_data=tweet_data, nombre_usuario=nombre_usuario)):
        with open('nombre_usuarios.txt') as f:
            if nombre_usuario not in [i.rstrip('\n') for i in f.readlines()]:
                new=True
            else:
                new=False
        if(new):
            with open('nombre_usuarios.txt', 'a') as f: # para ir añadiendo todos los usuarios analizados
                f.writelines(nombre_usuario + '\n')
    else:
        print("Algo ha fallado, no se han podido obtener los tweets del usuario: " + nombre_usuario)
