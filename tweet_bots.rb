#!/usr/bin/env ruby
$LOAD_PATH << './'

require 'twitterbot.rb'

mcnulty = TwitterBot.new('jamesmcnulty')
mcnulty.tweet
mcnulty.reply
mcnulty.close

draper = TwitterBot.new('draper_don')
draper.tweet
draper.reply
draper.close

bauer = TwitterBot.new('getmebauer')
bauer.tweet
bauer.reply
bauer.close

