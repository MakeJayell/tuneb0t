

from pydub import AudioSegment


#sound1 = AudioSegment.from_file("drums.mp3")
#sound2 = AudioSegment.from_file("piano.mp3")

#combined = sound1.overlay(sound2) - this works.

#combined.export("finalsong.mp3", format='mp3') - this works.

# Try to do the above but by defining the 'sound' variables randomly :

import random

#sound3 = ['drums.mp3', 'piano.mp3']
#sound4 = ['lead.mp3', 'chip.mp3']

import os, sys

def extension(file):
    ext = os.path.splitext(file)[-1].lower()
    return ext

#define the directories
sound1 = "/Users/jake/documents/tunebot/sound1"
sound2 = "/Users/jake/documents/tunebot/sound2"
sound3 = "/Users/jake/documents/tunebot/sound3"
sound4 = "/Users/jake/documents/tunebot/sound4"


#Randomly select the files
random1 = random.choice(os.listdir(sound1))

#if they are .mp3s continue as normal, if not re-select a file - make this a function to use for each sound later
while extension(random1) != ".mp3":
	random1 = random.choice(os.listdir(sound1))

else: random1obj = AudioSegment.from_mp3(os.path.join(str(sound1), random1)) * 8


random2 = random.choice(os.listdir(sound2))

while extension(random2) != ".mp3":
	random2 = random.choice(os.listdir(sound2))

else: random2obj = AudioSegment.from_mp3(os.path.join(str(sound2), random2))


random3 = random.choice(os.listdir(sound3))

while extension(random3) != ".mp3":
	random3 = random.choice(os.listdir(sound3))

else: random3obj = AudioSegment.from_mp3(os.path.join(str(sound3), random3))


random4 = random.choice(os.listdir(sound4))

while extension(random4) != ".mp3":
	random4 = random.choice(os.listdir(sound4))

else: random4obj = AudioSegment.from_mp3(os.path.join(str(sound4), random4))

random5 = random.choice(os.listdir(sound5))

while extension(random5) != ".mp3":
	random5 = random.choice(os.listdir(sound5))

else: random5obj = AudioSegment.from_mp3(os.path.join(str(sound5), random5))

random6 = random.choice(os.listdir(sound6))

while extension(random6) != ".mp3":
	random4 = random.choice(os.listdir(sound6))

else: random6obj = AudioSegment.from_mp3(os.path.join(str(sound6), random6))

random7 = random.choice(os.listdir(sound7))

while extension(random7) != ".mp3":
	random7 = random.choice(os.listdir(sound7))

else: random7obj = AudioSegment.from_mp3(os.path.join(str(sound7), random7))

random7 = random.choice(os.listdir(sound8))

while extension(random8) != ".mp3":
	random8 = random.choice(os.listdir(sound8))

else: random8obj = AudioSegment.from_mp3(os.path.join(str(sound8), random8))


#Once the random filename has been selected above, actually load it as an audio segment from the relevant folder

#Print names of files. Just to test
print(random1)
print(random2)
print(random3)
print(random4)

#define the random variables above as sounds
#soundx = AudioSegment.from_mp3(random1)
#soundy = AudioSegment.from_mp3(random2)

#print(random.choice(sound3)) - These both work and randomly print the names of the sounds
#print(random.choice(sound4))

#tempo to milliseconds conversion
onebeat = 60 / 125
bar = onebeat * 4
beatms = bar * 1000
print(onebeat)
print(bar)

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

#intro = random1obj
#verse = random2obj


#Combine the two files

combined1 = random1obj.overlay(random2obj * 32, position=fourbar) #WHY DOESNT THIS WORK??!!?
combined2 = combined1.overlay(random3obj * 32, position=eightbar) 
combined3 = combined2.overlay(random4obj * 32, position=sixteenbar)
combined4 = combined3.overlay(random5obj * 32, position=twentyfourbar)
combined5 = combined4.overlay(random6obj * 32, position=thirtytwobar)
combined6 = combined5.overlay(random7obj * 32, position=fourtybar)

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

print('OK! Just uploaded ' + finaltitle)

#Export the final combined file
combined3.export("truerandom1.mp3", format='mp3')


#~~~~~~~~~~IMAGE GEN~~~~~~~~~~~#

#import glitch
#glitch.main()


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
    'asset_data': open('truerandom1.mp3', 'rb')
})




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
twitter.update_status(status='tuneb0t made a tune : https://soundcloud.com/une0t/' + finaltitlefortweet)

