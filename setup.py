# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from setuptools import find_packages, setup

setup(
    name="loog",
    description="Acsone Odoo Dev Tool",
    long_description="\n".join((open("README.md").read())),
    long_description_content_type='text/markdown',
    url='https://github.com/acsone/loog',
    packages=find_packages(where='src'),
    use_scm_version=True,
    include_package_data=True,
    install_requires=[
        "click",
        "configparser",
        "pip>=9.0.1",
        "pylint",
        "setuptools>=20,<31",
        "pytest",
    ],
    license="GPLv3+",
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: " "GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.6",
    ],
    package_dir={'': 'src'},
    python_requires='>=3.6',
    entry_points={
        'console_scripts':[
            'loog=loog.main:main',
        ]
    },
)