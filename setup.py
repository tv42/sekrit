#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name = "sekrit",
    version = "0.0.1",
    packages = find_packages(),

    author = "Tommi Virtanen",
    author_email = "tv@eagain.net",
    description = "manage multi-user GPG-protected secrets",
    long_description = """

TODO

""".strip(),
    license = "GPL",
    keywords = "git backup",
    url = "http://eagain.net/software/sekrit/",

    entry_points = {
        'console_scripts': [
            'sekrit-set = sekrit.cli.set_:main',
            'sekrit-get = sekrit.cli.get:main',
            'sekrit-verify = sekrit.cli.verify:main',
            ],
        },

    install_requires=[
        'GnuPGInterface',
        'setuptools>=0.6c9',
        ],

    tests_require=[
        'nose',
        ],
    )
