"""The setup script."""

from requirements import *
from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


setup(
    author="Storm Development Ltda",
    author_email='playerstars@stormsec.com.br',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: Portuguese',
        'Programming Language :: Python :: 3.7',
    ],
    description="Componente de domínio do PlayerStars",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='playerstars_domain',
    name='playerstars_domain',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/stormsecurity/internos/playerstars/domain.git',
    version='1.0.0',
    zip_safe=False,
)
