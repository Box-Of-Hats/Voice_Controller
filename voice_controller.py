import speech_recognition as sr
import winsound
from config import actions, key_phrase, audio_out, speech_tracks

from VoiceController import VoiceController, speaker_factory

listening = True #Set to False to end program

def main():

    speaker = speaker_factory(audio_out, speech_tracks)
    vc = VoiceController( actions, speaker, key_phrase)
    for line in vc.about_text(): print(line)
    while listening:
        vc.do_voice_command()


if __name__ == "__main__":
    main()
