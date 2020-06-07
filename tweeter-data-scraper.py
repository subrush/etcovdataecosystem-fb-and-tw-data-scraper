#tweeter data scraper
import os
import tweepy
import selenium
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import json, csv
import pandas as pd
import logging 
from datetime import datetime


acct_file = './account_twitter.txt'
account = []
#attributes of twitter post
tweet_id = []
location = []
time = []
tweet_txt = []
author = []
favorite = []
retweet = []
comments = []
geo_tweet = []
lang = []
source = []
media = []

#criteria for query and lang
query = '#covid%20OR%20#virus%20OR%20#corona%20OR%20corona%20OR%20virus'


#Twitter credentials for the app
consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' # API key
consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #API secret key
access_key= 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #Access token
access_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #Access token secret

def set_credentials():
    #pass twitter credentials to tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)    
    
    try:
        api.verify_credentials()
        #print("Authentication OK")
        logging.info('[!] Authentication OK.')
    except:
        loging.info('[!] Error during authentication.')
    return api

def read_account_file(acct_file):
    try: 
        account = open(acct_file, encoding='utf-8').readlines()
    except:
        print("File does not exist") 
    return account


def get_twitter_post(account_file):
    api = set_credentials()
    accounts = read_account_file(account_file)
    if api != None and  accounts != None: 
        for account in accounts[:-1]:
            tweets = api.user_timeline(id=account, lang=['am%20OR%20en'], q=query, tweet_mode='extended', count=30)
            for tweet in tweets:
                tweet_id.append(tweet.id) 
                author.append(tweet.author.name)            
                time.append(tweet.created_at)    
                tweet_txt.append(tweet.full_text)    
                favorite.append(tweet.favorite_count)    
                retweet.append(tweet.retweet_count) 
                temp = [url['expanded_url'] for url in tweet.entities['urls']]
                source.append(temp) 
                comments.append(' ')
                media.append("twitter")
                location.append(tweet.user.location)
        tdata = pd.DataFrame({'post id': tweet_id, 'time stamp': time, 'author': author, 'post': tweet_txt, 'likes': favorite, 'shares': retweet, 'comments': comments, 'social media': media, 'source': source, 'location': location})
    #fbdata = pd.DataFrame({'post id':post_id, 'time stamp':timestamp, 'author':author, 'post':post, 'likes':likes, 'shares':share, 'comments': comments, 'social media':media, 'sources':source})
                        
    return tdata


def save_data(tw_data):
###filter the data that has more than 200 shares and 1000 likes
#tdata = tdata[(tdata['retweet/share'] > 100) & (tdata['favorite/like'] > 200)]
    try:
        with open("./data/"+"tw-"+datetime.now().strftime('%Y-%m-%d') + ".csv",'w', encoding='utf-8') as file:
            tw_data.to_csv(file)
    except:
        print("File openning error") 
    
if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    
    tw_post = get_twitter_post(acct_file)
    
    logging.info('[!] Scraping complete. Total: {}'.format(len(tw_post)))
    logging.info('[!] Saving.')
    save_data(tw_post)
