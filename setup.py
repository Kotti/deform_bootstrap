import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except:
    README = ''
    CHANGES = ''

requires = [
    'deform',
    ]

setup(
    name='deform_bootstrap',
    version='0.1a5',
    description="Bootstrap 2 compatible templates for the deform form library",
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        ],
    keywords='twitter bootstrap deform styles css web forms form',
    author='Daniel Nouri and contributors',
    author_email="pylons-discuss@googlegroups.com",
    url='http://pypi.python.org/pypi/deform_bootstrap',
    license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    )
