from scraper import *
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


def add_movie(local_file,info):
	info['filename']=title2file(info['title'])
	conn=sqlite3.connect(os.path.join(BASEPATH,settings.DB))
	tf=tempfile.NamedTemporaryFile(delete=False)
	try:
		ffmpeg_proc=subprocess.Popen(settings.FFMPEG_QUERY(local_file),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		ffmpeg_out=ffmpeg_proc.communicate()
		acopy=("Audio: {0}".format(settings.FFMPEG_ACODEC) in ffmpeg_out[1])
		vcopy=("Video: {0}".format(settings.FFMPEG_VCODEC) in ffmpeg_out[1])
		result=subprocess.call(settings.FFMPEG_ENCODE(local_file,tf.name,acopy,vcopy))
		if result != 0:
			raise Exception('FFMPEG Failed')

		c=conn.cursor()
		prune=[(k,v) for (k,v) in info.items() if k in ['filename','title','year','meta','thumb']]
		keys=[p[0] for p in prune]
		values=[p[1] for p in prune]
		
		c.execute('INSERT INTO movies ({0}) values ({1})'.format(','.join(keys),','.join(['?']*len(values))),[str(v) for v in values])
		insertion=c.lastrowid
		target=os.path.join(BASEPATH,settings.CONTENT_DIR,'movies',str(insertion),info['filename'])
		os.makedirs(os.path.dirname(target))
		shutil.copy(tf.name,target)
		conn.commit()
	finally:
		os.unlink(tf.name)
		conn.close()

	return insertion
