from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='webcorp-crawler',
      version=version,
      description="A simple scraping tool for getting stuff out of web corpora",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='crawling corpora',
      author='Juho Härme',
      author_email='juho.harme@gmail.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
