import tweepy
from tweepy import TweepError

from tweepy_api import TweepyHandler
from tweet_utils import createNewUser


from datetime import datetime




def getTweets( tweepyAPI, user, max_iterations=2 ):
    ''' This is a method that takes a User object and gets their tweets from the API. 
        the API call can only return 200 tweets at a time. This is why we have a loop to get more than that if we wanted to.

        By default, max_iterations is 2, meaning we get 400 tweets by default. You can pass in 5 to this method and get 1000 tweets.

    '''

    # this is a dictionary/map. it stores key-value pairs. in this case, the key is a string datatype, and the value is a list.
    # we are going to store this user's tweets, retweets in here. 
    tweets = { 'tweets': [ ], 'rts': [ ], 'last_tweet_id': 0 } # notice how the dictionary can store multiple types (2 lists, and 1 int). cannot do this in java

    num_calls = 0 # number of times we've called the api
    tweet_count = 0 # number of tweets we've got

    kwargs = {}
    kwargs[ 'count' ] = 200
    kwargs[ 'include_rts' ] = True
    kwargs[ 'exclude_replies' ] = True
    max_tweet_id = user.last_tweet_id
    num_tweets_scraped = 0


    # There's 2 ways to loop through data: for loop and while loop.
    while num_calls < max_iterations:
        
        if max_tweet_id:
            kwargs[ 'max_id' ] = max_tweet_id
        
        # use API to get the tweets for this user.
        tweets_for_user = tweepyAPI.user_timeline( user.id_str, **kwargs )

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
                    # tweets is a dictionary. you access a dictionary using the keys. in this case, we're gonna add this tweet to the retweets list.
                    tweets['rts'].append( tweet )
                else:
                    # if the code reached here, then it isn't a retweet, its the user's own tweet. add it to the tweets list.
                    tweets['tweets'].append( tweet )
                
                max_tweet_id = tweet.id_str
                num_tweets_scraped += 1
            except TweepError as e:
                print( e, user.screen_name ) # print the error message and which user it was that caused the error. 
                if 'status code = 503' in e.reason:
                    return None
                continue
            
            # can catch multiple exceptions. this lets you handle different errors in different ways. this exception is used to catch StopIteration exception.
            except StopIteration:
                break # when we reach the end of all the user's tweets, we `break` out the loop. break is typically used to exit loops on a certain condition.

        num_calls += 1

    return tweets


# the start to any python script has to have this line
if __name__ == "__main__":
    
    # list variable
    quoc = [ 'swae_le' ]

    # API to get twitter data. Don't worry about how this works for now
    tweepyAPI = TweepyHandler( 'auth' )

    # getting quoc's twitter using API 
    quoc = tweepyAPI.user_lookup_screennames( quoc )[ 0 ] # this returns a List object. grab the first user from the list by doing [ 0 ]
    print( "Twitter API gets quoc's twitter and creates a User object. this is what it looks like:\n{}".format( quoc ) )
    
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
    tweets = getTweets( tweepyAPI, quoc )

    for idx, tweet in enumerate( tweets['rts'], 0 ):
        if idx < 5:
            print( "tweet: {}".format( tweet ) )



