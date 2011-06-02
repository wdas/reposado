import os
import sys
from distutils.core import setup

if sys.platform == 'win32':
    import py2exe

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if sys.platform == 'win32':
	setup(
		name = "reposado",
		version = "git",
		author = "Greg Neagle",
		author_email = "reposado@googlegroups.com",
		maintainer = "Brent B",
		maintainer_email = "brent.bb+py@gmail.com",
		description = ("Host Apple Software Updates on the hardware and OS of your choice."),
		license = "BSD",
		keywords = "apple software update repository",
		url = "https://github.com/wdas/reposado",
		packages=['reposadolib'],
		package_dir={'reposadolib': 'code/reposadolib'},
		scripts=["code/repo_sync","code/repoutil"],
		long_description=read('README.md'),
		classifiers=[
			"Intended Audience :: System Administrators",
			"Development Status :: 1 - Alpha",
			"Topic :: Utilities",
			"License :: OSI Approved :: BSD License",
			"Topic :: System :: Archiving :: Mirroring",
			"Topic :: System :: Installation/Setup",
		],
		console=["code/repo_sync","code/repoutil"],
	)
else:
	setup(
		name = "reposado",
		version = "git",
		author = "Greg Neagle",
		author_email = "reposado@googlegroups.com",
		maintainer = "Brent B",
		maintainer_email = "brent.bb+py@gmail.com",
		description = ("Host Apple Software Updates on the hardware and OS of your choice."),
		license = "BSD",
		keywords = "apple software update repository",
		url = "https://github.com/wdas/reposado",
		packages=['reposadolib'],
		package_dir={'reposadolib': 'code/reposadolib'},
		scripts=["code/repo_sync","code/repoutil"],
		long_description=read('README.md'),
		classifiers=[
			"Intended Audience :: System Administrators",
			"Development Status :: 1 - Alpha",
			"Topic :: Utilities",
			"License :: OSI Approved :: BSD License",
			"Topic :: System :: Archiving :: Mirroring",
			"Topic :: System :: Installation/Setup",
		],
	)
