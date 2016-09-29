[![Build Status](https://travis-ci.org/TheGhouls/zerolog.svg?branch=master)](https://travis-ci.org/TheGhouls/zerolog)
[![Coverage Status](https://coveralls.io/repos/github/TheGhouls/zerolog/badge.svg?branch=master)](https://coveralls.io/github/TheGhouls/zerolog?branch=master)
[![Documentation Status](https://readthedocs.org/projects/zerolog/badge/?version=latest)](http://zerolog.readthedocs.io/en/latest/?badge=latest)

# zerolog

## Introduction

Zerolog is a very simple library designed to help you capture logs from TCP, filter them, dispatch them and process them for your needs.
It gives you all needed elements to start quickly and let you focus to processing logs.

Here is an explanatory scheme of the workflow

![https://github.com/TheGhouls/zerolog/raw/master/docs/img/zerolog-base-graph.png](https://github.com/TheGhouls/zerolog/raw/master/docs/img/zerolog-base-graph.png)

All you need to do here is creating your own woker to fit your needs, you can for example store logs in database, elasticsearch, etc. or parse messages and add some logic to them.
Bonus: zerolog gives you a CLI tool to start all parts easily.

You don't want to code your worker using python ? Well good news: zeromq gives you [bindings for many programming languages](http://zeromq.org/bindings:_start) so you can create your own worker implementation using your favorite programming language

## Using zerolog with logstash

Note that you can also use zerolog with logstash pretty easily. Since logstash got a zeromq output, you can replace forwarder or receiver by logstash

![https://github.com/TheGhouls/zerolog/blob/master/docs/img/zerolog_logstash_forwarder.png](https://github.com/TheGhouls/zerolog/blob/master/docs/img/zerolog_logstash_forwarder.png)

![https://github.com/TheGhouls/zerolog/blob/master/docs/img/zerolog_logstash_receiver.png](https://github.com/TheGhouls/zerolog/blob/master/docs/img/zerolog_logstash_receiver.png)

More informations are avaibles in the documentation.

## Installation

Using pip

```
pip install zerolog
```

Via source

```
pip install -r requirements.txt
python setup.py install
```

## What's next

[See the documentation](http://zerolog.readthedocs.io/en/latest/?badge=latest)

## Running tests

Tests are written with pytest.

You can run test suite using 


```
python setup.py test
```

Or manualy using 


```
py.test -v tests/
```
