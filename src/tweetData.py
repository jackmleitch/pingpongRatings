import tweepy
import pandas as pd
import config 
import io

df = pd.read_csv(config.PLAYERS_FILEPATH, index_col=0)
textRankings = df.to_csv(sep=' ', index=True, header=True)

class connectTwitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(config.TWITTER_KEYS['consumer_key'], config.TWITTER_KEYS['consumer_secret'])
        self.auth.set_access_token(config.TWITTER_KEYS['access_token_key'], config.TWITTER_KEYS['access_token_secret'])    
        self.client = tweepy.API(self.auth)
        self.clientId = self.client.me().id

    def updateRankings(self, rankings):
        self.client.update_status(status = rankings)

    def fetchRankings(self):
        tweet = self.client.user_timeline(self.clientId, count = 1)[0]
        data = io.StringIO(tweet.text)
        df = pd.read_csv(data, sep=" ")
        return df


twitter = connectTwitter()
twitter.updateRankings(textRankings)
df = twitter.fetchRankings()
print(df)
    