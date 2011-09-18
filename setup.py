#!/usr/bin/env python
"""
Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
     python setup.py py2app

Usage (Windows):
     python setup.py py2exe
"""
import glob
import os

import ez_setup
ez_setup.use_setuptools()


from setuptools import setup
import sys

mainscript = 'src/StructurEd.pyw'

if sys.platform == 'darwin':
     extra_options = dict(
         setup_requires=['py2app'],
         app=[mainscript],
         # Cross-platform applications generally expect sys.argv to
         # be used for opening files.
         options=dict(
             py2app=dict(
                argv_emulation=True,
                iconfile='resources/application_icon/StructurEd.icns',
                includes=['sip'],
                packages=['PyQt4']
             )),
     )
elif sys.platform == 'win32':
     extra_options = dict(
         setup_requires=['py2exe'],
         app=[mainscript],
     )
else:
     extra_options = dict(
         # Normally unix-like platforms will use "setup.py install"
         # and install the main script as such
         scripts=[mainscript],
     )

setup(
    name="StructurEd",
    version="0.1",
    author="Sergey Klimov",
    author_email="sergey.v.klimov@gmail.com",
    url="http://darvin.github.com/StructurEd/",
    description="Editor for custom-structured files, firstly for plists for iOS/OS X games",
    long_description="""
    """,
    classifiers="""
Development Status :: 3 - Alpha
Environment :: MacOS X
Environment :: X11 Applications :: Qt
Intended Audience :: Developers
Intended Audience :: End Users/Desktop
License :: OSI Approved :: GNU General Public License (GPL)
Natural Language :: Russian
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Programming Language :: Python :: 2.7
Topic :: Games/Entertainment
Topic :: Software Development :: Code Generators
Topic :: Software Development
Topic :: Utilities
""".split("\n"),
    license="GPL",
    package_dir = {'structured': 'src'},
    packages = ['structured'],
    scripts=[mainscript],
    **extra_options
)
