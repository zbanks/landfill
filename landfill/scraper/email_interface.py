#!/usr/bin/python

import from_email
import add_imdb
import add_torrent
import add_movie
import cp
import sys
import os

from email.mime.text import MIMEText
import smtplib

me="landfill@localhost"
cp_url="http://localhost:9500/cmd"
cp_local=os.path.join(os.path.dirname(__file__),'/home/eric/cesspool/downloads')
lf_url="http://localhost:9501/"

(sender,subj,body)=from_email.parse_email(sys.stdin)

def send_mail(body):
	msg=MIMEText(body)
	msg['Subject']="Re: {0}".format(subj)
	msg['From']=me
	msg['To']=sender
	print msg.as_string()
	#s = smtplib.SMTP('localhost')
	#s.sendmail(me, [sender], msg.as_string())

try:
	useful=from_email.find_useful(body)
	if len(useful)!=2 or useful[1][0]!='imdb' or useful[0][0]!='magnet':
		raise Exception('Bad format. Need a magnet link followed by an IMDB url.')

	imdb=useful[1][1]
	magnet=useful[0][1]
	info=add_imdb.get_omdb_info(imdb)
	send_mail("Downloading {0}.".format(info['title']))

	uid=cp.get_torrent(cp_url,magnet)

	local_torrent=os.path.join(cp_local,str(uid))
	movie_file=add_torrent.get_movie_from_torrent(local_torrent)
	lf_uid=add_movie.add_movie(movie_file,info)
	link=lf_url+"movie/"+str(lf_uid)
	send_mail("Finished! {0}".format(link))

except Exception as e:
	send_mail("An error occurred. {0}".format(str(e)))
