from cx_Freeze import setup, Executable

setup(
	name = "semtex",
	version = "0.1a",
	author='Nic Roland',
	author_email='nicroland9@gmail.com',
	description = "SemTeX: Equations Made using laTEX",
	executables = [Executable("src/semtex.py")])
