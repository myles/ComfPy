from setuptools import setup, find_packages

setup(
	name = "comfpy",
	version = "0.1",
	url = "http://github.com/myles/comfpy",
	license = "Apache 2.0",
	description = "A library for CouchDB",
	author = "Myles Braithwaite",
	packages = find_packages('src'),
	package_dir = {'': 'src'},
	install_requires = ['setuptools', 'simplejson', 'httplib2'],
)