from distutils.core import setup

setup(
	name = "semtex",
	version = "0.5a",
	author='Nic Roland',
	author_email='nicroland9@gmail.com',
	description = "SemTeX: Equations Made using laTEX",
	scripts = ["semtex.py"],
	packages = ['semtex'],
	package_data = {'semtex':['cache/*','res/*']})
