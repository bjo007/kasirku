[app]
title = Kasir Warung Pintar
package.name = kasirwarungpintar
package.domain = id.warungpintar
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,md,txt,sql
source.exclude_dirs = tests,scripts,backups,exports,receipts,logs,build,dist,.git,__pycache__,_smoke_mobile_data,assets/icons
source.exclude_patterns = *_smoke*,*.spec,.gitignore
version = 1.0.0

requirements = python3,kivy==2.3.1,kivymd==2.0.0,sqlalchemy,materialyoucolor,filetype,asyncgui,asynckivy

orientation = landscape
fullscreen = 0
android.allow_backup = True
android.minapi = 24
android.api = 34
android.archs = arm64-v8a
android.accept_sdk_license = True

icon.filename = mobile_assets/icon.png
presplash.filename = mobile_assets/presplash.png

# Nama tampilan di launcher Android
android.app_name = Kasir Warung Pintar

[buildozer]
log_level = 2
warn_on_root = 1

# Build: buildozer android debug   -> bin/kasirwarungpintar-1.0.0-arm64-v8a-debug.apk
#        buildozer android release (butuh keystore untuk publish)
