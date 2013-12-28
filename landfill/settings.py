DB='library.db'
FFMPEG=lambda i,o:['ffmpeg', '-i', i, '-acodec', 'libvo_aacenc', '-vcodec', 'libx264', '-movflags', 'faststart', '-f', 'mp4', o, '-y']
