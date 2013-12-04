#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import simplejson as json
except ImportError:
    import json
from random import choice
import twitter


class TwitterBot:

    def __init__(self, name):
        botfile = open('data/' + name, 'rb')
        self.data = json.load(botfile)
        botfile.close()

        self.name = name
        self.last_replied_tweet_id = self.data['last_replied_tweet_id']
        self.is_active = self.data['is_active']
        self.quotes = self.data['quotes']
        self.replies = self.data.get('replies')
        self.twitter_client = twitter.Api(
            consumer_key='wgSiqzzG1yIANIwhqNZWCA',
            consumer_secret='uBocxUaYDWByEbmoz3A0Un4cPyN6CZ3nlgdu4A7tSQ',
            access_token_key=self.data['access_token'],
            access_token_secret=self.data['access_token_secret']
        )

    def tweet(self):
        trimmed_quote = self.random_quote()[:140]
        status = self.twitter_client.PostUpdate(trimmed_quote)
        return status.text

    def reply(self):
        statuses = self.twitter_client.GetSearch(term="to:%s" % self.name,
                                                 since_id=self.last_replied_tweet_id, count=1)
        if len(statuses) > 0:
            status = statuses[0]
            trimmed_reply = "@%s %s" % (status.user.screen_name, self.random_quote())[:140]
            updated_status = self.twitter_client.PostUpdate(trimmed_reply, in_reply_to_status_id=status.id)
            self.update_last_replied_tweet_id(status.id)
            return updated_status.text
        else:
            return False

    def converse_with(self, from_name):
        statuses = self.twitter_client.GetSearch("to:%s from:%s" % (self.name, from_name), count=1,
                                                 since_id=self.last_replied_tweet_id)
        if len(statuses) > 0:
            status = statuses[0]
            quote = self.find_reply_by_text(status.text)
            if quote is not None:
                status = self.twitter_client.PostUpdate(quote, in_reply_to_status_id=status.id)
                self.update_last_replied_tweet_id(status.id)
                return status.text
            else:
                return False
        else:
            return False

    def find_reply_by_text(self, text):
        if text in self.replies:
            reply = self.replies[self.replies.index(text) + 1]
            if reply in self.quotes:
                return reply

    def random_quote(self):
        return choice(self.quotes)

    def update_last_replied_tweet_id(self, since_id):
        self.data['last_replied_tweet_id'] = since_id
        with open('data/' + self.name, 'wb') as botfile:
            json.dump(self.data, botfile, indent=4, sort_keys=True)
