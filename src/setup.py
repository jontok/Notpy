from setuptools import setup, find_packages
from setuptools_scm import get_version

setup(
    name='notpy',
    version=get_version(root='src', relative_to=__file__, fallback_version='0.0.1'),
    author="jontok",
    author_email="jonas@tokmaji.de",
    license="GNU General Public License v3 (GPLv3)",
    platforms="linux64",
    install_requires=[
        'Markdown==3.4.3',
    ],
    entry_points={
        'console_scripts': [
            'notpy=notpy:main'  # Use notpy.py as the entry point for the application
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
