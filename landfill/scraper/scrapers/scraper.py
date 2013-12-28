class Scraper:
	TYPE_STRING='scraper'

	def __init__(self,pool,uid,args):
		self.uid=uid
		self.pool=pool

		self.add(**args)

	def intrinsics(self):
		return {'type':self.parent.TYPE_STRING,'uid':self.uid}

	def _describe(self):
		return dict(self.intrinsics().items()+self.describe().items())

