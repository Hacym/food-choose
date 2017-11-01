from setuptools import setup, find_packages
from pip.req import parse_requirements
"""
A simple API for choosing which food you will eat.
"""

try:
    reqs = [str(ir.req) for ir in parse_requirements('requirements.txt')]
except Exception as e:
    reqs = [str(ir.req) for ir in parse_requirements('requirements.txt', session = False)]

setup(
    name='food_choose',
    version='1.0.0',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=True,
    install_requires=reqs,
)

