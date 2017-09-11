#!/usr/bin/python
#

from __future__ import with_statement
import setuptools

requires = [
    "flake8 > 3.0.0",
]

setuptools.setup(
    name="F5 Ansible modules",
    license="GPL3",
    version="1.0.0",
    description="Ansible modules for F5 products",
    author="Tim Rupp",
    author_email="t.rupp@f5.com",
    url="https://github.com/F5Networks/f5-ansible",
    packages=[
        "f5-ansible",
    ],
    install_requires=requires,
    entry_points={
        'flake8.extension': [
            'F5 = flake8_example:ExamplePlugin',
        ],
    },
    classifiers=[
        "Framework :: Ansible",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache 2 License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Topic :: Software Development :: Libraries :: Ansible Modules"
    ]
)
