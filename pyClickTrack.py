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

#import pygame

def sound_dict(value):
	displacement = 0
	sound = AudioSegment.silent(0)
	if type(value) is list:
		try:
			displacement = int(value[0])
			sound = AudioSegment.from_wav(value[1])
		except ValueError:
			displacement = int(value[1])
			sound = AudioSegment.from_wav(value[0])
	else:
		sound = AudioSegment.from_wav(value)
	
	return { 'sound' : sound, 'displacement' : displacement } 

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
	
	
	parts = {}
	sounds = {
		'+' : sound_dict("data/click_hi.wav"),
		'-' : sound_dict("data/click_lo.wav")
	}
	silence = 0
	outfile = filename+'.wav'
	
	
	if config.has('track.parts'):
		parts = config.get('track.parts')
	if config.has('track.silence'):
		silence = config.get('track.silence')
	if config.has('track.sounds'):
		custom_sounds = config.get('track.sounds')
		for k,v in custom_sounds.iteritems():
			sounds[k] = sound_dict(v)
	
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
				try:
					sound = sounds[symbol]
				except KeyError:
					sound = sounds['+']
					
				tick = sound['sound']
				tick_displacement = sound['displacement']
				
				if len(tick) < bar_length:
					fill = round(bar_length - len(tick))
					pad = AudioSegment.silent(fill)
					tick = tick + pad
				if len(tick) > bar_length:
					tick = tick[:bar_length]
				#log.debug("before track: %s tick: %s displace: %s",len(track),len(tick),tick_displacement)
				if len(track) >= tick_displacement and tick_displacement > 0:
					mix_from = len(track)-tick_displacement
					track += AudioSegment.silent(len(tick)-tick_displacement)
					track = track.overlay(tick, position=mix_from)
				else:
					displace = len(tick) - tick_displacement
					if displace < len(tick):
						tick = tick[displace:]
					track += tick
					
				#log.debug("after track: %s tick: %s displace: %s",len(track),len(tick),tick_displacement)
					
				#track += click

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
