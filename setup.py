from setuptools import setup, find_packages
from os import path
from io import open
from bsl2sq.__version__ import __version__

here_path = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='bsl2sq',
      python_requires='>=3.6.0',
      version=__version__,
      description='bsl file finder to sonarqube',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Aleksey Maksimkin',
      author_email='maximkin@mail.ru',
      url='https://github.com/brobots-corporation/bsl2sq',
      license='GPL-3.0',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Natural Language :: Russian',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      packages=find_packages(),
      tests_require=['coverage', 'unittest-xml-reporting'],
      test_suite='tests',
      entry_points={
          'console_scripts': [
              'bsl2sq=bsl2sq.app:bsl2sq'
          ]
      },
      project_urls={
          'Bug Reports': 'https://github.com/brobots-corporation/bsl2sq/issues',
          'Source': 'https://github.com/brobots-corporation/bsl2sq',
      }
      )
