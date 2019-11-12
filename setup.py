import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cronpi",
    version="2.0.0",
    author="dakc",
    author_email="dakc@outlook.jp",
    description="a small crontab deploying package for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dakc/cronpi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python ",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    License="MIT",
)