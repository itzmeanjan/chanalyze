#!/usr/bin/python3

from setuptools import setup

setup(
    name='chanalyze',
    version='0.1.0',
    description='A simple WhatsApp Chat Analyzer ( for both Private & Group chats ), made with <3',
    author='Anjan Roy',
    author_email='anjanroy@yandex.com',
    maintainer='Anjan Roy',
    maintainer_email='anjanroy@yandex.com',
    url='https://github.com/itzmeanjan/chanalyze',
    license='MIT',
    keywords='whatsapp chat analysis data visualization',
    py_modules=['app', 'util', 'model', 'model.*'],
    entry_points={
        'console_scripts': [
            'app = app:main'
        ]
    },
    install_requires=['matplotlib>=3.0.*'],
    python_requires='~=3.6'
)
