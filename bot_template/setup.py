"""
Установщик пакета
"""

import setuptools
from setuptools import find_packages


with open("README.md") as fh:
    long_description = fh.read()

requires = open('requirements.txt').read().split('\n')


setuptools.setup(
    name="bot_template",
    version="0.0.1",
    author="Grigory Ovchinnikov",
    author_email="ogowm@hotmail.com",
    description="Telegram bot template.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JointEntropy/",
    packages=find_packages(),
    install_requires=requires,
    setup_requires=[
        'pytest-runner',
    ]
)
