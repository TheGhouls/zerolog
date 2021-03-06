from setuptools import setup, find_packages


__version__ = "0.3"


setup(
    name="zerolog",
    version=__version__,
    author="TheGhouls",
    author_email="manu.valette@gmail.com",
    packages=find_packages(),
    description="Minimalist and agnostic log aggregation with zeromq from tcp",
    url="https://github.com/TheGhouls/zerolog",
    keywords=["logging", "logs", "zeromq", "rsyslog"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ],
    install_requires=[
        "pyzmq"
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-timeout', 'mock'],
    entry_points={
        'console_scripts': [
            'zerolog = zerolog.commands.main:main'
        ]
    }
)
