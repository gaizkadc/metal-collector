# imports
import os

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
# header_path = image_utils.create_header(logger)

# create collage
# collage_path = image_utils.create_collage(logger, album_list)

# create caption
caption = utils.create_caption(logger, album_list)

# tweet collage
if os.getenv('TWITTER_POST') == '1':
    # twitter_utils.tweet_collage(logger, collage_path, caption)
    client = twitter_utils.get_twitter_client(logger)
    twitter_utils.tweet_caption(logger, client, caption)

# post collage to instagram
# if os.getenv('INSTAGRAM_POST') == '1':
#     instagram_utils.instagram_collage(logger, collage_path, caption)

# done
logger.info('done ✅')
