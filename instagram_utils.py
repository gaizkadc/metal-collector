import os
import image_utils

from instabot import Bot


def instagram_collage(logger, collage_path, caption):
    logger.info('instagramming collage')

    ig_bot = instagram_login(logger)

    jpg_collage_path = image_utils.convert_to_jpg(logger, collage_path)

    ig_bot.upload_photo(jpg_collage_path, caption=caption)

    logger.info('collage instagrammed')


def instagram_login(logger):
    logger.info('logging in instagram')

    ig_username = os.getenv('IG_USERNAME')
    ig_password = os.getenv('IG_PASSWORD')

    cookie_path = 'config/Fohoma_uuid_and_cookie.json'
    if os.path.exists(cookie_path):
        os.remove(cookie_path)

    bot = Bot()
    bot.login(username=ig_username, password=ig_password)

    return bot
