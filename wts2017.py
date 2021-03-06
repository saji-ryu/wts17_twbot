#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import system
from passkey import *
import codecs
import re
import tweepy
from datetime import datetime, timedelta


# Twitter OAuth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

# Twitter API
api = tweepy.API(auth)

# 自分のタイムラインを取得
timeline = api.home_timeline(count=150)

one_day = timedelta(days=1)

# 呼び出された時の丸一日前の時点を取得
day_start = datetime.now() - one_day
# 日本との時差
tojst = timedelta(hours=9)

# 各月における評価点の辞書
point_rule = {}

if day_start.month == 1:
    point_rule = {"spring":0, "summer":-5, "autumn":0, "winter":5}
elif day_start.month == 2:
    point_rule = {"spring":0, "summer":-5, "autumn":-1, "winter":4}
elif day_start.month == 3:
    point_rule = {"spring":2, "summer":-4, "autumn":-3, "winter":3}
elif day_start.month == 4:
    point_rule = {"spring":5, "summer":0, "autumn":-5, "winter":0}
elif day_start.month == 5:
    point_rule = {"spring":5, "summer":0, "autumn":-3, "winter":0}
elif day_start.month == 6:
    point_rule = {"spring":3, "summer":3, "autumn":0, "winter":-2}
elif day_start.month == 7:
    point_rule = {"spring":0, "summer":5, "autumn":0, "winter":-4}
elif day_start.month == 8:
    point_rule = {"spring":0, "summer":5, "autumn":2, "winter":-5}
elif day_start.month == 9:
    point_rule = {"spring":-4, "summer":2, "autumn":5, "winter":-4}
elif day_start.month == 10:
    point_rule = {"spring":-5, "summer":0, "autumn":5, "winter":0}
elif day_start.month == 11:
    point_rule = {"spring":-4, "summer":-3, "autumn":3, "winter":1}
elif day_start.month == 12:
    point_rule = {"spring":-1, "summer":-5, "autumn":0, "winter":4}


# 各ツイートの情報を保持する配列
tweet_score = []

# タイムラインのテキストをoutput.txtに書き出し
fp = codecs.open('output.txt', 'w', 'utf-8')
for tweet in timeline:
    # tweet.created_atはUTCなのでJSTに変換
    tweet_time = tweet.created_at + tojst
    # スタートよりも遅い投稿であるか見る
    if day_start < tweet_time:
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
for line in codecs.open('dict.txt','r','utf-8'):
    line = line.rstrip()
    lis = line.split("\t")
    dict[lis[0]] = lis[1]

# ツイート内に季語があるか
line_count = 0
noun_count = 0
tweet_count = 0
point = 0
pre = []
for line in codecs.open('output.txt.chasen','r','utf-8'):
    line = line.rstrip('\r\n')
    if line == "EOS":
        # 名詞の割合が8割を超える=日本語としておかしい時
        if noun_count/line_count > 0.8:
            # ０点
            tweet_score[tweet_count][2] = 0
        del pre[:]
        point = 0
        line_count = 0
        noun_count = 0
        tweet_count += 1
    else:
        line_count += 1
        lis = line.split("\t")
        # 季語の辞書にあった場合かつその言葉がツイート内で初めての時
        if lis[2] in dict and lis[2] not in pre:
            # 現在のツイートに季語から判断した得点を追加
            tweet_score[tweet_count][2] += point_rule[dict[lis[2]]]
            pre.append(lis[2])
        # 名詞の数をカウント
        if re.search(ur'名詞',lis[3]):
            noun_count += 1


# 点数順に並び替え
tweet_score.sort(key=lambda x:x[2],reverse=True)

# ツイート文
text = '今日の季節感あるtweetランキング!!\n'
rank = 1

# 上位３つのツイートを表示する
for i in range(len(tweet_score)):
    # みんな０点だったら
    if tweet_score[0][2] <= 0:
        text = 'みなさん全然季節感がありませんね.......'
        break
    # 表示は３位まで
    if rank > 3:
        break
    # 順位とユーザー名、非公式引用リツイートの形で前半２０文字をリツイート
    elif tweet_score[i][2] > 0 and tweet_score[i][3] != 'wts2017_team13':
        text += str(rank) + '位は' + tweet_score[i][1].encode('utf8') + 'さんでした　' + 'RT @' + tweet_score[i][3].encode('utf8') + ': ' + tweet_score[i][4].encode('utf8') + '\n'
        rank += 1
# 該当者０の場合
if text == '今日の季節感あるtweetランキング!!\n':
    text = 'みなさん全然季節感がありませんね.......'

# ログ
print text

# 投稿
try:
    api.update_status(status=text)
except tweepy.TweepError as e:
    print e
