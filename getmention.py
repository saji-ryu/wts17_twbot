#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy
from passkey import *


# Twitter OAuth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

# Twitter API
api = tweepy.API(auth)

# Mentionの取得
# 自分宛てのツイートを取得して表示
mentions = api.mentions_timeline(count=10)
for tweet in mentions:
    print tweet.text, tweet.user.screen_name

# ツイートを送信
# try:
#     api.update_status(status='Hello, world!')
# except tweepy.TweepError as e:
#     print e
