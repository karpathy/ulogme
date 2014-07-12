import sys
from setuptools import setup

setup(
    app=['ulogme_osx.py'],
    options=dict(py2app=dict(argv_emulation=True)),
)
