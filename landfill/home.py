from werkzeug.wrappers import Request,Response
from common import *

def app(config,args,request):
	return page(config,'home.html')
