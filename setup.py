#!/usr/bin/python
#

from __future__ import with_statement
import setuptools

requires = [
    "flake8 > 3.0.0",
    "ansible == 2.4.0"
]

setuptools.setup(
    name="f5-ansible",
    license="GPL3",
    version="1.0.0",
    description="Ansible modules for F5 products",
    author="Tim Rupp",
    author_email="t.rupp@f5.com",
    url="https://github.com/F5Networks/f5-ansible",
    data_files=[
        (
            'library',
            [
                'bigip_pool.py',
                'bigip_selfip.py'
            ]
        )
    ],
    install_requires=requires,
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
