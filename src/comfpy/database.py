from comfpy.couch import Couch

class Database(object):
	def __init__(self, host, port, db_name):
		self.c = Couch(host, port)
		self.db_name = db_name