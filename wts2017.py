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
timeline = api.home_timeline(count=150)

# その日の0:00を設定
today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

# 各月における評価点の辞書
point_rule = {}

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

# 各ツイートの情報を保持する配列
tweet_score = []

# タイムラインのテキストをoutput.txtに書き出し
fp = codecs.open('output.txt', 'w', 'utf-8')
for tweet in timeline:
    if today_start < tweet.created_at:
        # 改行をなくして一文にする
        content = tweet.text
        content = content.replace('\n','')
        content = content.replace('\r','')
        # ファイルかきこみ
        fp.write(content + "\n")
        # 順位に表示する時用の切り詰めた文章を作る
        content_short = content[0:20]
        # 20文字以上なら......(略したという記号)をつける
        if len(content) > 20:
            content_short += ' ....'
        # 情報を配列に記憶
        tweet_score.append([tweet.id,tweet.user.name,0,tweet.user.screen_name,content_short])
fp.close()


# 外部コマンドの実行には `os.system()` を使う
# ここでは `from os import system` を宣言済み
system('chasen < output.txt > output.txt.chasen')

# 季語の辞書を読み込み
dict = {}
for line in codecs.open('dict2.txt','r','utf-8'):
    line = line.rstrip()
    lis = line.split("\t")
    dict[lis[0]] = lis[1]

# ツイート内に季語があるか
print len(tweet_score)
count = 0
point = 0
for line in codecs.open('output.txt.chasen','r','utf-8'):

    line = line.rstrip('\r\n')
    if line == "EOS":
        point = 0
        # if count < len(tweet_score):
        count += 1
    else:
        lis = line.split("\t")
        # 季語の辞書にあった場合
        if lis[2] in dict:
            print lis[2]
            # 現在のツイートに季語から判断した得点を追加
            tweet_score[count][2] += point_rule[dict[lis[2]]]


# 点数順に並び替え
tweet_score.sort(key=lambda x:x[2],reverse=True)
# print tweet_score[0][1]

# ツイート文
text = ''

# 上位３つのツイートを表示する
for i in range(3):
    # みんな０点だったら
    if tweet_score[0][2] <= 0:
        text += 'みなさん全然季節感がありませんね.......'
    # 順位とユーザー名、非公式引用リツイートの形で前半２０文字をリツイート
    elif tweet_score[i][2] > 0:
        text += str(i+1) + '位は' + tweet_score[i][1].encode('utf8') + 'さんでした　' + 'RT @' + tweet_score[i][3].encode('utf8') + ': ' + tweet_score[i][4].encode('utf8') + '\n'

# ログ
print text

# 投稿
try:
    api.update_status(status=text)
except tweepy.TweepError as e:
    print e
