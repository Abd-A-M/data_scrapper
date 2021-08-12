import os
import random
import threading
import time
import pyperclip
import tweepy
import pandas as pd
import subprocess
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
from selenium import webdriver


def run_commands(command):
    command = command.split("[separator]")
    print(command)
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         text=True)
    return p


def everyone_timeline_keyword(keyword="باسم  ", tweettype=" ", min_like=0, min_retweets=0, min_replies=0):
    key = ["covid 19", "corona virus"]
    keyword=random.choice(key)
    if min_like != 0:
        min_l = "[separator]" "--min-like" + "[separator]" + str(min_like)
    else:
        min_l = ""

    if min_retweets != 0:
        min_rt = "[separator]" "--min-retweets" + "[separator]" + str(min_retweets)
    else:
        min_rt = ""

    if min_replies != 0:
        min_rp = "[separator]" "--min-replies" + "[separator]" + str(min_replies)
    else:
        min_rp = ""
    if tweettype.isspace():
        command = "twint" + "[separator]" + "-s" + "[separator]" + keyword + "[separator]" + "--count" + min_l + min_rt + min_rp
    else:
        command = "twint" + "[separator]" + "-s" + "[separator]" + keyword + "[separator]" + "--count" + "[separator]" + tweettype + min_l + min_rt + min_rp

    p = run_commands(command)
    lines = p.stdout
    for line in lines:
        stop = splitter(line)
        if stop:
            print("[*] everyone_timeline_keyword completed")
            return True


users = []
country = []


def splitter(line):
    try:
        items_ = line.split(" ", maxsplit=5)
        Tuser = items_[4]
        Tuser = Tuser.replace("<", "")
        Tuser = Tuser.replace(">", "")
        users.append(Tuser)
        country.append("")
    except:
        pass
    if len(users) == 200:
        country_ = []
        names = []
        data = pd.read_csv("sample.csv")
        for item in list(data["user"]):
            names.append(item)
        for item in list(data["country"]):
            country_.append(item)
        for item in users:
            names.append(item)
        for item in country:
            country_.append(item)

        dict = {"user": names, "country": country_}
        data = pd.DataFrame(dict)
        os.system("rm sample.csv")
        data.to_csv("sample.csv", header=True)
        users.clear()
        country.clear()
        return True


def image_dowenloader():
    data = pd.read_csv("sample.csv")
    names = data["user"]
    if len(names) >= 200:
        for i in range(len(names) - 200, len(names)):
            try:
                driver = webdriver.Chrome(ChromeDriverManager().install())
                time.sleep(10)
                driver.maximize_window()
                time.sleep(10)
                url = "https://twitter.com/" + names[i] + "/photo/"
                time.sleep(10)
                driver.get(url)
                time.sleep(10)
                pyautogui.click(x=975,
                                y=597,
                                clicks=1,
                                interval=2, button='right')
                pyautogui.click(x=1084,
                                y=633,
                                clicks=1,
                                interval=2, button='left')
                pyperclip.copy(names[i])
                time.sleep(10)
                pyautogui.hotkey('ctrl', 'v', interval=0.15)
                time.sleep(10)
                pyautogui.press('enter')
                time.sleep(10)
                driver.close()

            except:
                continue
        print("[*] image_download completed ")


def get_location():
    consumer_key = 'nQJEcQCIZxYZd3IBCgG4k8RE0'
    consumer_secret = 'e4ytqpDOdrx5nlkeszPkduqTfbadX7PUiY5OclpWxK0uPYNXF2'
    access_token = '58235285-lINP9lnrHfPsLGlgPwBJxjgQIXLtZHIJFxxIL8gzA'
    access_token_secret = 'TQXDt2dSUcrO2L1oWYq9tq76lpehNmox7ySkm9b5J7jvI'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    data = pd.read_csv("sample.csv")
    names = list(data["user"])
    country = list(data["country"])

    if len(names) >= 200:
        for i in range(len(names) - 200, len(names)):
            try:
                id = names[i]
                user = api.get_user(id)
                location = user.location
                country[i] = location
            except:
                continue
        os.system("rm sample.csv")
        dict = {"user": names, "country": country}
        data = pd.DataFrame(dict)
        data.to_csv("sample.csv", header=True)

        print("[*] get_location completed ")
#
while True:
    th = threading.Thread(target=everyone_timeline_keyword)
    th.start()
    time.sleep(20)
    get_location()
    time.sleep(20)
    image_dowenloader()
    time.sleep(20)
    th = threading.Thread(target=everyone_timeline_keyword, daemon=True)
    th.start()
    time.sleep(20)
    get_location()
    time.sleep(20)
    image_dowenloader()
    time.sleep(360)
# driver = webdriver.Chrome(ChromeDriverManager().install())
