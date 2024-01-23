# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['appdirs', 'fsspec', 'simple_term_menu']
hiddenimports += collect_submodules('fsspec')
hiddenimports += collect_submodules('appdirs')
hiddenimports += collect_submodules('simple_term_menu')

a = Analysis(
    ['source/main.py', 'source/battle.py', 'source/check_yaml.py', 'source/colors.py', 'source/train.py', 'source/logger_sys.py', 'source/term_menu.py', 'source/mission_handling.py', 'source/dialog_handling.py', 'source/enemy_handling.py', 'source/data_handling.py', 'source/npc_handling.py', 'source/text_handling.py', 'source/zone_handling.py', 'source/uuid_handling.py', 'source/weapon_upgrade_handling.py'],
    pathex=[],
    binaries=[],
    datas=[('yamale/VERSION', 'yamale')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['fcntl'],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Bane-Of-Wargs',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)