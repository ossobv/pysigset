#!/usr/bin/env python
from distutils.core import setup

with open('README.txt') as file:
    long_description = file.read()

setup(
    name='pysigset',
    # Trying to use a PEP386 and distutils.version.StrictVersion compatible
    # versioning scheme here: 0.2a sorts before 0.2 and will mean
    # not-exactly-0.2-yet.
    version='0.2.1a',
    py_modules=['pysigset'],
    description='Signal blocking under Linux & OS X',
    long_description=long_description,
    author='Walter Doekes',
    author_email='wjdoekes@osso.nl',
    url='https://github.com/ossobv/pysigset',
    license='GPLv3+',
    platforms=('linux', 'darwin'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: GNU General Public License v3 or later '
         '(GPLv3+)'),
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries',
    ],
)

# vim: set ts=8 sw=4 sts=4 et ai tw=79:
