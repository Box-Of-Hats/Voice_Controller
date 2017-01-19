"""
Config settings for voice_controller.py

actions = [ (trigger phrase, trigger function, function description), ]
"""
from actions import *

ffmpeg_path = ".\\ffmpeg\\bin\\ffmpeg" # The filepath of the ffmpeg installation (required for active text_to_speach)

key_phrase = "robyn" #The phrase used to wake the listener. Set as "" to have listener always awake
audio_out_mode = 2 # 0,1,2 :: 0: Mute, 1: Beeps, 2: Text To Speech
actions = [
    ("google", google_search, "Search Google for a given phrase"),
    ("play", play_youtube_video, "Play a youtube video"),
    ("run command", run_command, "Run a cmd command"),
    ("start", start_program, "Start a program"),
    ("show me what you got", me_irl, "Lets meme"),
    ("open my email", open_email, "Open Thunderbird"),
    ("open my drive", open_gdrive, "Open Google Drive"),
    ("itunes", play_itunes_music, "Play music in iTunes"),
    ("what's the weather like", get_weather,"Weather Forecast"),
    ("stop listening", pause_listener, "Stop Listening"),
    ("set timer", set_timer, "Start a timer"),
    ("answer this", query_wolfram, "Ask wolfram a question"),
]
speech_tracks = {
    "WELCOME": "resources\\audio_clips\\welcome.wav",
    "WAKE": "resources\\audio_clips\\how_can_i_help.wav", #Played when listener is woken by key_phrase
    "NOT_RECOGNISED": "resources\\audio_clips\\i_dont_understand.wav", #Played when a phrase isn't recognised
}
