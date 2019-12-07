from setuptools import setup, find_packages

cmdclass = {}

version = '0.0.4'
description = 'Create a filtered view of sequences through indices.'

packages = find_packages()

setup(
    name='filtr',
    version=version,
    description=description,
    cmdclass=cmdclass,
    packages=packages,
    install_requires=[
    ],
    setup_requires=[
    ],
    tests_require=[
        'mypy',
        'flake8',
        'pytest',
    ],
    classifiers=[
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering'
    ],
)
