from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bite",
    version="0.1",
    author="Samson Tan",
    author_email="samson.tan@salesforce.com",
    description="A tokenizer that splits words into bases and inflections.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/salesforce/bite",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: OSI Approved :: BSD License",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
