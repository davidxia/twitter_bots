require 'dbi'
require 'twitter'

class TwitterBot
  HOSTNAME = 'localhost'
  USERNAME = 'twitter_bots'
  PASSWORD = 'GAqBSsV6hMZ2j9Nc'
  DBNAME = 'twitter_bots'
  CONSUMER_KEY = ''
  CONSUMER_SECRET = ''

  attr_accessor :name

  def initialize(name)
    @dbh = DBI.connect("DBI:Mysql:#{DBNAME}:#{HOSTNAME}", "#{USERNAME}", "#{PASSWORD}")

    @name = name
    @bot_id = bot_id
    @tokens = access_tokens

    Twitter.configure do |config|
      config.consumer_key = CONSUMER_KEY
      config.consumer_secret = CONSUMER_SECRET
      config.oauth_token = @tokens['access_token']
      config.oauth_token_secret = @tokens['access_token_secret']
    end
  end

  def tweet
    quote = get_random_quote['quote']
    Twitter.update(quote)
  end

  def reply
    since_id = last_replied_tweet_id
    status = Twitter.search("to:#{@name}", :rpp => 1, :result_type => 'recent', :since_id => since_id)[0]
    if !status.nil?
      quote = get_random_quote['quote']
      Twitter.update("@#{status.from_user} #{quote}", { :in_reply_to_status_id => status.id })
      update_last_replied_tweet_id(status.id)
    end
  end

  def converse_with(from)
    since_id = last_replied_tweet_id
    status = Twitter.search("to:#{@name} from:#{from}", :rpp => 1, :result_type => 'recent', :since_id => since_id)[0]
    if !status.nil?
      quote = find_quote_by_text(status.text)
      if !quote.nil?
        quote_id = quote['id']
        quote = find_quote_by_id(quote_id.to_i + 1)
        if !quote.nil?
          quote_text = quote['quote']
          Twitter.update("#{quote_text}", { :in_reply_to_status_id => status.id })
          update_last_replied_tweet_id(status.id)
        end
      end
    end
  end


  def close
    @dbh.disconnect
  end

  private
    def bot_id
      sth = @dbh.prepare("SELECT id FROM bots WHERE name = ?")
      sth.execute(@name)
      id = sth.fetch_hash['id']
      sth.finish
      return id
    end


    def access_tokens
      sth = @dbh.prepare("SELECT * FROM access_tokens WHERE bot_id = ?")
      sth.execute(@bot_id)
      hash = sth.fetch_hash
      sth.finish
      return hash
    end

    def find_quote_by_text(text)
      sth = @dbh.prepare("SELECT * FROM quotes WHERE quote = ?")
      sth.execute(text)
      hash = sth.fetch_hash
      sth.finish
      return hash
    end

    def get_random_quote
      sth = @dbh.prepare("SELECT * FROM quotes WHERE bot_id = ? AND is_active = 1 ORDER BY RAND() LIMIT 1")
      sth.execute(@bot_id)
      hash = sth.fetch_hash
      sth.finish
      return hash
    end

    def find_quote_by_id(id)
      sth = @dbh.prepare("SELECT * FROM quotes WHERE bot_id = ? AND id = ?")
      sth.execute(@bot_id, id)
      hash = sth.fetch_hash
      sth.finish
      return hash
    end


    def last_replied_tweet_id
      sth = @dbh.prepare("SELECT last_replied_tweet_id FROM bots WHERE id = ?")
      sth.execute(@bot_id)
      last_id = sth.fetch_hash['last_replied_tweet_id'].to_i
      sth.finish
      return last_id
    end

    def update_last_replied_tweet_id(since_id)
      sth = @dbh.prepare("UPDATE bots SET last_replied_tweet_id = ? WHERE id = ?")
      sth.execute(since_id, @bot_id)
      sth.finish
    end


end

