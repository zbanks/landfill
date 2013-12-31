#!/usr/bin/python

import pool
import time

p=pool.Pool()

def do(cmd):
	print p.doCommand(cmd)

def spin(cmd,secs,freq): 
	for i in range(secs*freq): 
		do(cmd)
		time.sleep(1.0/freq)

#do({"cmd":"add","args":{"type":"add_movie","args":{"local_file":"../testing/diehard_clip.avi","info":{"title":"die hard"}}}})
do({"cmd":"add","args":{"type":"add_imdb","args":{"local_file":"bbtest.mkv","imdb":"http://www.imdb.com/title/tt0903747/"}}})
spin({"cmd":"pool"},300,2)
#do({"cmd":"rm","args":{"uid":0}})
#spin({"cmd":"pool"},3,2)
