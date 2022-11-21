import os
import pylast


def lastfm_login(logger):
    logger.info('logging in lastfm')

    api_key = os.getenv('LASTFM_API_KEY')
    api_secret = os.getenv('LASTFM_API_SECRET')
    username = os.getenv('LASTFM_USERNAME')
    password_hash = os.getenv('LASTFM_PASSWORD_HASH')

    logger.info(username)

    lfm = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret, username=username, password_hash=password_hash)

    return lfm


def get_weekly_charts(logger, lfm):
    logger.info('getting lastfm weekly charts')
    username = os.getenv('LASTFM_USERNAME')

    raw_album_list = lfm.get_user(username).get_weekly_album_charts()

    return unmarshal_artists_and_albums(logger, raw_album_list)


def unmarshal_artists_and_albums(logger, raw_album_list):
    logger.info('unmarshalling artists and albums')

    chart = []

    for i, raw_album in enumerate(raw_album_list):
        artist = str(raw_album[0]).split(' - ', 1)[0]
        album = str(raw_album[0]).split(' - ', 1)[1]

        chart.append([artist, album])

    return chart


def get_cover_img(logger, lfm, artist, album):
    logger.info('getting album cover: ' + artist + ' | ' + album)

    album = lfm.get_album(artist, album)

    return album.get_cover_image()


def get_complete_album_list(logger, lfm, weekly_charts):
    logger.info('getting complete album list')

    album_list = []

    for chart in weekly_charts:
        artist = chart[0]
        album = chart[1]
        cover = get_cover_img(logger, lfm, artist, album)

        if cover is not None:
            album = {
                'artist': artist,
                'album': album,
                'cover': cover
            }

            album_list.append(album)

            if len(album_list) == 9:
                return album_list

    return album_list
