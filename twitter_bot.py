#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from random import choice
import twitter


class TwitterBot:

    def __init__(self, name):
        botfile = open('data/' + name, 'rb')
        self.data = pickle.load(botfile)
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
        self.twitter_client.PostUpdate(self.random_quote())

    def reply(self):
        statuses = self.twitter_client.GetSearch(term="to:%s" % self.name,
                                                 since_id=self.last_replied_tweet_id, per_page=1)
        if len(statuses) > 0:
            status = statuses[0]
            self.twitter_client.PostUpdate("@%s %s" % (status.user.screen_name, self.random_quote()), in_reply_to_status_id=status.id)
            self.update_last_replied_tweet_id(status.id)

    def converse_with(self, from_name):
        statuses = self.twitter_client.GetSearch("to:%s from:%s" % (self.name, from_name), per_page=1,
                                                 since_id=self.last_replied_tweet_id)
        if len(statuses) > 0:
            status = statuses[0]
            quote = self.find_reply_by_text(status.text)
            if quote is not None:
                self.twitter_client.PostUpdate(quote, in_reply_to_status_id=status.id)
                self.update_last_replied_tweet_id(status.id)

    def find_reply_by_text(self, text):
        if text in self.replies:
            reply = self.replies[self.replies.index(text) + 1]
            if reply in self.quotes:
                return reply

    def random_quote(self):
        return choice(self.quotes)

    def update_last_replied_tweet_id(self, since_id):
        self.data['last_replied_tweet_id'] = since_id
        botfile = open('data/' + self.name, 'wb')
        pickle.dump(self.data, botfile)
        botfile.close()
