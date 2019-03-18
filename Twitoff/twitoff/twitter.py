"""Retrieve TWeets, embeddings, and persist in the database."""
import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

def fetch(username):
    twitter_user = TWITTER.get_user(username)
    db_user = User.query.get(twitter_user.id)
    twitter_tweets = twitter_user.timeline(
        count=200, exclude_replies=True, include_rts=False,
        tweet_mode='extended', since_id=db_user.newest_tweet_id)
    db_tweets = db_user.tweets
    return twitter_tweets, db_tweets

def add_or_update_user(username):
    """Add or update a user *and* their Tweets, error if no/private user."""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=twitter_user.screen_name))
        # We want as many recent non-retweet/reply statuses as we can get
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        DB.session.add(db_user)

        for tweet in tweets:
            # Get embedding for tweet, and store in db
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')
            db_tweet = Tweet(id=tweet.id, created_at=tweet.created_at, full_text=tweet.full_text[:500],
                             embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()
        return twitter_user
