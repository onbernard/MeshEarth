from distutils.core import setup
from setuptools import find_packages

setup(
    # Project name:
    name='meshEarth_onbernard',

    # Packages to include in the distribution:
    packages=find_packages(','),

    # Project version number:
    version='0.0.1',

    # List a license for the project, eg. MIT License
    license='MIT License',

    # Short description of your library:
    description='Transformation from MeshRoom coordinates to local tangential plane coordinates',

    # Your name:
    author='Onésime BERNARD',

    # Your email address:
    author_email='',

    # Link to your github repository or website:
    url='',

    # Download Link from where the project can be downloaded from:
    download_url='',

    # List of keywords:
    keywords=[],

    # List project dependencies:
    install_requires=[
        "pandas",
        "numpy",
        "sklearn",
        "pyproj",
        "pyyaml"
    ],

    # https://pypi.org/classifiers/
    classifiers=[]
)
