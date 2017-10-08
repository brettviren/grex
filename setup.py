from setuptools import setup, find_packages
setup(
    name='grex',
    version=open("version.txt").readlines()[0],
    packages = find_packages(),
    install_requires = open("requirements.txt").read().split('\n'),
    entry_points = dict(
        console_scripts = [
            'grex = grex.main:main',
        ]
    )
)
