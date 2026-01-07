set -xe

# Avoid this in GHA: "ERROR: Found GNU link.exe instead of MSVC link.exe"
rm /c/Program\ Files/Git/usr/bin/link.EXE
