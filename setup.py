from setuptools import find_packages
from setuptools import setup

# 1. Read the requirements.txt file so you don't list packages twice
with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(
    name="luxury_project",     
    version="1.0",
    description="Luxury Data Analysis for EDHEC",
    packages=find_packages(),  
    install_requires=requirements
)