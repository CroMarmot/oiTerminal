import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oiTerminal",
    version="0.0.1",
    author="Cro-Marmot",
    author_email="yexiaorain@gmail.com",
    description="terminal tool for online oi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CroMarmot/oiTerminal",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
)
