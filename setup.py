import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grimoire-if",
    version="1.0.7",
    install_requires=["hype-html"],
    author="Scott Russell",
    author_email="me@scottrussell.net",
    description="Static Interactive Fiction Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scrussell24/grimoire",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
