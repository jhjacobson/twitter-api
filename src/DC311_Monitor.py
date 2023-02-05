#Max search for tweets - 450 per 15 minute window
import tweepy
import re
from datetime import datetime, timezone, timedelta
from auth import BEARER_TOKEN
from dc_311_api import *
DELIM="|"
TWEET_URL_PREFIX="=HYPERLINK(\"https://twitter.com/twitter/status/"
TWEET_URL_SUFFIX='","Link")'
DEBUG=0
TWEETS_FILE="tweets.csv"

def check_for_311_tweet(client,conversation_id,original_tweet_id):
    query="from:311DCGov conversation_id:"+str(conversation_id)
    search_convo = client.search_recent_tweets(query=query,tweet_fields=['created_at','author_id','referenced_tweets'], max_results=100)
    if search_convo.data is None:
        result="No 311 Response"
    else:
        service_request = get_service_request_from_311_tweet(search_convo.data,original_tweet_id)
        result = service_request if service_request is not None else "No 311 response"
    return result

def get_service_request_from_311_tweet(tweets_from_311,original_tweet_id):
    for tweet in tweets_from_311:
        for reply_from_311 in tweet.referenced_tweets:
            if ((reply_from_311.id == original_tweet_id) and (reply_from_311.type == "replied_to")):
                try:
                    result=re.search("(22-\d{8})",tweet.text)[0]
                except:
                    result="No SR Included by 311"
                return result

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def get_tweets(client,query,start_time, end_time,max_results):
    tweets = client.search_recent_tweets(query=query, start_time=start_time, end_time=end_time, 
                                        tweet_fields=['conversation_id', 'created_at','author_id'], 
                                        max_results=max_results)
    return tweets

def is_sr(service_request_string):
    if re.search("(22-\d{8})",service_request_string):
        return 1
    else:
        return 0

def get_search_params():
    query = '#sidewalkpalooza @311DCgov -is:retweet'
    #query = 'from:JoshForANC @311DCgov -is:retweet'
    #query='from:nikkidc4anc6A03 @311DCGov -is:retweet'
    yesterday = (datetime.today().date() - timedelta(days=1)).strftime("%Y-%m-%d")
    #start_time=yesterday+"T00:00:00-04:00"
    #end_time=yesterday+"T23:59:59-04:00"
    #Run for nikkidc4anc6A03 for 10/19
    start_time='2022-10-24T16:00:00-04:00'
    end_time='2022-10-29T23:59:59-04:00'
    #2022-10-15T23:59:59-4:00]
    return query, start_time, end_time

def init_file(delim):
    file=open(TWEETS_FILE,"w")
    line=f"Tweeted{delim}Tweet Text{delim}URL{delim}Username{delim}Name{delim}Service Request ID"
    line += get_sr_line_headers()
    if DEBUG:
        line += f"{delim}Tweet ID{delim}Conversation ID"
    file.write(line)
    return file

def get_tweet_info(tweet,client):
    tweet_url=TWEET_URL_PREFIX+str(tweet.id)+TWEET_URL_SUFFIX
    user = client.get_user(id=tweet.author_id)
    tweet_text_without_line_break=tweet.text.replace("\n"," ")
    created_at=utc_to_local(tweet.created_at).strftime("%m/%d/%Y")
    service_request=check_for_311_tweet(client,tweet.conversation_id,tweet.id)
    username="@"+user.data.username
    line=f"\n{created_at}{DELIM}{tweet_text_without_line_break}{DELIM}{tweet_url}{DELIM}{username}{DELIM}{user.data.name}{DELIM}{service_request}"
    if is_sr(service_request):
        line += get_sr_datapoints(service_request)
    else:
        line += not_an_sr_datapoints()
    if DEBUG:
        line += f"{DELIM}{tweet.id}{DELIM}{tweet.conversation_id}"
    return line



def main():
    max_results=10 if DEBUG else 100
    file = init_file(DELIM)
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    query, start_time, end_time = get_search_params()
    tweets=get_tweets(client, query, start_time, end_time,max_results)
    for tweet in tweets.data:
        line = get_tweet_info(tweet,client)
        file.write(line)
    file.close()

main()