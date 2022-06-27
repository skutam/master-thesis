from setuptools import setup

from codecs import open
from os import path

# The directory containing this file
_pwd = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(_pwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='proactive-password-checker',
    version='0.1.0',
    description='Proactive password checker is a tool for finding weak passwords, by calculating the similarity rate with a weak dataset we produced.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matúš Škuta',
    author_email='xskuta04@vutbr.cz',
    packages=['ProactivePasswordChecker'],
    include_package_data=True,
    install_requires=[]
)
