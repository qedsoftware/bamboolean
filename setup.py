from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

from conf import PACKAGE_NAME, VERSION

curr_path = path.abspath(path.dirname(__file__))

with open(path.join(curr_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description='Interpreter of Boolean Logic Language',
    long_description=long_description,
    url='https://github.com/qedsoftware/bamboolean',
    author='Quantitative Engineering Design Inc.',
    author_email='info@qed.ai',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Interpreters',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='boolean logic interpreter',
    packages=find_packages(exclude=['tests']),
)
