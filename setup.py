from setuptools import setup, find_packages


__version__ = "0.1"


setup(
    name="zerolog",
    version=__version__,
    author="TheGhouls",
    author_email="manu.valette@gmail.com",
    packages=find_packages(),
    description="Minimalist and agnostic log aggregation with zeromq from tcp",
    url="https://github.com/TheGhouls/zerolog",
    keywords=["logging", "logs", "zeromq", "rsyslog"],
    classfifiers=[
        "Programming Language :: Python :: 3.5"
    ],
    install_requires=[
        "pyzmq"
    ]
)

