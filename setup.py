from setuptools import setup, find_packages
from os.path import join, dirname

import iwillplay

attrs = {
    'name': iwillplay.__name__,
    'version': iwillplay.__version__,
    'author': iwillplay.__author__,
    'author_email': iwillplay.__email__,
    'url': iwillplay.__url__,
    'long_description': open(join(dirname(__file__), 'README.md')).read(),
    'packages': find_packages(),
    'install_requires': [
        'requests',
        'bs4'
    ]
}

setup(**attrs)
