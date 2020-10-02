"""Set up file for the issuemaker package."""
from pathlib import Path

from setuptools import find_packages, setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
LONG_DESCRIPTION = README_FILE.read_text(encoding="utf-8")
VERSION = (PROJECT_DIR / "issuemaker" / "VERSION").read_text().strip()
GITHUB_URL = "https://github.com/home-assistant/github-issue-maker"
DOWNLOAD_URL = f"{GITHUB_URL}/archive/master.zip"
REQUIRES = ["click", "requests"]


setup(
    name="issuemaker",
    version=VERSION,
    description="Provide a package for issuemaker",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="The Home Assistant Authors",
    author_email="hello@home-assistant.io",
    url=GITHUB_URL,
    download_url=DOWNLOAD_URL,
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    python_requires=">=3.7",
    install_requires=REQUIRES,
    include_package_data=True,
    license="Apache-2.0",
    zip_safe=False,
    entry_points={
        "console_scripts": ["issuemaker=issuemaker.cli:cli"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "'Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
