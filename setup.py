from setuptools import find_packages , setup
from typing import List

HYPEM_E_DOT = '-e .'
def get_requirements(file_path:str)->list[str]:
    '''
    this function will return the list of requirementns
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readline()
        requirements=[req.replace ('\n' , '')for req in requirements]

        if HYPEM_E_DOT in requirements:
            requirements.remove(HYPEM_E_DOT)
setup(
    name= 'mlproject',
    version='0.0.1',
    author='Shisank',
    author_email='shisankyadav8@gmail.com',
    packages= find_packages(),
    install_requires=get_requirements('requirements.txt')
)