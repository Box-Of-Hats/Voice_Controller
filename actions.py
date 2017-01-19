"""
This contains the custom functions that are utilised by voice_controller. Must be added to config.py in order to be recognised
"""
import os
import requests
from bs4 import BeautifulSoup
import webbrowser
import pyautogui
import time
import wolframalpha

import win32ui as wui

def google_search(search_term):
    #Does a google search for a given phrase
    os.system("start chrome \"https://www.google.co.uk/webhp?hl=en&sa=X&ved=0ahUKEwiC3pLk_s3RAhUGxxQKHUbFCfEQPAgD#hl=en&q={}\"".format(search_term))
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
        return "Playing: {}".format(search_term)
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

def pause_listener(args="ignore"):
    input(">>>Press Enter To Start Listening Again")
    return "Listening resumed"


def open_gdrive(args="ignore"):
    os.system("start chrome https://drive.google.com/drive/my-drive")
    return "Opening Google Drive"

def open_email(args="ignore"):
    os.system("start thunderbird")
    return "Opening Emails"

def run_command(command):
    os.system("{}".format(command))
    return "Running command: {}".format(command)

def start_program(program_name):
    os.system("start {}".format(program_name))
    return "Starting program: {}".format(program_name)


def get_weather(args="ignore"):
    url = "http://www.bbc.co.uk/weather/2653822"
    page = requests.get(url).content
    soup = BeautifulSoup(page, "lxml")
    summary = soup.find("p",{"class":"body"}).getText()
    return summary


def set_timer(phrase):
    os.system("start chrome \"https://www.google.co.uk/webhp?hl=en&sa=X&ved=0ahUKEwiC3pLk_s3RAhUGxxQKHUbFCfEQPAgD#hl=en&q={} timer\"".format(phrase))
    return "setting timer for: {}".format(phrase)

def query_wolfram(phrase):
    wolfram_appid =  ""

    client = wolframalpha.Client(wolfram_appid)
    res = client.query(phrase)
    #print(res)
    for pod in res:
        #for part in pod:
        #    if 
        #    print(part)
        try:
            if pod['@id'] == 'Result':
                return pod['subpod']['plaintext']
        except KeyError:
            pass
    return False
