import tweepy
import os


def get_twitter_client(logger):
    logger.info('getting twitter client')
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    logger.info('twitter client retrieved')

    return client


def tweet_collage(logger, collage_path, caption):
    logger.info('tweeting collage')

    credentials = get_twitter_credentials(logger)
    api = twitter_login(logger, credentials)

    api.update_with_media(collage_path, status=caption)

    logger.info('collage tweeted')


def tweet_caption(logger, client, caption):
    logger.info('tweeting caption')

    response = client.create_tweet(
        text=caption
    )

    tweet_id = response.data['id']
    logger.info('text tweeted: https://twitter.com/user/status/' + tweet_id)


def get_twitter_credentials(logger):
    logger.info('getting twitter credentials')

    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    credentials = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'access_token': access_token,
        'access_token_secret': access_token_secret
    }

    logger.info('twitter credentials retrieved')

    return credentials


def twitter_login(logger, credentials):
    logger.info('logging in twitter')

    auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
    auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    logger.info('logged in twitter')

    return api
