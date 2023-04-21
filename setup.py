from setuptools import setup
from setuptools_scm import get_version

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='notpy',
    version=get_version(root='.', relative_to=__file__, fallback_version='0.0.2'),
    description="Create/Delete files and edit them as markdown files in neovim",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="jontok",
    author_email="jonas@tokmaji.de",
    license="GNU General Public License v3 (GPLv3)",
    packages=["notpy"],
    package_dir={"notpy":"notpy/"},
    platforms="linux64",
    keywords="notes markdown python nvim neovim",
    install_requires=[
        'Markdown==3.4.3',
    ],
    entry_points={
        'console_scripts': [
            'notpy=notpy.notpy:main'
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.10',
    ],
    data_files=[
        ("share/applications/", ["notpy.desktop"])
    ],
    python_requires=">=3.9"
)
