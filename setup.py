import os
import sys
from setuptools import setup, find_packages

setup(
    name='Replica',
    version='0.5.0',
    author='Tyler Rilling',
    author_email='tyler@underlost.net',
    description='A simple blogging CMS for Django.',
    license="MIT",
    url='https://github.com/underlost/Replica',
    zip_safe=False,
    install_requires=[
        'django',
        'psycopg2',
        'pillow',
        'bleach >= 1.4',
        'django >= 1.7, < 1.9',
        'Markdown >= 2.6.1',
    ],
    tests_require=[
        'pyflakes>=0.6.1',
        'pep8>=1.4.1'
    ],
    packages=find_packages(),
    test_suite='runtests.runtests',
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: "
                                            "Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
