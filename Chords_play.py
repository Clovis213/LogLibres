# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 16:13:17 2021

@author: chiapelg
"""

import speech_recognition as sr
import numpy as np
import pygame

#initialisation micro pour reconnaissance vocale :
micro = sr.Microphone()
#micro = sr.AudioFile("test.wav")
r = sr.Recognizer()

# initialisation mixer pygame : fréquence echantillonnage, taille, channels, buffer
pygame.mixer.init(44100,-16,2,512)

#Vitesse de lecture des accords (ms)
VITESSE = 500

#liste de notes
notes = [["C", 261.63],
		["C sharp",277.18],
		["D",293.66],
		["D sharp",311.13],
		["E",329.63],
		["F",349.23],
		["F sharp",369.99],
		["G",392.00],
		["G sharp",415.30],
		["A",440.0],
		["A sharp",466.16],
		["B",493.88]]

# autres variables :
val = 13	#numéro de note
mode = ""	#majeur ou mineur
sept = 0	#pas de septieme


# crée une note jouable avec PyGame
class Note:
	
	def __init__(self, freq):
		self.sampleRate = 44100
		self.freq = freq
		
		self.arr = np.array([4096 * np.sin(2.0 * np.pi * self.freq * x / self.sampleRate) for x in range(0, self.sampleRate)]).astype(np.int16)
		self.arr2 = np.c_[self.arr,self.arr]
		self.sound = pygame.sndarray.make_sound(self.arr2)
		

# fonction qui joue un accord donné en entrée
def jouer_accord(val, mode, seven):
	depassement_sept = 0
	
	# création de l"accord :
	fond = notes[val%12][1]	#fondamentale
	print(notes[val%12][0])
	
	if(mode == "minor"):
		tier = notes[(val+3)%12][1]	#tierce mineure
		depassement_tier = 8
		print(notes[(val+3)%12][0])
	else:
		tier = notes[(val+4)%12][1]	#tierce majeure
		depassement_tier = 7
		print(notes[(val+4)%12][0])
	
	quint = notes[(val+7)%12][1]	#quinte
	print(notes[(val+7)%12][0])
	
	if(seven == "min"):
		sept = notes[(val+10)%12][1]	#septième mineure
		depassement_sept = 1
		print(notes[(val+10)%12][0])
	elif(seven == "maj"):
		sept = notes[(val+11)%12][1]	#septième majeure
		depassement_sept = 0
		print(notes[(val+11)%12][0])
	else:
		sept = 0
	
	# pas de renversement d"accords:
	if(val>depassement_tier):
		tier *= 2
	if(val>4):
		quint *= 2
	if(val>depassement_sept):
		sept *= 2
	
	# déclaration des trois objets :
	note1 = Note(fond)
	note2 = Note(tier)
	note3 = Note(quint)
	note4 = Note(sept)

	# début routine de jeu d"accord :
	note1.sound.play(-1)	#jouer fondamentale
	pygame.time.delay(VITESSE)
	note1.sound.stop()

	note2.sound.play(-1)	#jouer tierce
	pygame.time.delay(VITESSE)
	note2.sound.stop()

	note3.sound.play(-1)	#jouer quinte
	pygame.time.delay(VITESSE)
	note3.sound.stop()
	
	if(seven!=0):
		note4.sound.play(-1)	#jouer septième, s'il y a
		pygame.time.delay(VITESSE)
		note4.sound.stop()
		

	pygame.time.delay(int(VITESSE*0.7))

	#accord entier
	note1.sound.play(-1)
	note2.sound.play(-1)
	note3.sound.play(-1)
	if(seven!=0):
		note4.sound.play(-1)
	
	pygame.time.delay(VITESSE*2)
	
	note1.sound.stop()
	note2.sound.stop()
	note3.sound.stop()
	note4.sound.stop()
	# fin routine


### début programme principal ###
while(1):
	#In english :
	with micro as source:
		print("Speak!")
		audio_data = r.listen(source)
		print("End!")
		
	try :
		phrase = " "+r.recognize_google(audio_data)+" "	#on ajoute des espaces pour optimiser le traitement
		print (">", phrase)
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))


	#recherche de la fondamentale
	# analyse de la phrase donnée :
	for i in range(12):	#on cherche la note
		if(" "+notes[i][0]+" " in phrase):
			val = i
		elif(" "+notes[i][0]+"7 " in phrase):
			val = i

	#nouvelle recherche en minuscule cette fois :
	if(val == 13):
		for i in range(12):	#on cherche la note
			if((" "+notes[i][0].lower()+" ") in phrase):
				val = i
			elif((notes[i][0].lower()+"-sharp") in phrase):
				val = i+1
			
	#cas particuliers :
	if(val == 13):
		if("imgur" in phrase):
			val = 4
		elif("Amina" in phrase):
			val = 4
		elif("fmaj7" in phrase):
			val = 5


	#Retour sur la phrase
	if(val == 13):
		print("aille aille aille, j'ai rien compris")
	else:
		#vérification mineur/majeur
		if(("minor" in phrase)|("Minor" in phrase)):
			mode = "minor"
		elif("imgur" in phrase):	#cas particulier
			mode = "major"
		elif("Amina" in phrase):	#cas particulier
			mode = "minor"
		elif("fmaj7" in phrase):	#cas particulier
			mode = "major"
		else:
			mode = "major"
		#vérification septième
		if((" major seven " in phrase) or (" major 7 " in phrase) or ("maj7" in phrase)):
			sept = "maj"
			print("bien entendu, je vais te jouer un", notes[val][0], mode, "maj7")
		elif((" seven " in phrase) or ("7" in phrase)):
			sept = "min"
			print("bien entendu, je vais te jouer un", notes[val][0], mode, "7")
		else:
			print("bien entendu, je vais te jouer un", notes[val][0], mode)
		
		#lancement des accords
		jouer_accord(val,mode,sept)

	val=13
	sept = 0

### fin programme principal ###
