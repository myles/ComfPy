import simplejson, httplib, urllib

class Couch(object):
	"""
	:param host: The URL to the CouchDB host.
	:param port: The Port that CouchDB is running on.
	
	>>> c = Couch()
	
	>>> c.list_databases()
	[]
	"""
	def __init__(self, host='127.0.0.1', port=5984, options=None):
		self.host = host
		self.port = port
	
	def _connect(self):
		"""Connect to the CouchDB server.
		"""
		return httplib.HTTPConnection(self.host, self.port)
	
	# Database operations
	
	def list_databases(self):
		"""List all the databases in the CouchDB server.
	
		:return: A list of database names.
		:rtype: list
		"""
		c = self._connect()
		headers = { "Accept": "application/json" }
		c.request("GET", '/_all_dbs', None, headers)
		r = c.getresponse()
		json = r.read()
		return simplejson.loads(json)
	
	def create_database(self, db_name):
		"""Create a database.
	
		:param db_name: The name of the database you wish to create.
		:return: If suessfuly will return { "ok": True }
		:rtype: dict
		"""
		c = self._connect()
		
		r = self._put(''.join([ '/', db_name, '/' ]), None)
		return r
	
	def delete_database(self, db_name):
		"""Delete a database
	
		:param db_name: The name of the database you wish to delete.
		:return: If suessfuly will return { "ok": True }
		:rtype: dict
		"""
		r = self._delete(''.join([ '/', db_name, '/']))
		return r
	
	def info_database(self, db_name):
		"""Returns information about a database.
	
		:param db_name: The name of the database.
		:return: update_seq, disk_size, doc_count, compact_running, db_name, doc_del_count
		:rtype: dict
		"""
		r = self._get(''.join([ '/', db_name, '/']))
		return r
	
	# Document operations
	
	def list_document(self, db_name):
		"""List of documents within a database.
		
		:param db_name: The name of the database.
		:return:
		"""
		c = self._connect()
		headers = { "Accept": "application/json" }
		uri = ''.join([ '/', db_name, '/' , '_all_docs' ])
		c.request("GET", uri, params, headers)
		r = c.getresponse()
		json = simplejson.loads(r.read())
		return json
	
	def open_document(self, db_name, doc_id, doc_rev=None):
		if doc_rev:
			params = urllib.urlencode({'rev': doc_rev})
			r = self._get(''.join([ '/', db_name, '/', doc_id ]), params=params)
		else:
			r = self._get(''.join([ '/', db_name, '/', doc_id ]))
		return r
	
	def save_document(self, db_name, body, doc_id=None):
		if doc_id:
			r = self._put(''.join([ '/', db_name, '/', doc_id ]), body)
		else:
			r = self._post(''.join([ '/', db_name, '/' ]), body)
		return r
	
	def create_document(self, db_name, body):
		return self.save_document(db_name, body)
	
	def delete_document(self, db_name, doc_id):
		""" Doesn't work """
		r = self._delete(''.join([ '/', db_name, '/', doc_id ]))


if __name__ == "__main__":
	import doctest
	doctest.testmod()