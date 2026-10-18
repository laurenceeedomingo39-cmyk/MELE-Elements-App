[app]

# (str) Title of your application
title = MELE Reviewer

# (str) Package name
package.name = melereviewer

# (str) Package domain (needed for android/ios packaging)
package.domain = org.msugensan

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let extensions)
# THIS IS THE CRITICAL LINE THAT INCLUDES YOUR DATABASES
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3==3.10.12,hostpython3==3.10.12,kivy,pyjnius>=1.5.0

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
