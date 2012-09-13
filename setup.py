# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe

setup(
options = {'py2exe': {'bundle_files': 1, 'includes': 'numpy' } },
console=['pekagame.py']
)