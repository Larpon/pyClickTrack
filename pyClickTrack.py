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
	
	return { 'click' : sound, 'displacement' : displacement }

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
	position = len(track)
	
	clicks = 0
	
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
		# Bar length (in seconds)
		bar_length = ((length / bars) / bpb)
		#bar_length = round(bar_length_f)
		
		displacement = 0
		
		log.debug('Preparing "%s" as %s/%s @ %sbpm. %sbps %sbpb %sbeats, length: %s, bar length:%s',name,bars,bpb,bpm,bps,bpb,beats,length,bar_length)
		
		track += AudioSegment.silent((length * 1000))
		
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
		# Bar length (in seconds)
		bar_length = ((length / bars) / bpb)
		#bar_length = round(bar_length_f)
		
		displacement = 0
		
		log.debug('Building "%s" as %s/%s @ %sbpm. %sbps %sbpb %sbeats, length: %s, bar length:%s',name,bars,bpb,bpm,bps,bpb,beats,length,bar_length)
		
		for b in range(0, bars):
			for symbol in bar:
				clicks += 1
				
				try:
					sound = sounds[symbol]
				except KeyError:
					sound = sounds['+']
				
				click = sound['click']
				click_displacement = sound['displacement']
				
				track = track.overlay(click, position=(position-click_displacement))
				position += bar_length*1000
		"""
		for b in range(0, bars):
			for symbol in bar:
				bars_length += bar_length_f
				
				clicks += 1
				
				try:
					sound = sounds[symbol]
				except KeyError:
					sound = sounds['+']
				
				click = sound['click']
				click_displacement = sound['displacement']
				
				if len(click) < bar_length_f:
					fill = round(bar_length_f - len(click))
					pad = AudioSegment.silent(fill)
					click = click + pad
				
				if len(click) > bar_length_f:
					log.debug('Click %s (longer than bar) length: %s displacement: %s. Track length: %s displacement: %s',clicks,len(click),click_displacement,len(track),displacement)
					mix_long = len(track)-displacement-click_displacement
					track += AudioSegment.silent(len(click)-displacement-click_displacement)
					track = track.overlay(click, position=mix_long)
				else:
					if displacement > 0:
						log.debug('Click %s (normal, displace) length: %s displacement: %s. Track length: %s displacement: %s',clicks,len(click),click_displacement,len(track),displacement)
						mix_from = len(track)-displacement-click_displacement
						track += AudioSegment.silent(len(click)-displacement-click_displacement)
						track = track.overlay(click, position=mix_from)
					else:
						log.debug('Click %s (normal) length: %s displacement: %s. Track length: %s displacement: %s',clicks,len(click),click_displacement,len(track),displacement)
						track += click
				
				#log.debug("before track: %s click: %s displace: %s",len(track),len(click),click_displacement)
				#if len(track) >= click_displacement and click_displacement > 0:
					#mix_from = len(track)-displacement-click_displacement
					##track += AudioSegment.silent(len(click)-click_displacement)
					#track += click
				#else:
					#displace = len(click) - click_displacement
					#if displace < len(click):
						#click = click[displace:]
					#track += click
					
				
				
				#log.debug("after track: %s click: %s displace: %s",len(track),len(click),click_displacement)
				
				if len(click) > bar_length_f:
					displacement = int(round(len(click) - bar_length_f))
				else:
					displacement = 0
				#log.debug('Track displacement: %s',displacement)
					
				#track += click
			log.debug('Bars length %s Track length: %s',bars_length,len(track))
			if len(track) < bars_length:
				patch = round(bars_length - len(track))
				log.debug(patch)
				track += AudioSegment.silent(patch)
				log.debug('Click %s (end patch) length: %s displacement: %s. Track length: %s displacement: %s',clicks,len(click),click_displacement,len(track),displacement)
		"""
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
