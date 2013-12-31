import threading
import time

from scrapers.add_movie import AddMovie
from scrapers.add_imdb import AddFromIMDB

import json
import os

BASEPATH=os.path.join(os.path.dirname(__file__),'..')

class Pool(object):
	params={'content_dir':os.path.join(BASEPATH,'../content'),'base_path':BASEPATH}
	scrapers=[AddMovie,AddFromIMDB]

	def __init__(self):
		self.uid=0
		self.pool=[]
		self.lock=threading.Semaphore()

	# pool command
	def get_pool(self):
		return [s._describe() for s in self.pool]

	# add command
	def add(self,type,args={}):
		s_inst=self.instantiate(type,args)
		self.pool.append(s_inst)
		return {'uid':s_inst.uid}

	def available_scrapers(self):
		return [s.TYPE_STRING for s in self.scrapers]

	def describe_scraper(self,uid):
                return self.find_s(uid)._describe()

	def rm(self,uid):
                return self.find_s(uid).rm()

	def find_s(self,uid):
		uid=int(uid)
		d=dict([(s.uid,s) for s in self.pool])
		if uid not in d:
			raise Exception("Download identifier does not exist")
		return d[uid]

	# Runs a set of commands. Pool is guarenteed to not change during them.
	def doMultipleCommandsAsync(self,commands):
		return self.sync(lambda:[self.doCommand(cmd) for cmd in commands])

	# Acquires this object's lock and executes the given cmd
	def sync(self,cmd):
		try:
			self.lock.acquire()
			result=cmd()
		except Exception:
			self.lock.release()
			raise
		self.lock.release()
		return result

	# Removes a download asynchronously
	def removeMeAsync(self,uid):
		self.sync(lambda:self.removeMe(uid))

	def removeMe(self,uid):
		self.pool=[obj for obj in self.pool if obj.uid != uid]

	# Parse and run a command
	def doCommand(self,line):
		if not isinstance(line,dict):
			return errorPacket('Command not a dict.')

		try:
			cmd=line['cmd'] # Fails if no cmd given
		except KeyError:
			return errorPacket('No command given.')

		try:
			args=line['args']
		except KeyError:
			args={}

		if not isinstance(args,dict):
			return errorPacket('Argument list not a dict.')

		try:
			f=self.commands[cmd]
		except KeyError:	
			return errorPacket('Bad command.')

		try:
			result=f(self,**args)
		except Exception as e:
			raise
			return errorPacket(str(e))

		return goodPacket(result)

	def get_uid(self):
		u=self.uid
		self.uid+=1
		return u

	def instantiate(self,type,args):
		if 'pool' in args or 'uid' in args:
			raise Exception('arg list cannot contain pool or uid')
		uid=self.get_uid()
		return (dict([(s.TYPE_STRING,s) for s in self.scrapers])[type])(self,uid,args)

	commands={
		'rm':rm,
		'add':add,
		'pool':get_pool,
		'describe':describe_scraper,
	}

# End class Pool

# Useful JSONification functions

def errorPacket(err):
	return {'success':False,'error':err}

def goodPacket(payload):
	if payload is not None:
		return {'success':True,'result':payload}
	return {'success':True}

