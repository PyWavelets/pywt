rem Configure the environment for 32-bit builds.
rem Use "vcvars32.bat" for a 32-bit build.
"C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\bin\vcvars32.bat"
setenv /x86 /release
rem Convince setup.py to use the SDK tools.
set MSSdk=1
set DISTUTILS_USE_SDK=1
