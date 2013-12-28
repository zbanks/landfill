#!/usr/bin/python

from werkzeug.wrappers import Request,Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException
from jinja2 import Environment,FileSystemLoader
import os

import home
import movies

template_path = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = Environment(loader=FileSystemLoader(template_path),autoescape=True)

config={
	'db':'library.db',
	'jinja_env':jinja_env
}

url_map = Map([
    Rule('/', endpoint=home.app),
    Rule('/movie', endpoint=movies.app),
    Rule('/movie/<int:id>', endpoint=movies.watch),
])

def application(environ, start_response):
	urls = url_map.bind_to_environ(environ)
	try:
		endpoint, args = urls.match()
	except HTTPException, e:
		return e(environ, start_response)
	return endpoint(config,args,environ)(environ, start_response)

if __name__=='__main__':
	from twisted.web.server import Site
	from twisted.web.wsgi import WSGIResource
	from twisted.internet import reactor
	from twisted.web.static import File
	from autobahn.resource import WSGIRootResource

	local_root=os.path.join(os.path.dirname(__file__), '../')

	site = WSGIResource(reactor, reactor.getThreadPool(),application)
	content = File(os.path.join(local_root,'content'))
	static = File(os.path.join(local_root,'static'))

	root = WSGIRootResource(site,{'content':content,'static':static})

	reactor.listenTCP(9501, Site(root))
	reactor.run()

