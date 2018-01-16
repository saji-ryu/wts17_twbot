# wts17_twbot

## 概要
2017年秋学期の授業、webテキスト処理法の最終課題用のレポジトリです。  
他人のツイートを解析し、フォローした人の中でその日一番季節にあったツイートをした人を教えてくれるtwitterBotです。

## 必要環境
- python(v2.7)
  - tweepy
- cron(linux)
- chasen

## 動作方法
1. wts2017.pyと同じディレクトリ内にpasskey.pyというファイルを作り、取得したAPI関連のキーを以下のように記述
  ```python:passkey.py
  # -*- coding: utf-8 -*-
  consumer_key        = 'xxxxxxxxxxxxxxxx'
  consumer_secret     = 'xxxxxxxxxxxxxxxx'
  access_token        = 'xxxxxxxxxxxxxxxx'
  access_token_secret = 'xxxxxxxxxxxxxxxx'
  ```
2. `$ crontab cron.schedule`

## リンク
https://twitter.com/wts2017_team13?lang=ja
