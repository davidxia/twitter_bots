#!/usr/bin/env python
# -*- coding: utf-8 -*-


from twitter_bot import TwitterBot

accts = ['jamesmcnulty', 'draper_don', 'getmebauer', 'sookie_stakhaus', 'walterwhite_',
         'doctor_ghouse', 'ned_stark_', 'portlandiafred', 'portlandiacarie']

for acct in accts:
    try:
        bot = TwitterBot(acct)

        # Check API credentials are valid
        bot.twitter_client.GetUserTimeline()

        if acct == 'portlandiafred':
            bot.converse_with('portlandiacarie')
        elif acct == 'portlandiacarie':
            bot.converse_with('portlandiafred')

        bot.tweet()
        bot.reply()
    except Exception as e:
        print "%s ERROR" % bot.name
        print e
        continue

print 'done'
