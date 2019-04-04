#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

requirements = [
    'django>=2.0.0',
    'graphene-django==2.2.0',
]

setup(
    name='graphene-django-ai',
    version='1.0.0',
    author=u'Ambient Innovation: GmbH',
    author_email='hello@ambient-innovation.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/ambient-innovation/graphene-django-ai',
    license="The MIT License (MIT)",
    description='Toolbox for changes to streamline graphene-django.',
    long_description=open('README.md').read(),
    zip_safe=False,
    dependency_links=['https://github.com/ambient-innovation/multiav/master/#egg=multiav', ],
    install_requires=requirements
)
