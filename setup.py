from os import path
from setuptools import setup


with open(path.join(path.abspath(path.dirname(__file__)), "README.md")) as f:
    long_description = f.read()


setup(
    name="conduct",
    version="0.0.0",
    url="https://github.com/lnbits/conduct",
    author="eillarra",
    author_email="eneko@illarra.com",
    license="MIT",
    description="A simple lightning nodes conductor, with a code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="bitcoin lightning-network",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    packages=["conduct"],
    package_data={"conduct": ["py.typed"]},
    install_requires=[],
    extras_require={"full": ["lnd-grpc", "pylightning", "requests"]},
    zip_safe=False,
)
