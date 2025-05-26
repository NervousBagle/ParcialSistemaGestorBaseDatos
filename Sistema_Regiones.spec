# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['Views/main.py'],
    pathex=['.', 'Controllers', 'Models', 'Views'],
    binaries=[],
    datas=[
        ('Controllers', 'Controllers'),
        ('Models', 'Models'),
        ('Recursos/Imgs', 'Recursos/Imgs'),  # Agregar el icono
    ],
    hiddenimports=[
        'Region', 
        'ControlRegion', 
        'Conexion',
        'pymysql'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'mysql.connector.locales',
        'mysql.connector.locales.eng'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Sistema_Regiones',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Recursos\\Imgs\\globe.ico',  # AGREGAR ESTA LÍNEA
)