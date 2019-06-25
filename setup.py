from setuptools import setup

setup(
    name='lprojection',
    version='0.0.1',
    description='Projection layout for graphs',
    license='BSD-3-Clause',
    packages=['lprojection'],
    author='Ricardo R. da Silva',
    install_requires=[
          'pandas',
          'numpy',
          'networkx',
          'matplotlib',
          'sklearn',
          'requests',
          'click',
          'cython',
    ],
    scripts=['bin/layout_script'],
    author_email='ridasilva@ucsd.edu'
)
