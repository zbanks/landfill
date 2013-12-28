from werkzeug.wrappers import Request,Response
from werkzeug.exceptions import NotFound
from common import *

def app(config,args,request):
	conn=db_connect(config)
	c=conn.cursor()
	movies_iter=c.execute('SELECT id,title FROM movies')
	p=page(config,'movies.html',{'movies':movies_iter})
	conn.close()
	return p

def watch(config,args,request):
	conn=db_connect(config)
	c=conn.cursor()
	c.execute('SELECT id,filename,title FROM movies WHERE id={0}'.format(int(args['id'])))
	movie_info=c.fetchone()
	conn.close()
	if movie_info is None:
		return NotFound()
	return page(config,'watch_movie.html',{'movie':movie_info})
