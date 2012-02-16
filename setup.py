#from cx_Freeze import setup, Executable #@UnresolvedImport
from distutils.core import setup

setup(
	name = "semtex",
	version = "0.1a",
	author='Nic Roland',
	author_email='nicroland9@gmail.com',
	description = "SemTeX: Equations Made using laTEX",
	scripts = ["semtex.py"],
	packages = ['semtex_gui'],
	package_data = {'semtex_gui':['cache/*','res/*']})
