#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='SETools',
    version='1.2.3',
    description='Speech Enhancement Tools Packages',
    author='haoxiang',
    author_email='haoxiangsnr@gmail.com',
    maintainer='haoxiang',
    maintainer_email='haoxiangsnr@gmail.com',
    long_description=long_description,
    license='MIT',
    packages=['SETools'],
    entry_points={
        'console_scripts':[
            'SETools=SETools:cal'
        ]
    },
    zip_safe=True,
    platforms=["all"],
    url='https://github.com/haoxiangsnr/Speech_Enhancement_Tools.git',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'pystoi',
        'tqdm',
        'librosa',
        'tablib'
    ]
)
