import sys

import setuptools
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    #use python setup.py -a 'arguments here, like -m integration'    
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrl-complete-codimoc",
    version="0.0.1",
    author="codimoc",
    author_email="codimoc@prismoid.uk",
    description="A readline auto-completer and command line parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codimoc/pyrl-complete",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ['ply',
                        'pyreadline'],
    entry_points={
        'console_scripts': [],
    },
    tests_require=['pytest'],
    cmdclass = {'test': PyTest}, 
    package_data={"tests": ["data/*.json"],
    }
)
