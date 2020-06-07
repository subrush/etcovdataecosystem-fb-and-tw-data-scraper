
import os
import requests
import re
import json
import time
import logging
import pandas as pd
from collections import OrderedDict
from bs4 import BeautifulSoup
from datetime import datetime



#attrib considered - id, author, title, timestamp, post/tweet, like/favorite, share/retweet, url, social media(fb or tweet) 

def get_bs(session, url):
    #Makes a GET requests using the given Session object and returns a BeautifulSoup object.
    r = None
    while True:
        r = session.get(url)
        if r.ok:
            break
    return BeautifulSoup(r.text, 'lxml')

def make_login(session, base_url, credentials):
    #Returns a Session object logged in with credentials.
    login_form_url = '/login/device-based/regular/login/?refsrc=https%3A'+'%2F%2Fmobile.facebook.com%2Flogin%2Fdevice-based%2Fedit-user%2F&lwv=100'
    params = {'email':credentials['email'], 'pass':credentials['pass']}

    while True:
        time.sleep(3)
        logged_request = session.post(base_url+login_form_url, data=params)
        
        if logged_request.ok:
            logging.info('[*] Logged in.')
            break
#open fb file from local machine
acct_file = './fb_profile_file.txt'
fb_file = []

def read_fb_files(file):
    try: 
        for file in os.listdir("./fb_profile"):
            if file.endswith(".html"):
                fb_file.append(file)       
    except:
        print("File does not exist") 
    return fb_file
#id, author, title, timestamp, post/tweet, like/favorite, share/retweet, url, social media(fb or tweet)
post_id = []
author = []
post = []
timestamp = []
likes = []
comments = []
share = []
media = []
source = []
location = []

def scrap_fb_profile_post(file):
    fb_files = read_fb_files(file)
    if fb_files != None:
        for file in fb_files:
            fb_file = open('./fb_profile/'+file, 'r', encoding='utf-8').read() 
            file_content = BeautifulSoup(fb_file, 'lxml')
            user_content = file_content.find_all('div', class_="userContentWrapper")

            for content in user_content:
                if content.find(class_="_5pcp") == None:
                    post_id.append("NA")
                else:
                    post_id.append(content.find('div', class_='_4r_y').text)
                if content.find(class_="_5ptz") == None:
                    timestamp.append("NA")
                else:
                    timestamp.append(((content.find(class_="_5ptz").text).strip()))    
                if content.find(class_="_3576") == None: 
                    post.append("NA") #user content
                else:
                    post.append((content.find(class_="_3576").text).strip()) #user content
                if content.find(class_="_355t _4vn2") == None: #share count
                    share.append("NA")
                else:        
                    share.append((content.find(class_="_355t _4vn2").text).strip())
                if content.find(class_="_4vn2") == None: #comment count
                    comments.append("NA")
                else:
                    comments.append((content.find(class_="_4vn2").text).strip())
                if content.find(class_="_3dli") == None: #like count _3dli
                    likes.append("NA")
                else:
                    likes.append((content.find(class_="_3dli").text).strip())
                author.append(' ')
                source.append(' ')
                location.append(' ')
                media.append('facebook')
        fbdata = pd.DataFrame(
                {'post id': post_id,'time stamp': timestamp,'author': author, 'post': post, 'likes': likes, 'shares': share, 'Comments': comments, 'social media': media, 'sources':source, 'location': location})
#fbdata = pd.DataFrame({'post id':post_id, 'time stamp':timestamp, 'author':author, 'post':post, 'likes':likes, 'shares':share, 'comments': comments, 'social media':media, 'sources':source, 'location': location})
        fbdata.to_csv('./fb_data.csv')
    return fbdata

def save_data(fb_data):
    #filter data that has more than 200 shares and 1000 likes
    #fb_post = fb_data[(int(fb_data['Num_shares']) > 200) & (int(fb_data['Likes']) > 1000)] 
    fb = fb_post[['post']].apply(lambda p: p.str.contains('ኮሮና|ቫይረስ|ቫይረሱ|corona|covid|virus|coronavirus|ኮቪድ', regex=True)).any(axis=1)
    
    try:
        with open("./data/"+"fb-profile-"+datetime.now().strftime('%Y-%m-%d') + ".csv",'w', encoding='utf-8') as file:
            fb_data[fb].to_csv(file)    
    except:
        print("File openning error") 
    
if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    
    fb_post = scrap_fb_profile_post(acct_file)
    
    logging.info('[!] Scraping complete. Total: {}'.format(len(fb_post)))
    logging.info('[!] Saving.')
    save_data(fb_post)