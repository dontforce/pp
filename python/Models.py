from functools import total_ordering
from datetime import datetime

@total_ordering
class User():

    ''' This is a class. Every class has to have a __init__ method that instantiates the object. '''

    ''' The 'self' is required to be in every method a class has. 'self' has to do with referencing this object.

        You instantiate an object by:
            user = User( <any variables this object requires> )

        This object requires you to pass in a user id and screen name for this user.
     '''
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

    # overwrite base object's less than method. (this is for ordering. determines which User object is less than the other)
    # ex: quoc has 500 followers, i have 300. If we have one quoc User object, and one Edmond User object, 
    # and you did print( Edmond < Quoc ), it would = True.
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