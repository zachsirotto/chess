import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chess",
    version="0.0.1",
    author="Zach Sirotto",
    author_email="zach.sirotto@ibm.com",
    description="A chess game :)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zachsirotto/chess",
    packages=setuptools.find_packages(),
    install_requires=["PyQt5", "chess"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
