from werkzeug.wrappers import Response
import sqlite3

def page(config,template_name,context={},mimetype='text/html'):
	t = config['jinja_env'].get_template(template_name)
	return Response(t.render(context), mimetype=mimetype)

def db_connect(config):
	conn=sqlite3.connect(config['db'])
	conn.row_factory = sqlite3.Row
	return conn
