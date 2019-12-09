import tweepy
from tweepy import TweepError

from tweepy_api import TweepyHandler
from tweet_utils import createNewUser

from functools import total_ordering
from datetime import datetime

@total_ordering
class User():

    def __init__(self, user_id, screen_name, **kwargs):
        self.id_str = user_id
        self.screen_name = screen_name
        self.friends_count = kwargs.get('friends_count', None)
        self.followers_count = kwargs.get('followers_count', None)
        self.verified = kwargs.get('verified', False)
        self.description = kwargs.get('description', "")
        self.last_tweet_id = kwargs.get('last_tweet_id', None)
        self.last_favorite_id = kwargs.get('last_favorite_id', None)
        self.location = kwargs.get('location', 'None')
        self.statuses_count = kwargs.get('statuses_count', None)
        self.favourites_count = kwargs.get('favourites_count', None)
        self.protected = kwargs.get('protected', False)
        self.last_updated = kwargs.get('last_update', datetime.now().strftime("%Y-%m-%d %H:%M:%S") )

    # overwrite less than method
    def __lt__(self, other):
        return self.followers_count < other.followers_count

    # overwrite base object's toString method
    def __str__(self):
        return "id: {}, screenname: {}, followers_count: {}".format(self.id_str, self.screen_name, self.followers_count)

    def setLastUpdated(self, last_update):
        self.last_updated = last_update
    
    def setLastTweetID(self, last_tweet_id):
        self.last_tweet_id = last_tweet_id

    def setLastFavoriteID(self, last_fav_id):
        self.last_favorite_id = last_fav_id




# the start to any python script has to have this line
if __name__ == "__main__":
    
    # list variable
    quoc = [ 'swae_le' ]

    # API to get twitter data
    tweepyAPI = TweepyHandler( 'auth' )

    # getting quoc's twitter using API 
    quoc = tweepyAPI.user_lookup_screennames( quoc )

    # Twitter API gets quoc's twitter and creates a User object. this is what it looks like:
    print( quoc )

    # convert to a simpler object 
    quoc = createNewUser( quoc )
    

