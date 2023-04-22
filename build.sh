#!/bin/bash
echo $(./env/bin/stoml_linux_amd64 pyproject.toml tool.poetry.version)
version=$(./env/bin/stoml_linux_amd64 pyproject.toml tool.poetry.version)

pip uninstall notpy -y

source env/bin/activate

# build package
poetry build

deactivate

pip install dist/notpy-${version}.tar.gz

ls -lah /home/jt/.local/lib/python3.10/site-packages/notpy/

# Tests
notpy help
