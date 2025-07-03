from setuptools import setup, find_packages
from typing import List


def get_requirements() -> List[str]:
    """
    Returns a list of requirements for the project.
    """

    requirement_list:List[str] = []

    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and line != '-e .':
                    requirement_list.append(line)
    except FileNotFoundError:
        print("requirements.txt file not found.")

    return requirement_list

print(get_requirements())

setup(
    name='AI-travel_planner',
    version='0.1.0',
    author='Saketh',
    packages=find_packages(),
    install_requires=get_requirements(),
)

