#!/usr/bin/python

from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware
import os

import sys

class LFServer(object):
	def __init__(self,database):
		self.database=database

	def dispatch_request(self,request):
		return Response("hallo media server")

	def wsgi_app(self, environ, start_response):
		request = Request(environ)
		response = self.dispatch_request(request)
		return response(environ, start_response)

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ,start_response)


if __name__=='__main__':
	from twisted.web.server import Site
	from twisted.web.wsgi import WSGIResource
	from twisted.internet import reactor
	from twisted.web.static import File
	#from autobahn.resource import WSGIRootResource

	if len(sys.argv)>1:
		lib=sys.argv[1]
	else:
		lib='library.json'

	app=LFServer(lib)

	local_root=os.path.join(os.path.dirname(__file__), '../')

	site = WSGIResource(reactor, reactor.getThreadPool(),app)
	content = File(os.path.join(local_root,'content'))
	static = File(os.path.join(local_root,'static'))

	root = WSGIRootResource(site,{'content':content,'static':static})

	reactor.listenTCP(9501, Site(root))
	reactor.run()

