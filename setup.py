#!/usr/bin/env python3
# Created by Ziqiu Wang < sgwzq0810@gmail.com >

import os
import sys
from setuptools import setup, find_packages, Extension
from setuptools.command.build_py import build_py

def get_version():
    topdir = os.path.abspath(os.path.join(__file__, '..'))
    with open(os.path.join(topdir, 'prism', '__init__.py'), 'r') as f:
        for line in f.readlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise ValueError("Version string not found")


def get_platform():
    from distutils.util import get_platform
    platform = get_platform()
    if sys.platform == 'darwin':
        arch = os.getenv('CMAKE_OSX_ARCHITECTURES')
        if arch:
            osname = platform.rsplit('-', 1)[0]
            if ';' in arch:
                platform = f'{osname}-universal2'
            else:
                platform = f'{osname}-{arch}'
        elif os.getenv('_PYTHON_HOST_PLATFORM'):
            # the cibuildwheel environment
            platform = os.getenv('_PYTHON_HOST_PLATFORM')
            if platform.endswith('arm64'):
                os.putenv('CMAKE_OSX_ARCHITECTURES', 'arm64')
            elif platform.endswith('x86_64'):
                os.putenv('CMAKE_OSX_ARCHITECTURES', 'x86_64')
            else:
                os.putenv('CMAKE_OSX_ARCHITECTURES', 'arm64;x86_64')
    return platform

VERSION = get_version()
setup(
        name='prism',
        version=VERSION,
        # package_dir={'prism': 'prism'},  # packages are under directory prism
        # include *.so *.dat files. They are now placed in MANIFEST.in
        # package_data={'': ['*.so', '*.dylib', '*.dll', '*.dat']},

        include_package_data=True,  # include everything in source control
        packages=find_packages(exclude=['*test*', '*examples*']),
        # cmdclass={'build_py': CMakeBuildPy},
        description='A Quan. Chem. Package',
        long_description='This is a Quantum Chemistry package based on PySCF, with methods like NEVPT2 and MR-ADC, authored by Dr. Sokolov\'s gruop at https://github.com/sokolov-group/prism/'
        )
