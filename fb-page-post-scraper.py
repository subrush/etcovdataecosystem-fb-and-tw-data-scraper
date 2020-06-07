#facebook page - post scraper 
import facebook_scraper
from facebook_scraper import get_posts, codecs, fetch_share_and_reactions
import pandas as pd
import csv, json 
import logging
import re
import sys
from datetime import datetime
from urllib import parse as urlparse
from requests import RequestException
from requests_html import HTML, HTMLSession


account = []
#attributes of twitter post
post_id = []
timestamp = []
author = []
post = []
likes = []
share = []
source = []
media = []
comments = []
location = []

try: 
    account = open('./account_fb.txt', encoding='utf-8').readlines()
except:
    print("File does not exist") 
#id, author, title, timestamp, post/tweet, like/favorite, share/retweet, url, social media(fb or tweet)
#{tweet_id, time, author,  tweet_txt,  favorite, 'retweet/share': retweet, 'social media': media})

def get_facebook_post(accounts):
    for account in accounts[:-1]:        
        for mypost in get_posts(account[:-1], extra_info=True, pages=10): #ethioDJMusic, PMAbiyAhmedAli, EthiopiaFMoH, getu26 
            post_id.append(mypost['post_id'])
            timestamp.append(mypost['time'])
            author.append(' ')
            post.append(mypost['text'])
            likes.append(mypost['likes'])
            comments.append(mypost['comments'])
            share.append(mypost['shares'])
            #reactions.append(mypost.get('reactions'))
            source.append(mypost['post_url'])
            media.append('facebook')
            location.append(' ')
        fbdata = pd.DataFrame({'post id':post_id, 'time stamp':timestamp, 'author':author, 'post':post, 'likes':likes, 'shares':share, 'comments': comments, 'social media':media, 'sources':source, 'location': location})
      #tdata = pd.DataFrame({'post id': tweet_id, 'time stamp': time, 'author': author, 'post': tweet_txt, 'likes': favorite, 'shares': retweet, 'comments': comments, 'social media': media, 'source': source, 'location': location})
 
    return fbdata

def save_data(fb_data):
    #filter data that has more than 200 shares and 1000 likes
    #fb = fbdata[(fbdata['shares'] > 200) & (fbdata['likes'] > 1000)] 
    fb = fb_post[['post']].apply(lambda p: p.str.contains('ኮሮና|ቫይረስ|corona|covid|virus|coronavirus|ኮቪድ', regex=True)).any(axis=1)
    try:
        with open("./data/"+"fb-page-"+datetime.now().strftime('%Y-%m-%d') + ".csv",'w', encoding='utf-8') as file:
            fb_data[fb].to_csv(file)
    except:
        print("File openning error") 
    
    
if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    
    fb_post = get_facebook_post(account)
    
    logging.info('[!] Scraping complete. Total: {}'.format(len(fb_post)))
    logging.info('[!] Saving.')
    save_data(fb_post)