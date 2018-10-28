import speech_recognition as sr
import winsound
from enum import Enum
from gtts import gTTS
import os
from VoiceAction import VoiceAction
import re

class VoiceController():
    def __init__(self, actions, speaker, input_device, key_phrases=''):
        self.actions = actions
        self.actions.append(VoiceAction("what can you do",
                                        self.about_text, "Show this about text"))
        self.speaker = speaker

        self.key_phrases = key_phrases

        self.input_device = input_device

    def about_text(self, args="ignore"):
        """
        Generator: yields about text for the current VoiceController
        """
        if self.key_phrases:
            print("Key Phrase: {}".format(self.key_phrases))
            print("")

        for action in self.actions:
            print(action.match_patterns, action.about_text)

        return "Here's a list of the things I can do"

    def parse_speech(self, phrase):
        """
        Takes an input string 'phrase' and performs the appropriate action, definied by 'actions' if available.
        """
        phrase = phrase.lower()
        for action in self.actions:
            # if phrase.startswith(tup[0]):
            #    input_phrase = phrase.replace(tup[0], '').strip()
            #    return tup[1](input_phrase)
            matched_pattern = action.is_match(phrase)
            if matched_pattern:
                kwargs = action.get_values(phrase, matched_pattern)
                return action.execute(kwargs)

        return False

    def do_voice_command(self):
        """
        Listens for voice input on default microphone device, then performs the appropriate action defined by 
        'actions' if one is found.
        """
        voice_input = self.input_device.take_input()

        if voice_input:
            if self.contains_key_phrase(voice_input):#(self.contains_key_phrase(voice_input) and (len(voice_input) == len(self.contains_key_phrase(voice_input)))):
                
                # When phrase only contains the key phrase, acknowledge and wait for further input
                self.speaker.play_track('WAKE')
                print("How can I help?")
                voice_input = self.input_device.take_input()
                response = self.parse_speech(voice_input)
                if response:
                    #print('\tA: {}'.format(response))
                    self.speaker.text_to_speech(response)
                else:
                    self.speaker.play_track("NOT_RECOGNISED")
                return response

            elif (self.contains_action(voice_input) and self.contains_key_phrase(voice_input)):
                # When phrase contains key phrase and a valid action, just perform the action
                found_action = self.contains_action(voice_input)
                found_kp = self.contains_key_phrase(voice_input)
                response = self.parse_speech(
                    voice_input.replace(found_kp, '').strip())
                if response:
                    print('\tA: {}'.format(response))
                    self.speaker.text_to_speech(response)
                else:
                    self.speaker.play_track("NOT_RECOGNISED")
                return response

            else:
                return False
        else:
            # No voice input detected
            return False

    def contains_key_phrase(self, check_phrase):
        """ Checks if there is a key phrase in a check phrase and returns the key phrase if found. """
        for key_phrase in self.key_phrases:
            if re.match(key_phrase, check_phrase):
                return key_phrase
        return False

    def contains_action(self, phrase):
        """ Checks if there is an action in a check phrase and returns the action if found. """
        for action in self.actions:
            if action.is_match(phrase):
                return action
        return False

# region input devices


class InputDeviceType(Enum):
    MICROPHONE = 0
    CONSOLE = 1


class InputDevice():
    def __init__(self):
        pass

    def take_input(self):
        raise NotImplementedError

    def make_device(device_type):
        if device_type in (InputDeviceType.MICROPHONE, InputDeviceType.MICROPHONE.value):
            return Microphone()
        elif device_type in (InputDeviceType.CONSOLE, InputDeviceType.CONSOLE.value):
            return Console()
        else:
            print("Invalid input device type given: {0}".format(device_type))
            print("Device type must be one of:")
            for dt in InputDeviceType:
                print("    {0}".format(dt))
            return False


class Console(InputDevice):
    def take_input(self):
        return input(">")


class Microphone(InputDevice):
    def __init__(self):
        self.voice_recogniser = sr.Recognizer()

        # Parts below can be removed and the voicecontroller will still work.
        # These are just an attempt at making the mic work better
        # Attempt to stop hanging.
        self.voice_recogniser.dynamic_energy_threshold = False
        self.energy_threshold = 400

        m = sr.Microphone()
        with m as source:
            # we only need to calibrate once, before we start listening
            self.voice_recogniser.adjust_for_ambient_noise(source)

    def take_input(self):
        """
        Listen for audio input with default microphone device and return the string if recognised by Google Speech Recognition.
        """
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.voice_recogniser.listen(source)
            print("Recognising...")

        try:
            audio_input = self.voice_recogniser.recognize_google(audio)
            print("Heard: \"{}\"".format(audio_input))
            return audio_input.lower()

        except sr.UnknownValueError:
            print("Could not understand audio.")
            return False

        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))
            return False

        except KeyError:
            return False

# endregion

# region Speakers


class SpeakerType(Enum):
    MUTE = 0
    BEEP = 1
    SPEECH = 2


class Speaker():
    """
    Base class for speaker output.
    """

    def __init__(self, args):
        pass

    def text_to_speech(self, text):
        # Play a specific line of text
        raise NotImplementedError

    def play_file(self, filepath):
        # Play a sound file
        raise NotImplementedError

    def play_track(self, trackname):
        # Play a given track by it's name
        raise NotImplementedError

    def make_speaker(speaker_type, speech_tracks=False, ffmpeg_path='.'):
        if speaker_type in (SpeakerType.MUTE, SpeakerType.MUTE.value):
            return MuteSpeaker()
        elif speaker_type in (SpeakerType.BEEP, SpeakerType.BEEP.value):
            return BeepSpeaker()
        elif speaker_type in (SpeakerType.SPEECH, SpeakerType.SPEECH.value):
            return SpeechSpeaker(speech_tracks, ffmpeg_path)
        else:
            print("Invalid speaker type given: {0}".format(speaker_type))
            print("Speaker must be one of:")
            for v in SpeakerType:
                print("    {0}".format(v))
            return False


class SpeechSpeaker(Speaker):
    def __init__(self, tracks={}, ffmpeg_path='.'):
        self.tracks = tracks
        self.ffmpeg_path = ffmpeg_path

    def text_to_speech(self, text):
        # Speak (Text to speech) a given text
        try:
            tts = gTTS(text=text, lang='en')
            tts.save("output_audio.mp3")

            os.system(
                "{} -loglevel panic -i output_audio.mp3 -acodec pcm_u8 -ar 22050 output_audio.wav -y".format(self.ffmpeg_path))
            winsound.PlaySound('output_audio.wav', winsound.SND_FILENAME)
            os.remove("output_audio.wav")
            os.remove("output_audio.mp3")
        except AttributeError:
            # Issue with gTTs
            pass

    def play_file(self, filepath):
        winsound.PlaySound(filepath, winsound.SND_FILENAME)

    def play_track(self, trackname):
        winsound.PlaySound(self.tracks[trackname], winsound.SND_FILENAME)


class BeepSpeaker(Speaker):
    def __init__(self, args="ignore"):
        pass

    def text_to_speech(self, text):
        winsound.Beep(600, 200)
        winsound.Beep(600, 200)

    def play_file(self, filepath):
        winsound.Beep(600, 200)
        winsound.Beep(600, 200)

    def play_track(self, trackname):
        winsound.Beep(600, 200)
        winsound.Beep(600, 200)


class MuteSpeaker(Speaker):
    def __init__(self, args="ignore"):
        pass

    def text_to_speech(self, text):
        print(text)

    def play_file(self, args="ignore"):
        pass

    def play_track(self, args="ignore"):
        pass

# endregion
