# -*- coding:utf8 -*-
import os
import sys
import codecs
import re
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


here = os.path.abspath(os.path.dirname(__file__))
package_requires = [
]
test_requires = [
    'pytest',
    'pytest-pep8',
    'pytest-flakes',
]

# Use README.rst for long description.
readme_path = os.path.join(here, 'README.rst')
long_description = ''
if os.path.exists(readme_path):
    with codecs.open(readme_path, encoding='utf-8') as fp:
        long_description = fp.read()


def find_version(*file_paths):
    version_file_path = os.path.join(*file_paths)
    try:
        with codecs.open(version_file_path) as fp:
            version_file = fp.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
        if version_match:
            return version_match.group(1)
    except OSError:
        raise RuntimeError("Unable to find version string.")
    raise RuntimeError("Unable to find version string.")


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            '--pep8',
            '--flakes',
        ]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='Ananta',
    version=find_version('ananta/__init__.py'),
    url='https://github.com/attakei/Ananta',
    description='AWS Lambda packager',
    long_description=long_description,
    author='attakei',
    author_email='attakei@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='aws lambda',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=package_requires,
    tests_require=test_requires,
    cmdclass={'test': PyTest},
    entry_points={
        "console_scripts": [
            "ananta=ananta.scripts:main",
        ]
    }
)
