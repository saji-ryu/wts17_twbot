#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import system
from passkey import *
import codecs
import re
import tweepy
from datetime import datetime


# Twitter OAuth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

# Twitter API
api = tweepy.API(auth)

# 自分のタイムラインを取得
timeline = api.home_timeline(count=100)

today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

point_rule = {}

# if today_start.month <= 2:
#     point_rule = {"spring":1, "summer":-3, "autumn":1, "winter":3}
# elif today_start.month <= 5:
#     point_rule = {"spring":3, "summer":1, "autumn":-3, "winter":1}
# elif today_start.month <= 8:
#     point_rule = {"spring":1, "summer":3, "autumn":1, "winter":-3}
# elif today_start.month <= 11:
#     point_rule = {"spring":-3, "summer":1, "autumn":3, "winter":1}
# else:
#     point_rule = {"spring":1, "summer":-3, "autumn":1, "winter":3}

if today_start.month <= 2:
    point_rule = {"spring":1, "summer":-3, "autumn":1, "winter":3}
elif today_start.month <= 5:
    point_rule = {"spring":3, "summer":1, "autumn":-3, "winter":1}
elif today_start.month <= 8:
    point_rule = {"spring":1, "summer":3, "autumn":1, "winter":-3}
elif today_start.month <= 11:
    point_rule = {"spring":-3, "summer":1, "autumn":3, "winter":1}
else:
    point_rule = {"spring":1, "summer":-3, "autumn":1, "winter":3}

tweet_score = []

# タイムラインのテキストをoutput.txtに書き出し
fp = codecs.open('output.txt', 'w', 'utf-8')
for tweet in timeline:
    if today_start < tweet.created_at:
        fp.write(tweet.text + "\n")
        tweet_score.append([tweet.id,tweet.user.name,0])
fp.close()


# 外部コマンドの実行には `os.system()` を使う
# ここでは `from os import system` を宣言済み
system('chasen < output.txt > output.txt.chasen')


dict = {}
for line in codecs.open('dict.txt','r','utf-8'):
    line = line.rstrip()
    lis = line.split("\t")
    dict[lis[0]] = lis[1]


count = 0
point = 0
for line in codecs.open('output.txt.chasen','r','utf-8'):

    line = line.rstrip('\r\n')
    if line == "EOS":
        tweet_score[count][2] = point
        point = 0
        count += 1
    else:
        lis = line.split("\t")
        if lis[2] in dict:
            point += point_rule[dict[lis[2]]]

tweet_score.sort(key=lambda x:x[2],reverse=True)
print tweet_score



# for x in sorted(tweet_score.items(), key=lambda x:x[2], reverse=True):
#     print x[0], x[1],x[2]
