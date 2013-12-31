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


class AddMovie(Scraper,threading.Thread):
	TYPE_STRING='add_movie'

	def add(self,local_file,info):
		self.local_file=local_file
		self.info=info
		self.go()

	def go(self):
		threading.Thread.__init__(self)
		self.daemon=True
		self.start()

	def run(self):
		self.info['filename']=title2file(self.info['title'])
		conn=sqlite3.connect(os.path.join(self.pool.params['base_path'],settings.DB))
		tf=tempfile.NamedTemporaryFile(delete=False)
		try:
			ffmpeg_proc=subprocess.Popen(settings.FFMPEG_QUERY(self.local_file),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			ffmpeg_out=ffmpeg_proc.communicate()
			acopy=("Audio: {0}".format(settings.FFMPEG_ACODEC) in ffmpeg_out[1])
			vcopy=("Video: {0}".format(settings.FFMPEG_VCODEC) in ffmpeg_out[1])
			result=subprocess.call(settings.FFMPEG_ENCODE(self.local_file,tf.name,acopy,vcopy))
			if result != 0:
				raise Exception('FFMPEG Failed')

			c=conn.cursor()
			prune=[(k,v) for (k,v) in self.info.items() if k in ['filename','title','year','meta','thumb']]
			keys=[p[0] for p in prune]
			values=[p[1] for p in prune]
			
			c.execute('INSERT INTO movies ({0}) values ({1})'.format(','.join(keys),','.join(['?']*len(values))),[str(v) for v in values])
			target=os.path.join(self.pool.params['content_dir'],'movies',str(c.lastrowid),self.info['filename'])
			os.makedirs(os.path.dirname(target))
			shutil.copy(tf.name,target)
			conn.commit()
		finally:
			os.unlink(tf.name)
			conn.close()

