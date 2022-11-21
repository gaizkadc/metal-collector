# metal-collector
A bot that collects Last.fm charts and post them to Twitter, IG and Tumblr.

This bot:
* retrieves your Last.fm weekly charts
* creates a collage with the most scrobbled albums from last week
* tweets it
* instagrams it
* tumblrs it

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

TUMBLR_CONSUMER_KEY=<consumer key>
TUMBLR_CONSUMER_SECRET=<consumer secret>
TUMBLR_OAUTH_TOKEN=<oauth token>
TUMBLR_OAUTH_SECRET=<oauth secret>
```

## Docker

To run the bot from Docker, create the `.env` file and run:
```
docker run --env-file /path/to/.env gaizkadc/metal-collector:latest
```
