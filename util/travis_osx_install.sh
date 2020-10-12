#!/bin/bash
travis-wait-improved --timeout 30m brew update
brew install ccache

git clone --depth 1 --branch devel https://github.com/matthew-brett/multibuild ~/multibuild
source ~/multibuild/osx_utils.sh
get_macpython_environment $MB_PYTHON_VERSION ~/macpython_venv

source ~/macpython_venv/bin/activate
pip install virtualenv
