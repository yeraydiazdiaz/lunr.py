from setuptools import setup

LONG_DESCRIPTION = 'A Python implementation of Lunr.js'

setup(
    name='lunr.py',
    version='0.1',
    url='http://www.lunr.org',
    license='BSD',
    description='A Python implementation of Lunr.js',
    long_description=LONG_DESCRIPTION,
    author='Yeray Diaz Diaz',
    author_email='yeraydiazdiaz@gmail.com',
    packages=['lunr'],
    include_package_data=True,
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Text Processing',
    ],
    zip_safe=False,
)
