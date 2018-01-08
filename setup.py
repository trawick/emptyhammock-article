#!/usr/bin/env python3

import os
import sys

from setuptools import find_packages, setup

import articles

VERSION = articles.__version__

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()

setup(
    name='emptyhammock_article',
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2.0 License',
    version=VERSION,
    description='A Django app providing an Article model and utilities, with Django CMS integration',
    author='Emptyhammock Software and Services LLC',
    author_email='info@emptyhammock.com',
    url='https://github.com/trawick/emptyhammock-article',
    keywords=['django', 'article', 'cms'],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Alpha',
    ],
)
