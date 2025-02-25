from setuptools import setup, find_packages

from mir import version

print(version.__version__)

# Module dependencies
requirements = []
with open('requirements.txt') as f:
    for line in f.read().splitlines():
        requirements.append(line)

setup(
    name='ymir-cmd',
    version=version.__version__,
    python_requires=">=3.8.10",
    author_email="ymir-team@intellif.com",
    description="mir: A data version control tool for YMIR",
    url="https://github.com/IndustryEssentials/ymir",
    packages=find_packages(exclude=["*tests*"]),
    install_requires=requirements,
    include_package_data=True,
    entry_points={"console_scripts": ["mir = mir.main:main"]},
)
