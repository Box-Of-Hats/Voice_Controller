"""
Config settings for voice_controller.py

actions = [ (trigger phrase, trigger function, function description), ]
"""
from actions import *

key_phrase = "robyn" #The phrase used to wake the listener. Set as "" to have listener always awake
audio_out = 2 # 0,1,2 :: 0: Mute, 1: Beeps, 2: Text To Speech
actions = [
    ("google", google_search, "Search Google for a given phrase"),
    ("play", play_youtube_video, "Play a youtube video"),
    ("itunes", play_itunes_music, "Play music in iTunes"),
    ("stop listening", quit, "Quit"),
    ("show me what you got", me_irl, "Lets meme")
]
speech_tracks = {
    "WELCOME": "resources\\audio_clips\\welcome.wav",
    "WAKE": "resources\\audio_clips\\how_can_i_help.wav", #Played when listener is woken by key_phrase
    "NOT_RECOGNISED": "resources\\audio_clips\\i_dont_understand.wav", #Played when a phrase isn't recognised
}