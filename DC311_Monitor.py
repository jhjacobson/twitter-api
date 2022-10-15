#Max search for tweets - 450 per 15 minute window

import tweepy
import re
from datetime import datetime, timezone
from twitter_auth import BEARER_TOKEN
DELIM="|"
TWEET_URL_PREFIX="=HYPERLINK(\"https://twitter.com/twitter/status/"
TWEET_URL_SUFFIX='","Link")'
DEBUG=0

def check_for_311_tweet(client,conversation_id):
    query="from:311DCGov conversation_id:"+str(conversation_id)
    search_convo = client.search_recent_tweets(query=query,tweet_fields=['created_at','author_id','referenced_tweets'], max_results=10)
    result=""
    if search_convo.data is None:
        result="No 311 Response"
    else:
        try:
            tweet_text_from_311=search_convo.data[0].text
            result=re.search("(22-\d{8})",tweet_text_from_311)[0]
        except:
            result="No SR Included by 311"
    return result

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def get_tweets(client, query, start_time, end_time,max_results):
    #query = 'from:MKeegan_5F07 @311DCgov -is:retweet'
    #start_time='2022-10-05T23:36:00-04:00'
    #end_time='2022-10-12T22:10:59-04:00'
    tweets = client.search_recent_tweets(query=query, start_time=start_time, end_time=end_time, 
                                        tweet_fields=['conversation_id', 'created_at','author_id'], 
                                        max_results=max_results)
    return tweets

def get_search_params():
    query = '#sidewalkpalooza @311DCgov -is:retweet'
    start_time='2022-10-12T23:36:00-04:00'
    end_time='2022-10-13T23:35:59-04:00'
    return query, start_time, end_time

def init_file(delim):
    file=open("tweets.csv","w")
    line=f"Tweeted{delim}Tweet Text{delim}URL{delim}Username{delim}Name{delim}Service Request ID"
    if DEBUG:
        line += f"{delim}Tweet ID{delim}Conversation ID"
    file.write(line)
    return file

def main():
    max_results=100
    if DEBUG:
        max_results=10
    file = init_file(DELIM)
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    query, start_time, end_time = get_search_params()
    tweets=get_tweets(client, query, start_time, end_time,max_results)
    for tweet in tweets.data:
        tweet_url=TWEET_URL_PREFIX+str(tweet.id)+TWEET_URL_SUFFIX
        user = client.get_user(id=tweet.author_id)
        tweet_text_without_line_break=tweet.text.replace("\n"," ")
        created_at=utc_to_local(tweet.created_at).strftime("%m/%d/%Y")
        name=user.data.name
        if hasattr(tweet,'conversation_id'):
            conversation_id=tweet.conversation_id
            service_request=check_for_311_tweet(client,conversation_id)
        else:
            service_request="No 311 Response lol"
        username="@"+user.data.username
        line=f"\n{created_at}{DELIM}{tweet_text_without_line_break}{DELIM}{tweet_url}{DELIM}{username}{DELIM}{name}{DELIM}{service_request}"
        #line=f"\n{created_at}{DELIM}{tweet_text_without_line_break}{DELIM}{tweet_url}{DELIM}{username}{DELIM}{name}{DELIM}{service_request}"
        if DEBUG:
            line += f"{DELIM}{tweet.id}{DELIM}{conversation_id}"
        file.write(line)
    file.close()

main()