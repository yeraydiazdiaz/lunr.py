#!/bin/bash

# To be executed on a manylinux1 Docker container with Rust nightly
set -ex

# for PYBIN in {python3.5,python3.6,python3.7,python3.8}; do
for PYBIN in python3.5; do
    export PYTHON_SYS_EXECUTABLE="$PYBIN"

    rm -fr .venv
    "${PYBIN}" -m venv .venv
    source .venv/bin/activate
    "${PYBIN}" -m pip install -U setuptools wheel setuptools-rust
    "${PYBIN}" setup.py bdist_wheel
done
