from scraper import Scraper
import settings
import tempfile
import sqlite3
import subprocess
import os
import shutil
import threading

def title2file(title):
		acceptable_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()'
		return (''.join([l for l in title if l in acceptable_chars]))+'.mp4'

BASEPATH=os.path.join(os.path.dirname(__file__),'../')

class AddMovie(Scraper,threading.Thread):
	TYPE_STRING='add_movie'

	def add(self,local_file,info):
		threading.Thread.__init__(self)
		self.daemon=True
		self.local_file=local_file
		self.info=info

		self.start()

	def run(self):
		self.info['filename']=title2file(self.info['title'])
		conn=sqlite3.connect(os.path.join(BASEPATH,settings.DB))
		tf=tempfile.NamedTemporaryFile(delete=False)
		try:
			result=subprocess.call(settings.FFMPEG(self.local_file,tf.name))
			if result != 0:
				raise Exception('FFMPEG Failed')

			c=conn.cursor()
			prune=[(k,v) for (k,v) in self.info.items() if k in ['filename','title','year','meta','thumb']]
			keys=[p[0] for p in prune]
			values=[p[1] for p in prune]
			
			c.execute('INSERT INTO movies ({0}) values ({1})'.format(','.join(keys),','.join(['?']*len(values))),[str(v) for v in values])
			target=os.path.join(BASEPATH,'../content/movies',str(c.lastrowid),self.info['filename'])
			os.makedirs(os.path.dirname(target))
			shutil.copy(tf.name,target)
			conn.commit()
		finally:
			os.unlink(tf.name)
			conn.close()

