# Setup

Install pip dependencies:

    $ sudo pip/install.py

or if you're using virtualenv

    (env)$ pip/install.py

Pickle a dictionary of user data:

    import pickle

    jamesmcnulty = {
        'access_token': 'blah',
        'access_token_secret': 'blah',
        'last_replied_tweet_id': 289070795626512384,
        'is_active': 1,
        'quotes': [
            "quote1",
            "quote2",
        ],
    }

    pickle.dump(jamesmcnulty, open('data/jamesmcnulty', 'wb'))

Define your bots' pickled data files in `tweet_bots.py` and cron it:

    # Run Twitter bots everyday at 13:00
    0 13 * * * /bin/bash -c 'cd /path/to/botdir && ./tweet_bots.py' >> cron.log 2>&1
