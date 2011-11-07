from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='plone.app.contentlistingtile',
      version=version,
      description="",
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],

      keywords='',
      author='Plone Foundation',
      author_email='',
      url='http://svn.plone.org/svn/collective/',

      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'plone.app.querystring',
        'plone.directives.tiles',
        # -*- Extra requirements: -*-
        ],

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
