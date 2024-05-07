# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('extra/service.json', 'extra'), ('main.kv', '.'), ('ui/login.kv', 'ui/'), ('ui/projects.kv', 'ui/'), ('ui/suppliers.kv', 'ui/'), ('ui/clients.kv', 'ui/'), ('ui/resources.kv', 'ui/'), ('ui/manpower.kv', 'ui/'), ('ui/finances.kv', 'ui/'), ('ui/archive.kv', 'ui/'), ('validation.kv', '.'), ('visuals/icon.png', 'visuals'), ('visuals/icon.ico', 'visuals'), ('log.txt', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RohanApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='visuals/icon.ico'
)
