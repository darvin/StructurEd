#~/bin/sh
pyrcc4 resources/resources.qrc -py2 -o src/rc.py
PATH_TO_QT_FRAMEWORK=/usr/local/Cellar/qt/4.7.3/lib/QtGui.framework/
PATH_TO_PYINSTALLER=~/Workspace/pyinstaller/
arch -i386 python ${PATH_TO_PYINSTALLER}pyinstaller.py PlistStructurEd.spec
cp -rv ${PATH_TO_QT_FRAMEWORK}Versions/4/Resources/qt_menu.nib dist/PlistStructurEd.app/Contents/Resources/
