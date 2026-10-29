# -*- mode: python ; coding: utf-8 -*-
# Spesifikasi PyInstaller untuk Kasir Warung Pintar
# Build: pyinstaller kasir_warung.spec

import sys
from pathlib import Path

block_cipher = None
ROOT = Path(SPECPATH)

hiddenimports = [
    "sqlalchemy.dialects.sqlite",
    "matplotlib.backends.backend_qtagg",
    "openpyxl",
    "reportlab.pdfbase._fontdata",
]

a = Analysis(
    ["main.py"],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(ROOT / "assets"), "assets"),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "PyQt5", "PyQt6"],
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
    name="KasirWarungPintar",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,           # aplikasi GUI tanpa jendela konsol
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
