# imports
import os

import tumblr_utils
import utils
import lastfm_utils
import image_utils
import twitter_utils
import instagram_utils

from dotenv import load_dotenv
load_dotenv()


# get logger
logger = utils.get_logger()
logger.info('metal-friday started')

# get weekly charts
lfm = lastfm_utils.lastfm_login(logger)
weekly_charts = lastfm_utils.get_weekly_charts(logger, lfm)

# get complete album list
album_list = lastfm_utils.get_complete_album_list(logger, lfm, weekly_charts)

# create header
header_path = image_utils.create_header(logger)

# create collage
collage_path = image_utils.create_collage(logger, album_list)

# create caption
twitter_caption = utils.create_caption(logger, album_list)
tumblr_tags = utils.create_tumblr_tags(logger, album_list)

# tweet collage
if os.getenv('TWITTER_POST') == '1':
    twitter_utils.tweet_collage(logger, collage_path, twitter_caption)

# post collage to instagram
if os.getenv('INSTAGRAM_POST') == '1':
    instagram_utils.instagram_collage(logger, collage_path, twitter_caption)

# post collage to tumblr
if os.getenv('TUMBLR_POST') == '1':
    tumblr_utils.tumblr_collage(logger, collage_path, twitter_caption, tumblr_tags)

# done
logger.info('done ✅')
