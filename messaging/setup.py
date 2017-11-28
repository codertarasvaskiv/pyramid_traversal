import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


requires = [
    'bcrypt',
    'cornice',
    'couchdb-schematics == 1.1.1',
    'pyramid',
    'pyramid_jinja2',
    'schematics == 1.1.1',
    'waitress',
    'jsonpatch==1.16',
    'pytz'
]

setup(name='messaging',
      version=0.1,
      description='Cornice tutorial',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
      ],
      keywords="web services",
      author='',
      author_email='',
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main=messaging:main
      """,
      paster_plugins=['pyramid'])
