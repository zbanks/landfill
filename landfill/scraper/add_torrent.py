import settings
import os
import magic

def is_movie(f):
	m=magic.from_file(f)
	# dammit brian
	return ('video:' in m and 'audio:' in m) or ('matroska' in m) or ('MPEG v4' in m)

def get_movie_from_torrent(torrent):
	MAX_VIDEOS=4 # If a torrent has more than four videos, it is unlikely to be a movie
	files=[os.path.join(root,f) for (root, subFolders, fs) in os.walk(torrent) for f in fs]
	if len(files)==0:
		raise Exception('Torrent does not contain any files.')
	files=[(x,os.stat(x).st_size) for x in files]
	files.sort(key=lambda x:-x[1])
	if len(files)>MAX_VIDEOS+1:
		files=files[0:MAX_VIDEOS+1]
	files=[(f,s) for (f,s) in files if is_movie(f)]
	if len(files)==0:
		raise Exception('Torrent does not contain any videos.')
	if len(files)==1:
		return files[0][0]
	if len(files)>1 and files[0][1] > 5*files[1][1]: # If the largest video is more than five times larger than the second largest video
		return files[0][0]
	raise Exception('Too many video files in torrent')

if __name__=='__main__':
	print "FOUND:",get_movie_from_torrent('/home/eric/cesspool/')
