from setuptools import setup


setup(name='netrange',
      version='0.0.6',
      description='Script to range multiple IPs and ports',
      url='https://github.com/muhannadengineer/iprange',
      author='Muhannad Alghamdi',
      author_email='muhannadengineer@gmail.com',
      license='MIT',
      packages=['netrange'],
      entry_points={
          'console_scripts': [
              'netrange = netrange.cli:main'
          ]
      },
      keywords='ip address port range')
