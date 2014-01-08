#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" system """
import logging as log
import collections

""" package """
import lib.yaml as yaml


configs = {}

def add(config_file):
	global configs
	log.debug('config.add %s',config_file)
	
	f = open(config_file)
	config = yaml.safe_load(f)
	f.close()
	
	update(config)

def update(config):
	global configs
	log.debug('config.update %s',config)
	if(config != None):
		_r_update(configs, config)

def _r_update(d, u):
	for k, v in u.iteritems():
		if isinstance(v, collections.Mapping):
			r = _r_update(d.get(k, {}), v)
			d[k] = r
		else:
			d[k] = u[k]
	return d

def get(path):
	global configs
	keys = path.split('.')
	keys.reverse()
	return _r_get(configs,keys)
	
def _r_get(segment,keys):
	try:
		key = keys.pop()
	except IndexError:
		return segment
	
	try:
		next_segment = segment[key]
	except:
		#log.warning('core._r_config No result with key "%s"',key)
		return None
	
	return _r_get(next_segment,keys)

def clear():
	global configs
	configs = {}