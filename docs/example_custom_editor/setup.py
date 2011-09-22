#!/usr/bin/env python
"""
Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
     python setup.py py2app

Usage (Windows):
     python setup.py py2exe
"""
import distutils
import glob
import os

import ez_setup
ez_setup.use_setuptools()

from subprocess import call

from setuptools import setup
import sys

mainscript = os.path.join('src','ExampleEditor.pyw')


if sys.platform == 'darwin':
     extra_options = dict(
         setup_requires=['py2app'],
         app=[mainscript],
         # Cross-platform applications generally expect sys.argv to
         # be used for opening files.
         options=dict(
             py2app=dict(
                argv_emulation=False,
#                iconfile='resources/application_icon/StructurEd.icns',
                includes=['sip'],
                packages=['PyQt4','structured'],
                resources=["resources/sample_citybuilder_scheme.plist", "resources/qt.conf"]
             )),
     )
elif sys.platform == 'win32':
     import py2exe
     msredist_path = r"C:\Python27\Microsoft.VC90.CRT"
     sys.path.append(msredist_path)
     sys.path.append(r"C:\Python27\Lib\site-packages\PyQt4")
     print sys.path
     msredist_files = [msredist_path+"\\Microsoft.VC90.CRT.manifest"]+glob.glob(msredist_path+"\\*.dll")
     print msredist_files
     extra_options = dict(
         setup_requires=['py2exe'],
	 zipfile=None,
         windows=[{"script":mainscript, "icon_resources": [(1, "resources\\application_icon\\StructurEd.ico")]}],
         options=dict(py2exe= {"includes" : ["sip", "PyQt4",'structured'],
				"bundle_files":1,
	 
	 }
	 ),
         data_files=[("Microsoft.VC90.CRT", msredist_files)] 
     )
else:
     extra_options = dict(
         # Normally unix-like platforms will use "setup.py install"
         # and install the main script as such
         scripts=[mainscript],
     )

setup(
    name="ExampleStructurEdBasedEditor",
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
    package_dir = {'cityeditor': 'src'},
    packages = ['cityeditor'],
    scripts=[mainscript],
    **extra_options

)
