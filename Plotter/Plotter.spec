# -*- mode: python -*-

block_cipher = None


a = Analysis(
  ['run.py'],
  pathex=['/Users/kestin/Projects/Plotter'],
  binaries=[],
  datas=[],
  hiddenimports=['PyQt5.sip'],
  hookspath=[],
  runtime_hooks=[],
  excludes=[],
  win_no_prefer_redirects=False,
  win_private_assemblies=False,
  cipher=block_cipher
)

pyz = PYZ(
  a.pure, 
  a.zipped_data,
 cipher=block_cipher
)

exe = EXE(
  pyz,
  a.scripts,
  exclude_binaries=True,
  name='Plotter',
  debug=False,
  strip=False,
  upx=False,
  console=False
)

coll = COLLECT(
  exe,
  a.binaries,
  a.zipfiles,
  a.datas,
  strip=False,
  upx=False,
  name='Plotter'
)

app = BUNDLE(
  coll,
  name='Plotter.app',
  icon='img/icon.icns',
  bundle_identifier=None
)
