# Setup

Install pip dependencies:

    $ sudo pip/install.py

or if you're using virtualenv

    (env)$ pip/install.py

Create a JSON file of user data and put into `data/bot_name`:

    {
        "access_token": "foo",
        "access_token_secret": "bar",
        "is_active": 1,
        "last_replied_tweet_id": 408329902472314900,
        "quotes": [
            "quote1",
            "quote2",
        ],
    }

Define your bots in `twitter_bots.conf`:

    {
      "logging": {
        "logfile": "logs/log",
        "max_bytes": 1000000,
        "backup_count": 5
      },
      "bot_usernames": [
        "jamesmcnulty",
        "draper_don",
        "getmebauer",
        "sookie_stakhaus",
        "walterwhite_",
        "doctor_ghouse",
        "ned_stark_",
        "portlandiafred",
        "portlandiacarie"
      ],
      "error_email": "david@davidxia.com"
    }

Cron it:

    # Run Twitter bots everyday at 13:00
    0 13 * * * /bin/bash -c 'cd /path/to/botdir && ./tweet_bots.py &>> cron.log'
