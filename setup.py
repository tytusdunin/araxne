from distutils.core import setup
from setuptools import setup, find_packages
setup(
  name = 'araxne',
  packages = ['araxne'],
  version = '0.0.5',
  license='GPL-3.0',
  description = 'A simple algorithm for quantifying how much two strings rhyme in Polish.',
  author = 'Tytus Dunin',
  author_email = 'tm.dunin@student.uw.edu.pl',
  url = 'https://github.com/tytusdunin/araxne',
  download_url = 'https://github.com/tytusdunin/araxne/archive/refs/tags/0.0.5.tar.gz',
  keywords = ['nlp', 'rhyme detection', 'phonetics', 'polish'],
  include_package_data=True,
  package_data={
        'araxne': ['*.txt'],
  },
  install_requires=['kokosznicka'],

  classifiers=[
    'Development Status :: 4 - Beta',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

    'Programming Language :: Python :: 3',  
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)