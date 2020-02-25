# Copyright 2019 ACSONE SA/NV (<https://acsone.eu/>)

from setuptools import find_packages, setup

setup(
    name="loog",
    description="An Odoo log parsing and enrichment library and CLI.",
    long_description="\n".join(open("README.md").read()),
    long_description_content_type="text/markdown",
    url="https://github.com/acsone/loog",
    packages=find_packages(where="src"),
    use_scm_version=True,
    include_package_data=True,
    install_requires=[
        "click",
        "configparser",
        'importlib_metadata ; python_version<"3.8"',
    ],
    license="mit",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.6",
    ],
    package_dir={"": "src"},
    python_requires=">=3.6",
    setup_requires=["setuptools_scm"],
    entry_points={"console_scripts": ["loog=loog.main:main"]},
)
