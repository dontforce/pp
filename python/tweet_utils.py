from langid.langid import LanguageIdentifier, model
from models import User
from datetime import datetime
import re



lang_identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

def tweetWorthScraping( tweet ):
    '''
    Method that determines if a given tweet is worth documenting in the database, based on 3 criterias:
        - tweet > 3 years old and NOT viral
        - tweet > 2 years old and has less than 20 favorites
        - tweet > 0 years old and has less than 5 favorites 

        possibly need to make this relevant to the amount of followers a user has
    '''
    if tweet.lang != 'en' and tweet.lang != 'und':
        return False
    if len( tweet.full_text.split() ) < 7:
        return False
    years_old = 2019 - getYearFromDate(tweet)
    fav_count = tweet.favorite_count
    if hasattr(tweet, "retweeted_status"):
        fav_count = tweet.retweeted_status.favorite_count

    if years_old >= 3 and fav_count > 1000:
        return True
    elif years_old >= 2 and fav_count > 100:
        return True
    elif years_old >= 0 and fav_count > 25:
        return True
    
    return False

def getYearFromDate(tweet):
    try:
        year = tweet.created_at.year
        return year
    except ValueError:
        print("caught number format exception: " + tweet.created_at())
        return -1

def tweetTooOld(tweet):
    years_old = 2019 - getYearFromDate(tweet)
    return years_old >= 3

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


# include another param to indicate whether we want foreigns, regardless of follower count
def userWorthScraping( user ):
    '''
    Method that determines whether or not to document a user.
    '''
    """if checkIfUserExists( user ) or user.statuses_count < 500 or user.protected == True:
        return False"""
    if user.protected == True:
        return False
    if user.followers_count < 1000:
        return False
    if user.lang != 'en' and user.followers_count < 10000:
        return False

    bio_lang = lang_identifier.classify( user.description )

    if bio_lang[ 0 ] != 'en' and user.followers_count < 100000:
        return False
    return True



def createNewUser( user, last_tweet_id=None, last_favorite_id=None ):
    kwargs = {
            'friends_count': user.friends_count,
            'followers_count': user.followers_count,
            'verified': user.verified,
            'description': user.description,
            'location': user.location,
            'protected': user.protected,
            'statuses_count': user.statuses_count,
            'favourites_count': user.favourites_count,
            'last_update': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    if last_tweet_id != None:
        kwargs['last_tweet_id'] = last_tweet_id
        kwargs['last_favorite_id'] = last_favorite_id

    user_model = User(user.id_str, user.screen_name, **kwargs)
    return user_model


def removeUrl( tweet ):
    result = re.sub('http\S+\s*', '', tweet, flags=re.MULTILINE)
    return result

def removeRT( tweet ):
    if tweet.startswith( 'RT' ):
        tweet = re.sub( 'RT ', '', tweet, count=1 )
    return tweet

def cleanTweetForDB( tweet ):
    tweet = removeUrl( tweet )
    tweet = removeRT( tweet )
    return tweet

# remove emojis - 