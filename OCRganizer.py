from os import listdir
import os
from os.path import isfile, join
from time import sleep
import fileinput
import sys
from re import search, sub
import eyed3
import shutil

mypath = os.getcwd()
eyed3.log.setLevel("ERROR")

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def sanitize_name(album):
	return sub(r'[^A-Za-z0-9\s-]', '', album).rstrip()

print "Starting..."

for i in onlyfiles:
	print i
	if i.endswith('.mp3'):
		audiofile = eyed3.load(i)
		print "Loaded {0}".format(i)
		res =  search(r"(.*)\s'(.*)'\s.*", audiofile.tag.title)
		if res:
			album, title = res.groups()

			# Strip non-alphanumerics from album to avoid directory issues
			directory = sanitize_name(album)
			filename = sanitize_name(title)

			print "Song's new filename: {0}. Directory: {1}".format(filename, directory)

			audiofile.tag.title = title
			audiofile.tag.album = album
			try:
				audiofile.tag.save()
			except eyed3.id3.tag.TagException:
				pass
		else:
			# This file has already been processed but not put into
			# sub-directory.
			directory = sanitize_name(audiofile.tag.album)
			filename = sanitize_name(audiofile.tag.title)

			print "File processed. Renaming to {0} and moving to {1}".format(filename, directory)

		if not os.path.exists(directory):
			os.makedirs(directory)

		os.rename(i, "{0}/{1}.mp3".format(directory, filename))

	else:
		continue




