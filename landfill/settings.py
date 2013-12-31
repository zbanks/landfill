CONTENT_DIR='../content'
DB='library.db'

def FFMPEG_ENCODE(i,o,acopy,vcopy):
	if acopy: ac='copy'
	else: ac='libvo_aacenc'
	if vcopy: vc='copy'	
	else: vc='libx264'

	return ['ffmpeg', '-i', i, '-acodec', ac, '-vcodec', vc, '-movflags', 'faststart', '-f', 'mp4', '-y', o]

def FFMPEG_QUERY(i):
	return ['ffprobe', i]

FFMPEG_ACODEC='aac'
FFMPEG_VCODEC='h264'
