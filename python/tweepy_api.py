import tweepy
from configparser import ConfigParser  

class TweepyHandler():

    def __init__(self, config_section):
        self.api = self.connectToTwitter( config_section )

    def user_timeline(self, user_id, **kwargs):
        '''
        Fetches all tweets/retweets of a given user. 
        '''
        count = kwargs.get('count', 200)
        include_rts = kwargs.get('include_rts', True)
        max_tweet_id = kwargs.get('max_tweet_id', None)
        exclude_replies = kwargs.get('exclude_replies', True)
        return tweepy.Cursor( self.api.user_timeline, user_id=user_id, 
                                count=count, include_rts=include_rts, max_id=max_tweet_id, 
                                tweet_mode='extended', exclude_replies=exclude_replies ).items(200)

    def favorites(self, user_id, **kwargs):
        '''
        Gets all favorited tweets for specified user_id and returns it as a list.
        '''
        count = kwargs.get('count', 200)
        max_fav_id = kwargs.get('max_favorite_id', None)
        return tweepy.Cursor( self.api.favorites, user_id=user_id, count=count, max_id=max_fav_id, tweet_mode='extended' ).items( 200 )


    def friends(self, user_id, **kwargs):
        if user_id == None:
            user_id = self.api.me().id_str
        count = kwargs.get('count', 200)
        try:
            return tweepy.Cursor( self.api.friends, user_id=user_id, count=count ).items()
        except tweepy.TweepError:
            print("tweepy error: friends rate limit reached")
            return None

    def friends_ids(self, user_id, **kwargs):
        '''
            Gets all user_ids this account is following, up to 5000 count per request.
            If user has more than 5000, save 'next_cursor_str' for that user (in a dict), and 
            call this method again with cursor set to 'next_cursor_str'.
        '''
        count = kwargs.get('count', 5000)
        return tweepy.Cursor(self.api.friends_ids, user_id=user_id, count=count).items( 5000 )

    def home_timeline( self, **kwargs ):

        since_id = kwargs.get( 'since_id', None )
        max_id = kwargs.get( 'max_id', None )
        count = kwargs.get( 'count', 200 )
        return tweepy.Cursor( self.api.home_timeline, since_id=since_id, max_id=max_id, count=count, tweet_mode='extended' ).items( count )


    def user_lookup(self, users):
        try:
            result = self.api.lookup_users(user_ids=users)
            return result
        except tweepy.TweepError as e:
            print(e)
            return None

    def user_lookup_screennames( self, users ):
        try:
            result = self.api.lookup_users(screen_names=users)
            return result
        except tweepy.TweepError as e:
            print(e)
            return None
        
    def checkRateLimit(self, resources, call):
        path = ''
        try:
            path = '/{}/{}'.format(resources, call)
            return self.api.rate_limit_status(resources=resources)['resources'][resources][path]
        except tweepy.TweepError:
            print("tweepy error: rate_limit_status rate limit exceeded")
            return None

    def retrieveTweetById( self, ids ):
        return self.api.statuses_lookup( ids )

    def connectToTwitter( self, config_section ):
        config = ConfigParser()
        config.read('config/config.ini')
        
        if config.has_section( config_section ):
            consumer_key                = config.get( config_section, 'consumer-key')
            secret_consumer_key         = config.get( config_section, 'secret-consumer-key')
            access_token                = config.get( config_section, 'access-token')
            secret_access_token         = config.get( config_section, 'secret-access-token')
            auth                        = tweepy.OAuthHandler( consumer_key, secret_consumer_key )
            auth.set_access_token(access_token, secret_access_token)
            return tweepy.API( auth, wait_on_rate_limit=True )
        else:
            raise Exception("Config file has no section {}. Could not connect to API".format( config_section ) )

    