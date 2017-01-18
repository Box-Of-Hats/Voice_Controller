import speech_recognition as sr
import winsound
from config import *
from gtts import gTTS
import os



class VoiceController():
    def __init__(self, actions, speaker, key_phrase=''):
        self.actions = actions
        self.speaker = speaker
        self.key_phrase = key_phrase.lower()


    def about_text(self):
        if self.key_phrase:
            yield "Key Phrase: {}".format(key_phrase)
            yield ""
        for action_tuple in self.actions:
            yield "\t{:25}:\t{}".format('"{}"'.format(action_tuple[0]), action_tuple[2])

    def listen(self):
        #Listen for audio input with default microphone device and return the string if detected
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
        
        try:
            audio_input = r.recognize_google(audio)
            print("Heard: \"{}\"".format(audio_input))
            return audio_input.lower()
    
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return False
    
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return False
    
        except KeyError:
            return False

    def parse_speech(self, phrase):
        phrase = phrase.lower()
        for tup in self.actions:
            if tup[0] in phrase:
                input_phrase = phrase.replace(tup[0], '').strip()
                return tup[1](input_phrase)
    
        return False

    def do_voice_command(self):
        voice_input = self.listen()
        if (voice_input and self.key_phrase in voice_input):
            self.speaker.play_track('WAKE')
            voice_input = self.listen()
            command = voice_input.replace(self.key_phrase, '').strip() #remove key phrase from input phrase to give only command
            response = self.parse_speech(command)
            if response:
                self.speaker.text_to_speech(response)
            return response



class SpeechSpeaker():
    def __init__(self, tracks=False):
        self.tracks = tracks

    def text_to_speech(self, text):
        #Speak (Text to speech) a given text
        tts = gTTS(text=text, lang='en')
        tts.save("output_audio.mp3")
        
        os.system(".\\ffmpeg\\bin\\ffmpeg -loglevel panic -i output_audio.mp3 -acodec pcm_u8 -ar 22050 output_audio.wav -y")
        winsound.PlaySound('output_audio.wav', winsound.SND_FILENAME)

    def play_file(self, filepath):
        winsound.PlaySound(filepath, winsound.SND_FILENAME)

    def play_track(self, trackname):
        winsound.PlaySound(self.tracks[trackname], winsound.SND_FILENAME)

class BeepSpeaker():
    def __init__(self, tracks=False):
        self.tracks = tracks

    def text_to_speech(self, text):
        winsound.Beep(600,200)
        winsound.Beep(600,200)

    def play_file(self, filepath):
        winsound.Beep(600,200)
        winsound.Beep(600,200)

    def play_track(self, trackname):
        winsound.Beep(600,200)
        winsound.Beep(600,200)

class MuteSpeaker():
    def __init__(self, args="ignore"):
        pass

    def text_to_speech(self, args="ignore"):
        pass

    def play_file(self, args="ignore"):
        pass

    def play_track(self, args="ignore"):
        pass

def speaker_factory(speaker_type, speech_tracks=False):
    if speaker_type == 0:
        return MuteSpeaker()
    elif speaker_type == 1:
        return BeepSpeaker()
    elif speaker_type == 2:
        return SpeechSpeaker(speech_tracks)
    else:
        return False