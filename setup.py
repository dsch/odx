from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='odx',
    version='1.0.0',
    description='A ODX (Open Diagnostic Data Exchange) importer',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/dsch/odx',

    # Author details
    author='David Schneider',
    author_email='schneidav81@gmail.com',

    # Choose your license
    license='GNU',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='automotive diagnostics',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['odx'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
