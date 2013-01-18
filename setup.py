#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name="cepbrcache",
    version="0.0.1b",
    author="Felipe 'chronos' Prenholato",
    author_email="philipe.rp@gmail.com",
    maintainer="Felipe 'chronos' Prenholato",
    maintainer_email="philipe.rp@gmail.com",
    url="http://github.com/chronossc/cepbr-cache",
    packages = find_packages(),
    description="Generic, easy to use, file reader and importer with validations like Django forms.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=[
        "CEPBR",
        "pymongo"
    ],
)
