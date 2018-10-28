import argparse
import json
from actions import *
from VoiceController import VoiceController, Speaker, InputDevice
from VoiceAction import VoiceAction


listening = True  # Set to False to end program


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str,
                        help="A config file to load commands from.")
    args = parser.parse_args()

    if args.config:
        config_file = args.config
    else:
        config_file = "config.json"

    actions = []
    try:
        with open(config_file, "r") as config_file:
            loaded_config = json.load(config_file)

            key_phrases = loaded_config["key_phrases"]
            audio_out_mode = loaded_config["audio_out_mode"]
            input_mode = loaded_config["input_mode"]
            ffmpeg_path = loaded_config["ffmpeg_path"]
            speech_tracks = loaded_config["speech_tracks"]

            for action in loaded_config["actions"]:

                about_text = action["about_text"]
                phrases = action["phrases"]
                function = action["function"]
                try:
                    # Kwargs are optional
                    kwargs = action["kwargs"]
                except KeyError:
                    kwargs = {}
                    pass

                actions.append(VoiceAction(match_patterns=phrases, function=eval(
                    function), about_text=about_text, kwargs=kwargs))
    except FileNotFoundError:
        print("Could not find config file '{config_file}'".format(
            config_file=config_file))
        exit()

    input_device = InputDevice.make_device(input_mode)
    speaker = Speaker.make_speaker(
        audio_out_mode, speech_tracks, ffmpeg_path)
    if not speaker:
        print("Error creating speaker")
        exit()

    vc = VoiceController(actions, speaker, input_device, key_phrases)
    vc.about_text()
    while listening:
        response = vc.do_voice_command()
        if response:
            print(response)


if __name__ == "__main__":
    main()
