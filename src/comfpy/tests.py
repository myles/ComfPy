import unittest

from comfpy.couch import Couch

class TestCouch(unittest.TestCase):
	def setUp(self):
		self.couch = Couch()
		self.couch.create_database('test_comfpy')
	
	def tearDown(self):
		self.couch.delete_database('test_comfpy')
	
	def test_list_databases(self):
		self.couch.list_databases()
	
	def test_info_database(self):
		r = self.couch.info_database('test_comfpy')
		self.assertEqual(r['db_name'], 'test_comfpy')
	
	def test_list_document(self):
		r = self.couch.list_documents('test_comfpy')
		self.assertEqual(r['total_rows'], 0)
	
	def test_create_document(self):
		r = self.couch.create_document('test_comfpy', {'test1': 'test1'}, 'test1')
		self.assertEqual(r['ok'], True)
		r = self.couch.create_document('test_comfpy', {'test2': 'test2'}, 'test2')
		self.assertEqual(self.couch.list_documents('test_comfpy')['total_rows'], 2)
	
	def test_save_document(self):
		r = self.couch.save_document('test_comfpy', {'test1': 'test1', 'test2': 'test2'}, 'test1')
		self.assertEqual(r['ok'], True)
	
	# def test_delete_document(self):
	# 	self.couch.create_document('test_comfpy', {'test1': 'test1'}, 'test1')
	# 	rev = self.couch.open_document('test_comfpy', 'test1')['_rev']
	# 	self.couch.delete_document('test_comfpy', 'test1', rev)

def test_suite():
	return unittest.makeSuite(TestCouch)