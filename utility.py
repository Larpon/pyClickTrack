#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def file_split(filename):
	basename = os.path.basename(filename)
	file, extension = os.path.splitext(basename)
	return (file, extension)

def file_exists(path):
	if os.path.isfile(path):
		try:
			with open(path):
				return True;
		except IOError:
			return False;
