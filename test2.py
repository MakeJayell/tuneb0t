

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

#select the random samples from a directory
samples = "/Users/jake/documents/tunebot/samples"
samples2 = "/Users/jake/documents/tunebot/samples2"

random1 = random.choice(os.listdir(samples))
random2 = random.choice(os.listdir(samples2))

print(random1)
print(random2)

#define the random variables above as sounds
soundx = AudioSegment.from_mp3(random1)
soundy = AudioSegment.from_mp3(random2)

#print(random.choice(sound3)) - These both work and randomly print the names of the sounds
#print(random.choice(sound4))

combined = soundx.overlay(soundy) #This doesn't work. I don't think it recognises sound 3 and 4 as audio (gives error that it's a list item)

combined.export("truerandom1.mp3", format='mp3') #This doesn't work obviously as the above doesn't work.