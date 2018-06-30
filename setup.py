import os
import re
from setuptools import setup


PATH = os.path.abspath(os.path.dirname(__file__))


def read_file(filepath):
    with open(filepath, 'r') as fd:
        return fd.read()


def find_version():
    version_path = os.path.join(PATH, 'lunr', '__init__.py')
    contents = read_file(version_path)
    version_string = contents[contents.index('__VERSION__'):]
    try:
        return re.match(
            r'.*__VERSION__ = [\'"]([\d\w\.]+)[\'"]', version_string).group(1)
    except AttributeError:
        raise RuntimeError("Unable to find version string.")


setup(
    name='lunr',
    version=find_version(),
    url='https://github.com/yeraydiazdiaz/lunr.py',
    license='MIT',
    description='A Python implementation of Lunr.js',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Yeray Diaz Diaz',
    author_email='yeraydiazdiaz@gmail.com',
    packages=['lunr'],
    include_package_data=True,
    install_requires=[
        'future==0.16.0',
        'six==1.11.0',
    ],
    extras_require={
        'languages': ['nltk==3.2.5']
    },
    keywords='lunr full text search',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Text Processing',
    ],
)
