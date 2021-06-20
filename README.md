# metal-collector
A bot that collects Last.fm charts and post them to Twitter and IG.

This bot:
* retrieves your Last.fm weekly charts
* creates a collage with the most listened to albums from last week
* tweets it
* instagrams it

## Environment variables
Some env vars can be provided in an `.env` file:
```
APP_NAME=metal-collector
LOGS_FOLDER_PATH=logs

LASTFM_API_KEY=<you api keu>
LASTFM_API_SECRET=<your api secret>
LASTFM_USERNAME=<username>
LASTFM_PASSWORD_HASH=<password hash>

IMGS_FOLDER=img
BACKGROUND_FOLDER_PATH=backgrounds
FONTS_PATH=fonts

TWITTER_POST=1
INSTAGRAM_POST=1

TWITTER_CONSUMER_KEY=<consumer key>
TWITTER_CONSUMER_SECRET=<consumer secret>
TWITTER_ACCESS_TOKEN=<access token>
TWITTER_ACCESS_TOKEN_SECRET=<access token secret>

IG_USERNAME=<username>
IG_PASSWORD=<password>
```