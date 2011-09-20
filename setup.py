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

mainscript = os.path.join('src','StructurEd.pyw')

from distutils.core import Command
from distutils.command.build import build


def needsupdate(src, targ):
    return not os.path.exists(targ) or os.path.getmtime(src) > os.path.getmtime(targ)



class BuildUiCommand(Command):
    description = "build Python modules from qrc files"

    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


    def compile_qrc(self, qrc_file, py_file):
        if not needsupdate(qrc_file, py_file):
            return
        print("compiling %s -> %s" % (qrc_file, py_file))
        try:
            import subprocess
            rccprocess = subprocess.Popen(['pyrcc4', qrc_file, '-o', py_file])
            rccprocess.wait()
        except Exception, e:
            raise distutils.errors.DistutilsExecError, 'Unable to compile resouce file %s' % str(e)
            return
    def run(self):
        self.compile_qrc( os.path.join('resources','resources.qrc'), os.path.join('src','rc.py') )

class BuildCommand(build):
    def is_win_platform(self):
        return hasattr(self, "plat_name") and (self.plat_name[:3] == 'win')

    sub_commands = [('build_ui', None)] + build.sub_commands
    #+ [('build_winext', is_win_platform)]


cmds = {
        'build' : BuildCommand,
        'build_ui' : BuildUiCommand,
        }



if sys.platform == 'darwin':
     extra_options = dict(
         setup_requires=['py2app'],
         app=[mainscript],
         # Cross-platform applications generally expect sys.argv to
         # be used for opening files.
         options=dict(
             py2app=dict(
                argv_emulation=False,
                iconfile='resources/application_icon/StructurEd.icns',
                includes=['sip'],
                packages=['PyQt4'],
                resources=["tests/test_data/sample_data.plist", "tests/test_data/sample_scheme.plist", "resources/qt.conf"]
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
         options=dict(py2exe= {"includes" : ["sip", "PyQt4"],
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
     cmdclass = cmds,
    **extra_options

)
