

from setuptools import setup, find_packages

setup(
    name="chatbot",
    version="0.1",
    packages=find_packages(where="src"),  # finds all packages under src
    package_dir={"": "src"},               # src is root for packages
)
