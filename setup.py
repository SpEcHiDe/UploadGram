#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Upload (and download) files to Telegram upto 2 GiB
"""
import os
import glob
from setuptools import setup, find_packages

AUTHOR = "SpEcHIDe"
EMAIL = "spechide@shrimadhavUK.me"
URL = "https://github.com/SpEcHiDe/UploadGram/"

PACKAGE_NAME = "uploadgram"
PACKAGE_DOWNLOAD_URL = (
    "https://github.com/SpEcHiDe/UploadGram/archive/master.zip"
)
MODULE = "uploadgram"
REQUIREMENT_FILE = "requirements.txt"
KEYWORDS = ["telegram-upload", "telegram", "upload", "video", "audio"]
LICENSE = "AGPL license"


def read_requirement_file(path):
    with open(path) as f:
        return f.readlines()


def get_package_version(module_name):
    return __import__(module_name).__version__


def get_packages(directory):
    # Search modules and submodules to install
    # (module, module.submodule, module.submodule2...)
    packages_list = find_packages(directory)
    # Prevent include symbolic links
    for package in tuple(packages_list):
        path = os.path.join(directory, package.replace(".", "/"))
        if not os.path.exists(path) or os.path.islink(path):
            packages_list.remove(package)
    return packages_list


# paths
here = os.path.abspath(os.path.dirname(__file__))
readme = glob.glob("{}/{}*".format(here, "README"))[0]
scripts = [
    os.path.join(
        "scripts",
        os.path.basename(script)
    ) for script in glob.glob(
        "{}/scripts/*".format(here)
    )
]
# Package data
packages = get_packages(here)
modules = list(filter(lambda x: "." not in x, packages))
module = MODULE if MODULE else modules[0]


setup(
    name=PACKAGE_NAME,
    version=get_package_version(module),
    packages=["uploadgram"],

    description=__doc__.replace("\n", " "),
    long_description=open(readme, "r").read(),
    keywords=KEYWORDS,
    download_url=PACKAGE_DOWNLOAD_URL,

    author=AUTHOR,
    author_email=EMAIL,
    url=URL,

    install_requires=read_requirement_file(REQUIREMENT_FILE),

    entry_points={
        "console_scripts": [
            "uploadgram=uploadgram.shell:main"
        ],
    },

)
