#!/usr/bin/env python
# -*- coding: utf-8 -*-


from email.mime.text import MIMEText
import logging
import logging.handlers
try:
    import simplejson as json
except ImportError:
    import json
import smtplib
import socket
import traceback

from twitter_bot import TwitterBot


def load_conf(filename):
    with open(filename) as f:
        return json.load(f)

conf = load_conf('twitter_bots.conf')

logger = logging.getLogger('tweet_bots')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(conf['logging']['logfile'],
                                               maxBytes=conf['logging']['max_bytes'],
                                               backupCount=conf['logging']['backup_count'])
formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(funcName)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

bot_usernames = conf['bot_usernames']

for bot_username in bot_usernames:
    logger.info('activating bot %s' % bot_username)

    try:
        bot = TwitterBot(bot_username)

        # Check API credentials are valid
        bot.twitter_client.GetUserTimeline()

        if bot_username == 'portlandiafred':
            bot.converse_with('portlandiacarie')
        elif bot_username == 'portlandiacarie':
            bot.converse_with('portlandiafred')

        tweet = bot.tweet()
        if tweet:
            logger.info('%s tweeted %s' % (bot_username, tweet))
        else:
            logger.error('%s failed to tweet' % bot_username)

        tweet = bot.reply()
        if tweet:
            logger.info('%s replied %s' % (bot_username, tweet))

    except Exception as e:
        error_msg = "%s ERROR + %s" % (bot.name, str(e))
        logger.error(error_msg)
        content = error_msg + '\n\n' + traceback.format_exc()
        msg = MIMEText(content)
        msg['Subject'] = 'twitter_bots: tweet_bots.py error'
        msg['From'] = socket.gethostname()
        msg['To'] = conf['error_email']
        s = smtplib.SMTP('localhost')
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()
