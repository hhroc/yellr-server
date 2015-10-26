import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'mutagen',
    'markdown',
    'python-magic',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'sqlalchemy',
    'sqlalchemy_utils',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'requests',
    ]

setup(name='yellr-server',
      version='0.0',
      description='yellr-server',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='yellr_server',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = yellr_server:main
      [console_scripts]
      initialize_yellr-server_db = yellr_server.scripts.initializedb:main
      """,
      )
