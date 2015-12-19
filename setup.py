from distutils.core import setup

setup(
	name = "semtex",
	version = "v1.0",
	author='Nic Roland',
	author_email='nicroland9@gmail.com',
	description = "SemTeX: Equations Made using laTEX",
	scripts = ["bin/semtex"],
	packages = ['semtex'],
	package_data = {'semtex':['cache/*','res/*']})
