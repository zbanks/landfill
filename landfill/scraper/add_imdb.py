from add_movie import add_movie
import requests
import re
import json

def get_omdb_info(imdb):
	m=re.match(r'(?:http://)?(?:www\.)?imdb\.com/title/(tt\d+)/',imdb)
	if m is None:
		raise Exception('Not a valid IMDB link')
	imdb_id=m.groups()[0]
	omdb=requests.get('http://www.omdbapi.com/?i={0}'.format(imdb_id)).text
	j=json.loads(omdb)
	if j['Response']!='True':
		raise Exception('OMDB Query failed')
	info={'meta':omdb}
	if 'Title' in j: info['title']=j['Title']
	if 'Year' in j: info['year']=j['Year']
	if 'Poster' in j:
		p=j['Poster']
		m=re.match(r'(.+@@).+\.jpg',j['Poster'])
		if m is not None:
			p='{0}.jpg'.format(m.groups()[0])
		info['thumb']=p
	return info

def add_movie_from_imdb(local_file,imdb):
	return add_movie(local_file,get_omdb_info(imdb))

if __name__=='__main__':
	print add_movie_from_imdb('bbtest.mkv','http://www.imdb.com/title/tt0903747/')
