from add_movie import AddMovie
import requests
import re
import json

class AddFromIMDB(AddMovie):
	def __init__(self,local_file,imdb):
		self.local_file=local_file
		self.imdb=imdb

	def run(self):
		m=re.match(r'(?:http://)?(?:www\.)?imdb\.com/title/(tt\d+)/',self.imdb)
		if m is None:
			raise Exception('Not a valid IMDB link')
		imdb_id=m.groups()[0]
		omdb=requests.get('http://www.omdbapi.com/?i={0}'.format(imdb_id)).text
		j=json.loads(omdb)
		if j['Response']!='True':
			raise Exception('OMDB Query failed')
		self.info={'meta':omdb}
		if 'Title' in j: self.info['title']=j['Title']
		if 'Year' in j: self.info['year']=j['Year']
		if 'Poster' in j:
			p=j['Poster']
			m=re.match(r'(.+@@).+\.jpg',j['Poster'])
			if m is not None:
				p='{0}.jpg'.format(m.groups()[0])
			self.info['thumb']=p
		AddMovie.run(self)

if __name__=='__main__':
	AddFromIMDB('../testing/diehard_clip.avi','http://www.imdb.com/title/tt0095016/?ref_=nv_sr_1').run()
