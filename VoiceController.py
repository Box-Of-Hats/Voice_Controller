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

        self.actions.sort(key=lambda x: x[0])

        self.r = sr.Recognizer()


        #Parts below can be removed and the voicecontroller will still work.
        #These are just an attempt at making the mic work better
        self.r.dynamic_energy_threshold = False # Attempt to stop hanging.
        m = sr.Microphone()
        with m as source:
            self.r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening
        


    def about_text(self):
        """
        Generator: yields about text for the current VoiceController
        """
        if self.key_phrase:
            yield "Key Phrase: {}".format(key_phrase)
            yield ""
        for action_tuple in self.actions:
            yield "\t{:25}:\t{}".format('"{}"'.format(action_tuple[0]), action_tuple[2])

    def listen(self):
        """
        Listen for audio input with default microphone device and return the string if recognised by Google Speech Recognition.
        """
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.r.listen(source)
        
        try:
            audio_input = self.r.recognize_google(audio)
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
        """
        Takes an input string 'phrase' and performs the appropriate action, definied by 'actions' if available.
        """
        if phrase:
            phrase = phrase.lower()
            for tup in self.actions:
                if phrase.startswith(tup[0]):
                    input_phrase = phrase.replace(tup[0], '').strip()
                    return tup[1](input_phrase)
        return False

    def do_voice_command(self):
        """
        Listens for voice input on default microphone device, then performs the appropriate action defined by 
        'actions' if one is found.
        """
        voice_input = self.listen()
        if (voice_input and self.key_phrase in voice_input):
            self.speaker.play_track('WAKE')
            voice_input = self.listen()
            #command = voice_input.replace(self.key_phrase, '').strip() #remove key phrase from input phrase to give only command
            response = self.parse_speech(voice_input)
            if response:
                print('\tA: {}'.format(response))
                self.speaker.text_to_speech(response)
            else:
                self.speaker.play_track("NOT_RECOGNISED")
            return response

class SpeechSpeaker():
    def __init__(self, tracks=False, ffmpeg_path='.'):
        self.tracks = tracks

    def text_to_speech(self, text):
        #Speak (Text to speech) a given text
        tts = gTTS(text=text, lang='en')
        tts.save("output_audio.mp3")
        
        os.system("{} -loglevel panic -i output_audio.mp3 -acodec pcm_u8 -ar 22050 output_audio.wav -y".format(ffmpeg_path))
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

def speaker_factory(speaker_type, speech_tracks=False, ffmpeg_path='.'):
    if speaker_type == 0:
        return MuteSpeaker()
    elif speaker_type == 1:
        return BeepSpeaker()
    elif speaker_type == 2:
        return SpeechSpeaker(speech_tracks, ffmpeg_path)
    else:
        return False