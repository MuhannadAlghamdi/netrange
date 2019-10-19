import netrange

from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


CLASSIFIERS = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.6',
    'Operating System :: OS Independent',
]

setup(name='netrange',
      version=netrange.__version__,
      description=netrange.__description__,
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/muhannadengineer/netrange',
      author='Muhannad Alghamdi',
      author_email='muhannadengineer@gmail.com',
      license='MIT',
      packages=['netrange'],
      classifiers=CLASSIFIERS,
      keywords='ip address port range',
      entry_points={
          'console_scripts': [
              'netrange = netrange.__main__:main'
          ]
      })
