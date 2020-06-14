from plotly.offline import plot,iplot
import plotly_express as px
import pandas as pd

class plot_engagement:

    def __init__(self,tweet_df=None,name=None):

        assert isinstance(tweet_df,dict), "Diccionario"
        assert isinstance(name,str), "Nombre usuario"
        if not name in tweet_df: raise ValueError("Ese nombre no existe en el dataset ")
        assert len(name)>0, "Caracter vacío"
        assert len(tweet_df)>0, "Dataframe vacío"
        for val in tweet_df: assert isinstance(tweet_df[val],pd.DataFrame), "Valores en el diccionario"

        self.tweet_df = tweet_df
        self.name = name
        self.this_person = self.tweet_df[self.name]
        self.real_name = self.this_person['User Name'][0]
        self.friend_count = self.this_person['Friend Count']
        self.length = max(self.this_person.index)

        self.polarity = self.this_person['Polarity']
        self.favorite = self.this_person['Favorites']
        self.retweets = self.this_person['Retweets']
        self.subjectivity = self.this_person['Subjectivity']
        self.this_person['yr-month'] = pd.to_datetime((self.this_person['Date Created'])).dt.strftime('%Y-%b %A') #formato date
        self.daily = self.this_person.groupby('yr-month')

    def __repr__(self): #Localización
        return "plot_engagement Dirección "+hex(id(self))

    def calc_engagement(self): # score engagement: retweets + favoritos
        self.this_person['Engagement'] = ((2*self.this_person['Retweets'] + self.this_person['Favorites'])**2)
        return

    def create_plotly_df(self):
        self.calc_engagement()
        max_locs = self.this_person.groupby('Date Created')['Engagement'].idxmax()

        #plotly 
        plot_df = pd.DataFrame(pd.Series(self.this_person.loc[max_locs]['Date Created'],name="Date"))
        plot_df['Retweets'] = self.this_person.loc[max_locs]['Retweets']
        plot_df['Favorites'] = self.this_person.loc[max_locs]['Favorites']
        plot_df['Engagement'] = self.this_person.loc[max_locs]['Engagement']
        plot_df['Polarity'] = self.this_person.loc[max_locs]['Polarity']
        plot_df['Subjectivity'] = self.this_person.loc[max_locs]['Subjectivity']
        plot_df['Tweet'] = self.this_person.loc[max_locs]['Tweet']

        formatted = []
        for tweet in self.this_person['Tweet']:
            temp = self.format_hovertext(tweet,10)
            formatted.append(temp)
        self.this_person['Formatted Tweet'] = pd.DataFrame(formatted)
        plot_df['Formatted Tweet'] = self.this_person.loc[max_locs]['Formatted Tweet']
        return plot_df

    def bubble_chart(self):
        plot_df = self.create_plotly_df()
        p1 = px.scatter(plot_df,x="Date", y="Polarity",
                    size='Engagement',hover_data=["Formatted Tweet","Retweets","Favorites"],
                    opacity=.95,size_max=70,title=self.real_name+' - Engagement vs. Polarity',
                    color="Polarity",labels=({"Formatted Tweet":"Tweet"}),
                    color_continuous_scale=['red','rgb(220,220,220)','rgb(0,191,255)'])
        plot(p1)
        return

    def format_hovertext(self,string=None,n=None): #text
        assert isinstance(string, str)
        assert isinstance(n, int)
        assert n > 0
        split=string.split()
        i=1
        result = ''
        while (i * n) < len(split):
            result = result +' '.join(split[(i-1)*n:i *n]) + '<br>'
            i+=1
        result +=' '.join(split[(i-1)*n:])

        return result


if __name__ == '__main__':

    tweet_df=dict()
    with open('nombre_usuarios.txt') as f:
        polit_list = f.read().rstrip('\n').split('\n')
    for i in polit_list:
        tweet_df[i] = pd.read_csv(i + '_tweets.csv')
