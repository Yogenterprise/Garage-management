from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in garage_m/__init__.py
from garage_m import __version__ as version

setup(
	name="garage_m",
	version=version,
	description="Managing garage activities",
	author="saloni",
	author_email="saloni@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
