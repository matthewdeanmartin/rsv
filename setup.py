#!/usr/bin/env python

from __future__ import annotations

import glob
import os
import os.path
import sys
from typing import TYPE_CHECKING, Any

# we'll import stuff from the source tree, let's ensure is on the sys path
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

# This requires setuptools when building; setuptools is not needed
# when installing from a wheel file (though it is still needed for
# alternative forms of installing, as suggested by README.md).
from setuptools import Extension, find_packages, setup



# from setuptools.command.build_py import build_py


if TYPE_CHECKING:
    from typing_extensions import TypeGuard

def is_list_of_setuptools_extension(items: list[Any]) -> TypeGuard[list[Extension]]:
    return all(isinstance(item, Extension) for item in items)


def find_package_data(base, globs, root="rsv"):
    """Find all interesting data files, for setup(package_data=)

    Arguments:
      root:  The directory to search in.
      globs: A list of glob patterns to accept files.
    """

    rv_dirs = [root for root, dirs, files in os.walk(base)]
    rv = []
    for rv_dir in rv_dirs:
        files = []
        for pat in globs:
            files += glob.glob(os.path.join(rv_dir, pat))
        if not files:
            continue
        rv.extend([os.path.relpath(f, root) for f in files])
    return rv


package_data = ["py.typed"]

package_data += find_package_data(os.path.join("rsv"), ["*.py", "*.pyi"])

everything = [os.path.join("rsv", x) for x in find_package_data("rsv", ["*.py"])]

from mypyc.build import mypycify

opt_level = os.getenv("MYPYC_OPT_LEVEL", "3")
debug_level = os.getenv("MYPYC_DEBUG_LEVEL", "1")
force_multifile = os.getenv("MYPYC_MULTI_FILE", "") == "1"
ext_modules = mypycify(
    everything,  # + ["--config-file=mypy_bootstrap.ini"],
    opt_level=opt_level,
    debug_level=debug_level,
    # Use multi-file compilation mode on windows because without it
    # our Appveyor builds run out of memory sometimes.
    multi_file=sys.platform == "win32" or force_multifile,
)
assert is_list_of_setuptools_extension(ext_modules), "Expected mypycify to use setuptools"

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Operating System :: OS Independent"
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Software Development",
    "Typing :: Typed",
]

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="rsv",
    version="1.5.2",
    description="A module for reading and writing an RSV document file.",
    long_description=long_description,
    author="Romanin",
    author_email="semina054@gmail.com",
    keywords=["rsv", "csv", "io", "file", "format", "dump", "load", "read", "write"],

    url="https://github.com/romanin-rf/rsv",
    license="MIT",
    py_modules=[],
    ext_modules=ext_modules,
    packages=find_packages(),
    package_data={"rsv": package_data},
    entry_points={
        "console_scripts": [
            # "rsv=rsv.__main__:main",
        ]
    },
    classifiers=classifiers,
    install_requires=[
        # nothing!
        "setuptools"
    ],
    python_requires=">=3.8",
    include_package_data=True,
    project_urls={
        "Repository": "https://github.com/romanin-rf/rsv",
    },
)
