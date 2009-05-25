"""
Copyright 2009 Myles Braithwaite <me@mylesbraithwaite.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import urllib, base64, string

import simplejson
import httplib2

class Couch(object):
	"""
	:param host: The full URI to the CouchDB host.
	:params username password: The username and password to login.
	"""
	def __init__(self, host='http://127.0.0.1:5984', username=None, password=None):
		self.host = host
		self.username = username
		self.password = password
	
	def _connect(self):
		"""Connect to the CouchDB server.
		"""
		h = httplib2.Http()
		if self.username and self.password:
			h.add_credentials(self.username, self.password)
		
		return h
	
	def _http(self, path, method, headers={}, body=None):
		c = self._connect()
		return c.request('%s%s' % (self.host, path),
			method,
			headers=headers,
			body=body)
	
	# Database operations
	
	def list_databases(self):
		"""List all the databases in the CouchDB server.
	
		:return: A list of database names.
		:rtype: list
		"""
		headers = { "Accept": "application/json" }
		response, content = self._http('/_all_dbs', "GET", headers=headers)
		return simplejson.loads(content)
	
	def create_database(self, db_name):
		"""Create a database.
	
		:param db_name: The name of the database you wish to create.
		:return: If suessfuly will return { "ok": True }
		:rtype: dict
		"""
		url = ''.join([ '/', db_name, '/' ])
		response, content = self._http(url, "PUT")
		if response.status == 201:
			return True
		elif response.status == 412:
			return False # TODO Raise an exception instead.
		else:
			return False # TODO Raise an exception instead.
	
	def delete_database(self, db_name):
		"""Delete a database
	
		:param db_name: The name of the database you wish to delete.
		:return: If suessfuly will return { "ok": True }
		:rtype: dict
		"""
		url = ''.join([ '/', db_name, '/'])
		response, content = self._http(url, "DELETE")
		if response.status == 200:
			return True
		elif response.status == 404:
			return False # TODO Raise an exception instead.
		else:
			return False # TODO Raise an exception instead.
	
	def info_database(self, db_name):
		"""Returns information about a database.
	
		:param db_name: The name of the database.
		:return: update_seq, disk_size, doc_count, compact_running, db_name, doc_del_count
		:rtype: dict
		"""
		url = ''.join([ '/', db_name, '/'])
		response, content = self._http(url, "GET")
		if response.status == 404:
			return False # TODO Raise an exception instead.
		
		return simplejson.loads(content)
	
	# Document operations
	
	def list_documents(self, db_name):
		"""List of documents within a database.
		
		:param db_name: The name of the database.
		:rtype: list
		"""
		headers = { "Accept": "application/json" }
		url = ''.join([ '/', db_name, '/' , '_all_docs' ])
		response, content = self._http(url, "GET", headers=headers)
		return simplejson.loads(content)
	
	def open_document(self, db_name, doc_id, doc_rev=None):
		"""Opens a document within the database.
		
		:param db_name: The name of the database.
		:param doc_id: The ID of the document.
		:param doc_rev: The revision of the document, default to the current version.
		
		:return: The document.
		:rtype: dict
		"""
		headers = { "Accept": "application/json" }
		
		if doc_rev:
			params = urllib.urlencode({'rev': doc_rev})
			url = ''.join([ '/', db_name, '/', doc_id, '?', params ])
		else:
			params = None
			url = ''.join([ '/', db_name, '/', doc_id ])
		
		response, content = self._http(url, "GET", headers=headers)
		
		if response.status == 404:
			return False # TODO Raise an exception instead.
		
		return simplejson.loads(content)
	
	def save_document(self, db_name, body, doc_id):
		"""Saves an existing document in the database.
		
		:param db_name: The name of the database.
		:param doc_id: The ID of the document.
		:param doc_rev: The revision of the document, default to the current version.
		
		:return: {"ok": true, "id": "some_doc_id", "rev": "946B7D1C"}
		:rtype: dict
		"""
		headers = { "Content-type": "application/json" }
		url = ''.join([ '/', db_name, '/', doc_id ])
		
		json = simplejson.dumps(body)
		
		response, content = self._http(url, "PUT", body=json, headers=headers)
		
		if response.status == 412:
			return False # TODO Raise an exception instead.
		
		return simplejson.loads(content)
	
	def create_document(self, db_name, body, doc_id=None):
		"""Creates a document in the database.
		
		:param db_name: The name of the database.
		:param doc_id: Provide a document id.
		:type body: dict
		
		:return: {"ok": true, "id": "some_doc_id", "rev": "946B7D1C"}
		:rtype: dict
		"""
		headers = { "Content-type": "application/json" }
		
		json = simplejson.dumps(body)
		
		if doc_id:
			url = ''.join([ '/', db_name, '/', doc_id ])
			response, content = self._http(url, "PUT", body=json, headers=headers)
		else:
			url = ''.join([ '/', db_name, '/' ])
			response, content = self._http(url, "POST", body=json, headers=headers)
		
		if response.status == 412:
			return False # TODO Raise an exception instead.
		
		return simplejson.loads(content)
	
	def delete_document(self, db_name, doc_id, doc_rev):
		"""Deletes a document in the database.
		
		:param db_name:
		:param doc_id: 
		:param doc_rev:
		"""
		params = urllib.urlencode({'rev': doc_rev})
		url = ''.join([ '/', db_name, '/', doc_id, '?', params ])
		response, content = self._http(url, "DELETE")
		
		if response.status == 200:
			return True
		else:
			return False # TODO Raise an exception instead.
