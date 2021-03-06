# -*- coding:utf8 -*-
from __future__ import unicode_literals
import os
import sys
import codecs
import re
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


dev_version = 1
here = os.path.abspath(os.path.dirname(__file__))
package_requires = [
    'venusian'
]
test_requires = [
    'pytest',
    'pytest-pep8',
    'pytest-flakes',
    'pytest-cov',
]

# Use README.rst for long description.
readme_path = os.path.join(here, 'README.rst')
long_description = ''
if os.path.exists(readme_path):
    with codecs.open(readme_path, encoding='utf-8') as fp:
        long_description = fp.read()


def find_version(*file_paths):
    if os.environ.get('PRODUCTION', '0') == '1':
        suffix = ''
    else:
        suffix = '.dev' + str(dev_version)
    version_file_path = os.path.join(*file_paths)
    try:
        with codecs.open(version_file_path) as fp:
            version_file = fp.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
        if version_match:
            return version_match.group(1) + suffix
    except OSError:
        raise RuntimeError("Unable to find version string.")
    raise RuntimeError("Unable to find version string.")


class PyTest(TestCommand):
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
    name='ananta',
    version=find_version('ananta/__init__.py'),
    url='https://github.com/attakei/ananta',
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
    extras_require={'test': test_requires},
    cmdclass={'test': PyTest},
    entry_points={
        "console_scripts": [
            "ananta=ananta.scripts:main",
        ]
    }
)
