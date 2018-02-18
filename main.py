#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from googletrans import Translator
import random
import config
import readline

traductor = Translator()
lines = []
fails = []
dict_lang = ""
qust_lang = ""
transl_to = ""
randomize = False
restart_f = False


def game_ended():
	if len(fails) == 0:
		print "YOU WIN!"
		sys.exit()
	else:
		chooseMode()

def game_stopped():
	print "\nGame stopped"
	print "Fails: ",str(fails)
	chooseMode()


def game():
	fails = []
	print "\nGame starts\n"
	if randomize:
		random.shuffle(lines)
	for l in lines:
		if dict_lang != transl_to:
			correct_answer = traductor.translate(l, dest=transl_to, src=dict_lang).text.encode("utf-8").decode("utf-8").encode("utf-8").lower()
		else:
			correct_answer = l
		if dict_lang != qust_lang:
			question = traductor.translate(l, dest=qust_lang, src=dict_lang).text.encode("utf-8").decode("utf-8").encode("utf-8").lower()
			answer = raw_input(question+": ").lower()
		else:
			question = l
			answer = raw_input(question+": ").lower()
		if answer == "stop":
			game_stopped()
		if answer != correct_answer:
			print "Failed! Answer: "+ correct_answer.upper()
			fails.append(l)
			if restart_f:
				game()
	game_ended()


def failmode():
	print "\nFail Game starts\n"
	random.shuffle(fails)
	for l in fails:
		answer = raw_input(l+": ").lower()
		translated = traductor.translate(l, dest=transl_to, src=qust_lang).text.encode("utf-8").decode("utf-8").encode("utf-8").lower()
		if answer != translated:
			print "\nFailed! Answer: "+ translated.upper()
		else:
			fails.remove(l)
	game_ended()



def chooseMode():
	mode = raw_input("Choose mode: \n 1) All words \n 2) Failed words (first play mode 1) \nHint: Answer 'stop' to choose mode.\n\nElection (1/2):")
	if mode == "1":
		game()
	elif mode == "2":
		failmode()
	else:
		print "Unknown mode"


def setup():
	global dict_lang, qust_lang, transl_to, randomize, restart_f, lines
	dict_name = raw_input("Dictionary file path:    ") if config.dict_name == "" else config.dict_name
	dict_lang = raw_input("Dictionary language:     ") if config.dict_lang == "" else config.dict_lang
	qust_lang = raw_input("Ask in:                  ") if config.qust_lang == "" else config.qust_lang
	transl_to = raw_input("Translate to:            ") if config.transl_to == "" else config.transl_to
	randomize = raw_input("Random order [y/N]:      ") if config.randomize == "" else config.randomize
	restart_f = raw_input("Restart afer fail [y/N]: ") if config.restart_f == "" else config.restart_f
	if randomize.lower() == "y" or randomize.lower() == "yes":
		randomize = True
	else:
		randomize = False
	if restart_f.lower() == "y" or restart_f.lower() == "yes":
		restart_f = True
	else:
		restart_f = False
	try:
		lines = open(dict_name).read().splitlines()
	except:
		print "Could not open file"+str(dict_name)+". Check the path exists"
		sys.exit()


def main():
	setup()
	#chooseMode()
	game()



if __name__ == "__main__":
	main()