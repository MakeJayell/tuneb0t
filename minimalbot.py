

from pydub import AudioSegment


#sound1 = AudioSegment.from_file("drums.mp3")
#sound2 = AudioSegment.from_file("piano.mp3")

#combined = sound1.overlay(sound2) - this works.

#combined.export("finalsong.mp3", format='mp3') - this works.

# Try to do the above but by defining the 'sound' variables randomly :

import random

#sound3 = ['drums.mp3', 'piano.mp3']
#sound4 = ['lead.mp3', 'chip.mp3']

#tempo to milliseconds conversion
onebeat = 60 / 125
bar = onebeat * 4
beatms = bar * 1000


import os, sys

def extension(file):
    ext = os.path.splitext(file)[-1].lower()
    return ext

soundstore = {
    "loop1" : "/Users/jake/documents/tunebot/sound1",
    "loop2" : "/Users/jake/documents/tunebot/sound2",
    "loop3" : "/Users/jake/documents/tunebot/sound3",
    "loop4" : "/Users/jake/documents/tunebot/sound4"
}
 
#if they are .mp3s continue as normal, if not re-select a file
for count, (instrument, path) in enumerate(soundstore.items()):
    print("Randomly choosing a %s track" % instrument)
    random_track = random.choice(os.listdir(path))
    while extension(random_track) != ".mp3":
        random_track = random.choice(os.listdir(path))
    else: 
        randomobj = AudioSegment.from_mp3(os.path.join(str(path), random_track)) * 8
 
    if count == 0:
      mix = randomobj
    else:
      mix = mix.overlay(randomobj, position=(beatms * 4) )



#define the random variables above as sounds
#soundx = AudioSegment.from_mp3(random1)
#soundy = AudioSegment.from_mp3(random2)

#print(random.choice(sound3)) - These both work and randomly print the names of the sounds
#print(random.choice(sound4))



#generate blocks of silence

bar_of_silence = AudioSegment.silent(duration=beatms) # or be explicit
phrase_of_silence = bar_of_silence * 4

#need to write some code to randomly select these for everything after the drum track
fourbar = beatms * 4
eightbar = beatms * 8
sixteenbar = beatms * 16
twentyfourbar = beatms * 24
thirtytwobar = beatms * 32
fourtybar= beatms * 40

#Generate the random title of the track and the variables to use later i.e. the finaltitlefortweet
#NEED TO FIX, THIS OCCASIONALLY ONLY GRABS ONE WORD INSTEAD OF TWO
import requests

wordpage = "http://www.jakemayell.com/tunebot/words/words.html"
adjectivepage = "http://www.jakemayell.com/tunebot/words/adjectives.html"

words = requests.get(wordpage)
adjectives = requests.get(adjectivepage)

finalword = words.content.splitlines()
finaladjective = adjectives.content.splitlines()

word = random.choice(finalword)
adjective = random.choice(finaladjective)

finaltitle = adjective.decode() + ' ' + word.decode()
finaltitlefortweet = adjective.decode() + '-' + word.decode()

#Export the final combined file
mix.export(finaltitle + ".mp3", format='mp3')


#~~~~~~~~~~IMAGE GEN~~~~~~~~~~~#

import glitch
theglitcher = glitch.Glitch()
theglitcher.trigger(None, keyword=adjective,finalfilename= finaltitle + '.jpg')


#~~~~~~~~~~SOUNDCLOUD~~~~~~~~~~#

from secretstuff import scclientid, scclientsecret, scusername, scpassword
import soundcloud

# create client object with app and user credentials
client = soundcloud.Client(client_id=scclientid,
                           client_secret=scclientsecret,
                           username=scusername,
                           password=scpassword)

#Upload the track with details to SoundCloud
track = client.post('/tracks', track={
    'title': finaltitle,
    'sharing': 'private',
    'genre' : 'Electronic',
    'tag_list' : 'Robot Dynamic Python Loops Random minimal',
    'asset_data': open(finaltitle + ".mp3", 'rb'),
    'artwork_data': open(finaltitle + '.jpg', 'rb')
})


print('OK! Just uploaded ' + finaltitle)

#~~~~~~~~~~TWITTER~~~~~~~~~~#

#Load the API keys
from secretstuff import appkey, appsecret, authtoken, authsecret

from twython import Twython

APP_KEY = appkey
APP_SECRET = appsecret
OAUTH_TOKEN = authtoken
OAUTH_TOKEN_SECRET = authsecret

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


#Build and post the actual tweet containing the URL to the track on SoundCloud
#IS THERE A TIDIER WAY TO DO THIS I.E. USING SOUNDCLOUDS RESOLVE(?) FUNCTION?
twitter.update_status(status='tuneb0t made a tune : ' + track.permalink_url)
