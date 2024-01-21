from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in gm/__init__.py
from gm import __version__ as version

setup(
	name="gm",
	version=version,
	description="Garage Management",
	author="aazar",
	author_email="shaikhaazar11",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
