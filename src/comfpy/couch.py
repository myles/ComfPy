import simplejson, httplib, urllib

class Couch(object):
	"""
	:param host: The URL to the CouchDB host.
	:param port: The Port that CouchDB is running on.
	"""
	def __init__(self, host='127.0.0.1', port=5984, ssl=False):
		self.host = host
		self.port = port
		self.ssl = ssl
	
	def _connect(self):
		"""Connect to the CouchDB server.
		"""
		if self.ssl:
			return httplib.HTTPConnection(self.host, self.port)
		else:
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
		uri = ''.join([ '/', db_name, '/' ])
		c.request("PUT", uri, None)
		r = c.getresponse()
		if r.status == 201:
			return True
		elif r.status == 412:
			return False # TODO Raise an exception instead.
		else:
			return False # TODO Raise an exception instead.
	
	def delete_database(self, db_name):
		"""Delete a database
	
		:param db_name: The name of the database you wish to delete.
		:return: If suessfuly will return { "ok": True }
		:rtype: dict
		"""
		c = self._connect()
		uri = ''.join([ '/', db_name, '/'])
		c.request("DELETE", uri, None)
		r = c.getresponse()
		if r.status == 200:
			return True
		elif r.status == 404:
			return False # TODO Raise an exception instead.
		else:
			return False # TODO Raise an exception instead.
	
	def info_database(self, db_name):
		"""Returns information about a database.
	
		:param db_name: The name of the database.
		:return: update_seq, disk_size, doc_count, compact_running, db_name, doc_del_count
		:rtype: dict
		"""
		c = self._connect()
		uri = ''.join([ '/', db_name, '/'])
		c.request("GET", uri, None)
		r = c.getresponse()
		if r.status == 404:
			return False # TODO Raise an exception instead.
		
		json = r.read()
		return simplejson.loads(json)
	
	# Document operations
	
	def list_documents(self, db_name):
		"""List of documents within a database.
		
		:param db_name: The name of the database.
		:rtype: list
		"""
		c = self._connect()
		headers = { "Accept": "application/json" }
		uri = ''.join([ '/', db_name, '/' , '_all_docs' ])
		c.request("GET", uri, None, headers)
		r = c.getresponse()
		json = r.read()
		return simplejson.loads(json)
	
	def open_document(self, db_name, doc_id, doc_rev=None):
		"""Opens a document within the database.
		
		:param db_name: The name of the database.
		:param doc_id: The ID of the document.
		:param doc_rev: The revision of the document, default to the current version.
		
		:return: The document.
		:rtype: dict
		"""
		c = self._connect()
		headers = { "Accept": "application/json" }
		
		if doc_rev:
			params = urllib.urlencode({'rev': doc_rev})
			uri = ''.join([ '/', db_name, '/', doc_id, '?', params ])
		else:
			params = None
			uri = ''.join([ '/', db_name, '/', doc_id ])
		
		c.request("GET", uri, None, headers)
		r = c.getresponse()
		
		if r.status == 404:
			return False # TODO Raise an exception instead.
		
		json = r.read()
		return simplejson.loads(json)
	
	def save_document(self, db_name, body, doc_id):
		"""Saves an existing document in the database.
		
		:param db_name: The name of the database.
		:param doc_id: The ID of the document.
		:param doc_rev: The revision of the document, default to the current version.
		
		:return: {"ok": true, "id": "some_doc_id", "rev": "946B7D1C"}
		:rtype: dict
		"""
		c = self._connect()
		headers = { "Content-type": "application/json" }
		uri = ''.join([ '/', db_name, '/', doc_id ])
		
		json = simplejson.dumps(body)
		
		c.request("PUT", uri, json, headers)
		r = c.getresponse()
		
		if r.status == 412:
			return False # TODO Raise an exception instead.
		
		json = r.read()
		return simplejson.loads(json)
	
	def create_document(self, db_name, body, doc_id=None):
		"""Creates a document in the database.
		
		:param db_name: The name of the database.
		:param doc_id: Provide a document id.
		:type body: dict
		
		:return: {"ok": true, "id": "some_doc_id", "rev": "946B7D1C"}
		:rtype: dict
		"""
		c = self._connect()
		headers = { "Content-type": "application/json" }
		
		json = simplejson.dumps(body)
		
		if doc_id:
			uri = ''.join([ '/', db_name, '/', doc_id ])
			c.request("PUT", uri, json, headers)
		else:
			uri = ''.join([ '/', db_name, '/' ])
			c.request("POST", uri, json, headers)
		
		r = c.getresponse()
		
		if r.status == 412:
			return False # TODO Raise an exception instead.
		
		json = r.read()
		return simplejson.loads(json)
	
	def delete_document(self, db_name, doc_id, doc_rev):
		"""Deletes a document in the database."""
		c = self._connect()
		params = urllib.urlencode({'rev': doc_rev})
		uri = ''.join([ '/', db_name, '/', doc_id, '?', params ])
		c.request("DELETE", uri, None, None)
		r = c.getresponse()
		if r.status == 200:
			return True
		else:
			return False # TODO Raise an exception instead.
