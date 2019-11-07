import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cronpi",
    version="1.0.0",
    author="dakc",
    author_email="dakc@outlook.jp",
    description="a small crontab deploying package for python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dakc/cronpi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.0',
)