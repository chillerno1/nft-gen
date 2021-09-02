from setuptools import setup, find_packages

setup(
    name="nftgen",
    version="0.1.0",
    author="gimme.dev",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        "numpy",
        "Pillow",
        "PyYAML",
    ],
)
