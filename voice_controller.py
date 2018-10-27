import speech_recognition as sr
import winsound
from config import actions, key_phrase, audio_out_mode, speech_tracks, ffmpeg_path

from VoiceController import VoiceController, Speaker

listening = True #Set to False to end program

def main():

    speaker = Speaker.make_speaker(audio_out_mode, speech_tracks, ffmpeg_path)
    if not speaker:
        print("Error creating speaker")
        exit()

    vc = VoiceController( actions, speaker, key_phrase)
    vc.about_text()
    while listening:
        r = vc.do_voice_command()
        if r:
            print(r)

if __name__ == "__main__":
    main()
