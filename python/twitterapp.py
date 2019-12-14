import tweepy
from tweepy import TweepError

from tweepy_api import TweepyHandler
from tweet_utils import createNewUser

from functools import total_ordering
from datetime import datetime




@total_ordering
class User():

    ''' This is a class. Every class has to have a __init__ method that instantiates this object. '''

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



def getTweets( user, max_iterations=2 ):
    ''' This is a method that takes a User object and gets their tweets from the API. 
        the API call can only return 200 tweets at a time. This is why we have a loop to get more than that if we wanted to.

        By default, max_iterations is 2, meaning we get 400 tweets by default. You can pass in 5 to this method and get 1000 tweets.

    '''

    # this is a dictionary/map. it stores key-value pairs. in this case, the key is a string datatype, and the value is a list.
    # we are going to store this user's tweets, retweets in here. 
    tweets = { 'tweets': [ ], 'rts': [ ], 'last_tweet_id': 0 }

    num_calls = 0 # number of times we've called the api
    tweet_count = 0 # number of tweets we've got

    # There's 2 ways to loop through data: for loop and while loop.
    while num_calls < max_iterations:
        kwargs = {}
        kwargs[ 'count' ] = 200
        kwargs[ 'include_rts' ] = True
        kwargs[ 'exclude_replies' ] = True
        
        if max_tweet_id:
            kwargs[ 'max_id' ] = max_tweet_id
        
        # use API to get the tweets for this user.
        tweets_for_user = self.tweepy_handler.user_timeline( user.id_str, **kwargs )

        # iterate over the tweets for this user
        while True:
            tweet = None

            # this is a try/except block. It is used for exception handling. Exception is an error in the code that caused it to fail.
            # try/except block lets you catch these errors from stopping your code, and lets you handle what to do after.
            try:

                # grab next tweet. 
                tweet = tweets_for_user.next()

                # hasattr is a built in function. we are checking to see if this tweet object has that attribute/property.
                # if it does, then this tweet is a retweeted tweet, if not, then it is the User's own tweet.
                if hasattr( tweet, 'retweeted_status' ):
                    # tweets is a dictionary. you access a dictionary using the keys. 
                    # in this case, we're gonna add this tweet to the retweets list.
                    tweets['rts'].append( tweet )
                else:
                    # if the code reached here, then it isn't a retweet, its the user's own tweet. add it to the tweets list.
                    tweets['tweets'].append( tweet )
                
                max_tweet_id = tweet.id_str
                num_tweets_scraped += 1
            except TweepError as e:
                print( e, user.screen_name )
                if 'status code = 503' in e.reason:
                    return None
                continue
            
            except StopIteration:
                break

        num_calls += 1

    return tweets


# the start to any python script has to have this line
if __name__ == "__main__":
    
    # list variable
    quoc = [ 'swae_le' ]

    # API to get twitter data. Don't worry about how this works for now
    tweepyAPI = TweepyHandler( 'auth' )

    # getting quoc's twitter using API 
    quoc = tweepyAPI.user_lookup_screennames( quoc )
    print( "Twitter API gets quoc's twitter and creates a User object. this is what it looks like: {}".format( quoc ) )

    quoc = createNewUser( quoc )
    print( "converted quoc to a simpler object... {}".format( quoc ) )

    print( "Extracting some variables/data from quoc's twitter..." )
    screen_name = quoc.screen_name
    follow_count = quoc.friends_count       # this is how you get a class/object's properties. properties = variables and methods
    follower_count = quoc.followers_count
    bio = quoc.description
    numTweets = quoc.statuses_count
    numFavorites = quoc.favourites_count

    # the \n in a print statement denotes a new line. .format lets you insert variables in order of the {} inside the print statement.
    print( "Quoc's twitter:\nscreen name: {}\nbio: {} \nFollows {} people. \nFollowed by {} people.\nHas tweeted {} times. Has favorited {} tweets"
                .format( screen_name, bio, follow_count, follower_count, numTweets, numFavorites ) )


    print( "Calling a method to get all of quocs tweets" )
    tweets = getTweets( quoc )



