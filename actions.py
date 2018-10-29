"""
This contains the custom functions that are utilised by voice_controller.
Add a function here and reference it in your config.json file to be able to use it.
"""
import os
import requests
from bs4 import BeautifulSoup
import pyautogui
import time


def google_search(search_term):
    """
    Does a google search for a given phrase
    """
    os.system("start chrome \"https://www.google.co.uk/webhp?q={}\"".format(search_term))
    return "Searching for {}".format(search_term)


def play_youtube_video(search_term, api_key):
    """
    Plays the first youtube video result for a given phrase
    """
    url = "https://www.googleapis.com/youtube/v3/search?q={query}&maxResults=1&part=snippet&key={yt_api_key}".format(
        query=search_term, yt_api_key=api_key)
    results = requests.get(url).json()
    video_id = results["items"][0]["id"]["videoId"]

    if video_id:
        video_url = "https://www.youtube.com/watch?v={}".format(video_id)
        os.system("start chrome \"{}\"".format(video_url))
        return "Playing: {}".format(search_term)
    else:
        return False


def play_itunes_music():
    """
    Open iTunes and press play.
    """
    os.system("start itunes /min")
    time.sleep(5)

    pyautogui.keyDown("playpause")
    pyautogui.keyUp("playpause")
    return "Playing iTunes music"


def launch_reddit_slideshow(subreddit, private=False):
    """
    Launch a reddit slideshow of a given subreddit, such as /r/me_irl or /r/dogs
    """
    if private:
        incognito = "/incognito"
    else:
        incognito = ""
    os.system("start chrome \"http://redditp.com/r/{subreddit}\" {incognito}".format(
        subreddit=subreddit, incognito=incognito))
    return "Here is what I could find"


def set_timer(time_period):
    """
    Launch a chrome window with a timer running for a given time period
    """
    os.system(
        "start chrome \"https://www.google.co.uk/search?q={time_period} timer\"".format(time_period=time_period))
    return "setting timer for: {time_period}".format(time_period=time_period)

def change_volume(amount):
    """
    Make a relative change to the current volume.
    """
    presses_required = int(abs(amount)/2)
    if amount > 0:
        for i in range(0, presses_required):
            pyautogui.press("volumeup")
    else:
        for i in range(0, presses_required):
            pyautogui.press("volumedown")
    return "Changed volume by {amount}".format(amount=amount)

def set_absolute_volume(level):
    """
    Set the volume to be an absolute value.
    """
    try:
        level = int(level)
    except:
        return "The volume level should be a number"
    #Completely mute audio first so we know the current volume
    for i in range(0, 50):
        pyautogui.press("volumedown")

    #Cap volume to 100%
    presses_required = min(int(abs(level)/2), 50)

    for i in range(0, presses_required):
        pyautogui.press("volumeup")

    return "Set volume to {level}".format(level=level)