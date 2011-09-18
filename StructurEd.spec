# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(CONFIGDIR,'support/useUnicode.py'), 'src/StructurEd.pyw'],
             pathex=['/Users/darvin/Workspace/PlistStructurEd'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'StructurEd'),
          debug=False,
          strip=None,
          upx=True,
          console=False )



import sys
if sys.platform.startswith("darwin"):
    app = BUNDLE(exe,
                 name=os.path.join('dist', 'StructurEd.app'),
                 version="0.1")