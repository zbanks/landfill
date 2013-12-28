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

do({"cmd":"add","args":{"type":"add_movie","args":{"local_file":"../testing/diehard_clip.avi","info":{"title":"die hard"}}}})
spin({"cmd":"pool"},15,2)
#do({"cmd":"rm","args":{"uid":0}})
#spin({"cmd":"pool"},3,2)
