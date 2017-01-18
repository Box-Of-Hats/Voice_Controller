from gtts import gTTS
import os
import winsound
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("text")
args = parser.parse_args()


fname = args.text
fname = fname.replace(" ", "_")

tts = gTTS(text='{}'.format(args.text), lang='en')
tts.save("{}.mp3".format(fname))

os.system(".\\ffmpeg\\bin\\ffmpeg -loglevel panic -i {}.mp3 -acodec pcm_u8 -ar 22050 {}.wav -y".format(fname, fname))
winsound.PlaySound('{}.wav'.format(fname), winsound.SND_FILENAME)
