#!/usr/bin/env ruby
#$LOAD_PATH << '/home/david/twitter_bots/'

require '/home/david/twitter_bots/twitterbot.rb'

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

sookie = TwitterBot.new('sookie_stakhaus')
sookie.tweet
sookie.reply
sookie.close

walter = TwitterBot.new('walterwhite_')
walter.tweet
walter.reply
walter.close

house = TwitterBot.new('doctor_ghouse')
house.tweet
house.reply
house.close

stark = TwitterBot.new('ned_stark_')
stark.tweet
stark.reply
stark.close

fred = TwitterBot.new('portlandiafred')
fred.converse_with('portlandiacarie')
fred.tweet
fred.reply
fred.close

carrie = TwitterBot.new('portlandiacarie')
carrie.converse_with('portlandiafred')
carrie.tweet
carrie.reply
carrie.close

puts 'done'
