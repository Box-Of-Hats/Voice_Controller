"""
This contains the custom functions that are utilised by voice_controller. Must be added to config.py in order to be recognised
"""
import os
import requests
from bs4 import BeautifulSoup
import webbrowser
import pyautogui
import time

import win32ui as wui

def google_search(search_term):
    #Does a google search for a given phrase
    os.system("start chrome \"https://www.google.co.uk/?gfe_rd=cr&ei=hxV9WJ_wDK2k8wffi7yQBw#q={}\"".format(search_term))
    return "Searching for {}".format(search_term)

def play_youtube_video(search_term):
    #Plays the first youtube video result for a given phrase
    url = "https://www.youtube.com/results?search_query={}".format(search_term)
    page = requests.get(url).content
    soup = BeautifulSoup(page, "lxml")
    thing = soup.find("a",{"class":"yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink      spf-link "})
    if thing:
        video_url = "https://www.youtube.com{}".format(thing['href'])
        os.system("start chrome \"{}\"".format(video_url))
        return "Playing video: {}".format(search_term)
    else:
        return False

def play_itunes_music(args="ignore"):
    try:
        wui.FindWindow("iTunes", "iTunes")
        is_open = True
    except:
        is_open = False


    if not is_open:
        os.system("start /min \"\" E:\\Program_Files\\iTunes_0409\\iTunes.exe")
        time.sleep(2)
    pyautogui.keyDown("playpause")
    pyautogui.keyUp("playpause")
    return "Playing iTunes music"

def me_irl(args="ignore"):
    os.system("start chrome \"http://redditp.com/r/me_irl\"")
    return "stop looking at memes. you sack of shit"