# A collection of functions to extract information from
# tweets. The functions assume that the tweet has been
# converted into a dict using the python.json library.

import json
import pandas as pd

def get_full_text(tweet):
    '''
    Return the (whole, not curtailed) text of the tweet.
    Note: if it's a retweet, then we need to return the
    text from the retweet feature, not the main body.
    '''
    if 'retweeted_status' not in tweet:
        if 'extended_tweet' not in tweet:
            return tweet['text']
        else:
            return tweet['extended_tweet']['full_text']
    else:
        if 'extended_tweet' in tweet['retweeted_status']:
            return tweet['retweeted_status']['extended_tweet']['full_text']
        else:
            return tweet['retweeted_status']['text']

def get_hashtags(tweet):
    '''Get all hashtags in the given tweet'''
    hashtag_set_out=set()

    for key in tweet:
        if key=='hashtags':
            hashtag_set_out=hashtag_set_out.union({ht['text']
                                                   for ht in tweet[key]})
        else:
            if type(tweet[key])==dict:
                set_to_add=get_hashtags(tweet[key])
                hashtag_set_out=hashtag_set_out.union(set_to_add)

    return hashtag_set_out


def get_user_mentions(dict_in):
    '''Return the set of users mentioned in the tweet'''
    mentioned_user_set_out=set()

    for key in dict_in:
        if key=='user_mentions':
            mentioned_user_set_out=mentioned_user_set_out.union({mu['screen_name']
                                                                 for mu in dict_in[key]})
        else:
            if type(dict_in[key])==dict:
                set_to_add=get_user_mentions(dict_in[key])
                mentioned_user_set_out=mentioned_user_set_out.union(set_to_add)

    return mentioned_user_set_out

def get_timestamp(tweet):
    '''Return the date and time of the tweet'''
    # Use pandas 'cos it's got a good datetime parser in it
    return pd.to_datetime(tweet['created_at']).to_pydatetime()


def is_retweet(tweet):
    '''True if a retweet, False otherwise'''
    return 'retweeted_status' in tweet

def is_reply_to_screen_name(tweet):
    '''screen_name if a reply, empty otherwise'''
    sn=tweet['in_reply_to_screen_name']
    if sn:
        return sn
    else:
        return ''

def get_retweet_timestamp(tweet):
    '''If a retweet, return the date and time of the
       original tweet. Otherwise return None.'''
    # Use pandas 'cos it's got a good datetime parser in it
    if not is_retweet(tweet):
        return None
    else:
        return pd.to_datetime(tweet['retweeted_status']['created_at']).to_pydatetime()

def get_user_screenname(tweet):
    '''Return the screen name of the posting user'''
    return tweet['user']['screen_name']

def get_user_name(tweet):
    '''Return the name of the posting user'''
    return tweet['user']['name']

def get_url(t):
    '''Get the (constructed) URL of the tweet'''
    return 'https://twitter.com/{}/status/{}'.format(t['user']['screen_name'],
                                                     t['id'])
