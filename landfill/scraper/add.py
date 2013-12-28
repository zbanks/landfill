import settings
import tempfile
import sqlite3
import subprocess
import os
import shutil

def title2file(title):
		acceptable_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()'
		return (''.join([l for l in title if l in acceptable_chars]))+'.mp4'

BASEPATH=os.path.join(os.path.dirname(__file__),'../')

class AddMovie(object):
	def __init__(self,local_file,info):
		self.local_file=local_file
		self.info=info

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

if __name__=='__main__':
	AddMovie('../testing/diehard_clip.avi',{'title':'Die Hard','year':1988}).run()
