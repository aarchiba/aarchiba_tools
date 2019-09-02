#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aarchiba_tools",
    author="Anne Archibald",
    author_email="peridot.faceted@gmail.com",
    description="Convenient python (3) tools I often use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aarchiba/aarchiba_tools",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    keywords=["personal"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "six", "astropy", "astroplan"],
    include_package_data=True,
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
)
