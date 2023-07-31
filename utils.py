import os
import sys
import logging
import random

from logging.handlers import RotatingFileHandler


def get_logger():
    logs_folder_path = os.getenv('LOGS_FOLDER_PATH')
    app_name = os.getenv('APP_NAME')

    if not os.path.isdir(logs_folder_path):
        os.mkdir(logs_folder_path)
    log_file_path = logs_folder_path + '/' + app_name + '.log'
    if not os.path.isfile(log_file_path):
        log_file = open(log_file_path, "a")
        log_file.close()

    logger = logging.getLogger(app_name)
    logger.setLevel('DEBUG')

    log_format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(log_file_path, maxBytes=(1048576 * 5), backupCount=5)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    logger.info('logger created')

    return logger


def create_caption(logger, album_list):
    logger.info('creating caption')

    pool_var1 = ['huevos', 'pollas', 'hostias']
    pool_var2 = ['', 'puta ', 'jodida ', 'mierda de ']
    pool_var3 = ['su puta madre ', 'mierda puta ', 'me cago en los cojones ']
    var1 = random.choice(pool_var1)
    var2 = random.choice(pool_var2)
    var3 = random.choice(pool_var3)

    caption = '¿Que a qué ' + var1 + ' le he estado metiendo esta semana? Me alegra que me hagas esa ' + var2 + 'pregunta; a ' + var3 + 'esto:\n'
    precaption = ''

    artist_list = get_artist_list(logger, album_list)

    i = 0
    while len(caption) <= 280 and i < len(artist_list):
        precaption = caption
        caption += hashtagize_artist(logger, artist_list[i])
        i += 1

    caption = precaption

    return caption


def hashtagize_artist(logger, artist):
    logger.info('hashtagizing artist: ' + artist)
    return '#' + artist.replace(' ', '').replace('-', '').replace('.', '').replace('&', 'and').replace('!', '').replace(',', '') + '\n'


def get_artist_list(logger, album_list):
    logger.info('getting artist list')

    artist_list = []

    for album in album_list:
        artist_list.append(album['artist'])

    return artist_list
