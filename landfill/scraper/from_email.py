#!/usr/bin/env python

import encodings
import json
import os
import quopri
import re
import email

def parse_email(f):
	msg = email.message_from_file(f)
	sender = msg["From"]
	subject = msg["Subject"]

	for part in msg.walk():
		if part.is_multipart():
			continue
		if part.get_content_type() == "text/plain":
			aliases = encodings.aliases.aliases.keys()
			css=filter(lambda x: x in aliases, part.get_charsets())
			msg=part.get_payload(decode=True)
			msg=re.sub(r'\r\n','\n',msg) # fuck you windows
			body=msg
			return sender,subject,msg

	raise Exception('No email could be decoded.')

def find_useful(body):
	magnet=[('magnet',m.groups()[0].replace('\n',''),m.start()) for m in re.finditer(r'(magnet:\?.+?)(?: |\n\n)',body,re.DOTALL)]
	imdb=[('imdb',m.groups()[0],m.start()) for m in re.finditer(r'(?:http://)?(?:www\.)?imdb\.com/title/(tt\d+)/',body)]
	result=magnet+imdb
	result.sort(key=lambda x:x[2])
	result=[x[0:2] for x in result]
	return result

if __name__ == "__main__":
	import sys
	(sender,subject,body)=parse_email(sys.stdin)
	print find_useful(body)

