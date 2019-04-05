#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import re

from setuptools import setup, find_packages

# Dependencies
requirements = [
    'django>=2.0.0',
    'graphene-django==2.2.0',
    'django-graphql-jwt>=0.2.1',
]

# Parse version
_version_re = re.compile(r"__version__\s+=\s+(.*)")
with open("graphene_django_ai/__init__.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

setup(
    name='graphene-django-ai',
    version=version,
    author=u'Ambient Innovation: GmbH',
    author_email='hello@ambient-innovation.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/ambient-innovation/graphene-django-ai',
    license="The MIT License (MIT)",
    description='Toolbox for changes to streamline graphene-django.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    dependency_links=['https://github.com/ambient-innovation/multiav/master/#egg=multiav', ],
    install_requires=requirements
)
