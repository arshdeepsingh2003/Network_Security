'''
The setup.py file is an essential part of 
packaging and distributing Python Projects.
 It is used by setuptools(or distutils in older Python versions) to define
the configurationof your project , such as its
metadata , dependencies and more


The setup.py file helps you prepare your
 Python project so it can be shared or 
installed by others.It tells Python 
important details about your project,
 like its name, version, required libraries (dependencies), and other basic information.
Tools like setuptools use this file to
 package your project properly.
'''
#It automatically finds all the folders that are Python packages (folders that have __init__.py inside them).
from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            #read lines from the file
            lines = file.readlines()
            #Process each line
            for line in lines:
                requirement=line.strip()
                #ignore empty lines and -e .
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("reqirements.txt not found")

    return requirement_lst

setup(
    name="Network Security",
    version="0.0.1",
    author="Arshdeep Singh",
    author_email="arshdeepgtbit@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)