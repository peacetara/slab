"""
horrible. seriously.
"""
import os

from setuptools import setup

VERSION = "0.1.0"


def readme():
    """ Load the contents of the README file """
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, "r") as f:
        return f.read()

def read_requirements(filename):
    reqs = []
    with open(filename, 'r') as f:
        for line in f:
            reqs.append(line.strip())
    return reqs

setup(
    name="slab",
    version=VERSION,
    author="Tara Sawyer",
    author_email="tara@birl.org",
    description="A Python replacement for sudolikeaboss",
    long_description=readme(),
    license="MIT",
    url="",
    classifiers=[],
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('requirements-tests-py3.txt'),
    packages=[
        'onepassword',
        'slab'
    ],
    entry_points= {
        'console_scripts':['slab=slab.main:main','slabpw=slab.main:pwentry'],

    },

)