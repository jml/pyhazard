#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="pyhazard",
    version="0.0.1",
    description="Python client for Hazard.",
    author="Jonathan Lange",
    author_email="jml@mumak.net",
    install_requires=[
        'pyrsistent',
        'requests',
    ],
    zip_safe=False,
    packages=find_packages('.'),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
)
