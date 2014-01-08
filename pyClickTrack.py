#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" system """
import os
import logging as log
import sys
import math

""" package """
import utility
import config
from lib.pydub import AudioSegment

import pygame


def build(path):
	config.clear()
	config.add(path)
	filename, extension = utility.file_split(path)
	"""
	pygame.init()
	pygame.mixer.music.load("data/ping_high.wav")
	pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
	pygame.event.set_allowed(pygame.constants.USEREVENT)
	pygame.mixer.music.play()
	pygame.event.wait()
	"""
	parts = config.get('track.parts')
	silence = config.get('track.silence')
	outfile = filename+'.wav'
	
	hi = AudioSegment.from_wav("data/ping_hi.wav")
	lo = AudioSegment.from_wav("data/ping_lo.wav")
	
	track = AudioSegment.silent(silence)
	for part in parts:
		name = part['part']
		bpm = part['bpm']
		bar = part['bar']
		bars = part['bars']
		
		# Beats per second
		bps = float(bpm) / 60
		# Beats per bar
		bpb = float(len(bar))
		# Beats = bars * beats per bar
		beats = float(bars) * bpb
		# Length (in seconds)
		length = float(beats) / bps
		# Bar length (in milliseconds)
		bar_length = ((length / bars) / bpb) * 1000
		
		
		log.debug('Building "%s" as %s/%s @ %sbpm. %sbps %sbpb %sbeats, length: %s, bar length:%s',name,bars,bpb,bpm,bps,bpb,beats,length,bar_length)
		
		for b in range(0, bars):
			for symbol in bar:
				tick = hi
				if symbol == '-':
					tick = lo
				tick_length = len(tick)
				pad = AudioSegment.silent(round(bar_length - tick_length))
				
				click = tick + pad
				track += click

	if utility.file_exists(outfile):
		os.unlink(outfile)
	track.export(outfile,format="wav")

def main():
	FORMAT = '%(asctime)s - %(levelname)s\t- %(message)s'
	log.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S',level=log.DEBUG)
	logger = log.getLogger(__name__)
	
	file = None
	try:
		file = sys.argv[1]
	except IndexError:
		file = None
	
	if file:
		build(file)
	else:
		log.info('No file specified to make click track from')

if __name__ == "__main__":
	pwd = os.path.dirname(os.path.realpath(__file__))
	main()
