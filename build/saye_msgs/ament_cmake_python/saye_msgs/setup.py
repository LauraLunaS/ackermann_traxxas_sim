from setuptools import find_packages
from setuptools import setup

setup(
    name='saye_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('saye_msgs', 'saye_msgs.*')),
)
