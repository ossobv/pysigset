#!/usr/bin/env python
from distutils.core import setup
import os.path
import sys

here = os.path.dirname(__file__)
try:
    # PyPI prefers the readme as .txt
    with open(os.path.join(here, 'README.txt')) as file_:
        long_description = file_.read()
except IOError:
    # Check sdist, we *need* the README.txt in here.
    # (See Makefile in the source distribution.)
    if sys.argv[1:2] == ['sdist']:
        raise

    # We prefer it as .rst
    with open(os.path.join(here, 'README.rst')) as file_:
        long_description = file_.read()


setup(
    name='pysigset',
    # Trying to use a PEP386 and distutils.version.StrictVersion compatible
    # versioning scheme here: 0.2a sorts before 0.2 and will mean
    # not-exactly-0.2-yet.
    version='0.3.2',
    py_modules=['pysigset'],
    description='Signal blocking under Linux & OS X',
    long_description=long_description,
    author='Walter Doekes',
    author_email='wjdoekes+pysigset@osso.nl',
    url='https://github.com/ossobv/pysigset',
    license='GPLv3+',
    platforms=('linux', 'darwin'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: GNU General Public License v3 or later '
         '(GPLv3+)'),
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
)

# vim: set ts=8 sw=4 sts=4 et ai tw=79:
