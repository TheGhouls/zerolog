Running elements
================

Zerolog provide command line tool to start every element. This section will explain how to start each element of zerolog

Running forwarder
-----------------

The forwarder is in charge of receiving logs from external services and to forward them to receivers.
Thanks to zeromq PUB/SUB pattern, you can also use topic to filter messages. In this way you can associate receivers with specifics logs messages.

Like for all elements, zerolog provide a command to start a forwarder :

.. code-block:: bash

   usage: zerolog forwarder [-h] [-f FRONTEND] [-b BACKEND] [-m MONITOR]

   optional arguments:
       -h, --help            show this help message and exit
       -f FRONTEND, --frontend FRONTEND
                             frontend port for sending data to receivers
       -b BACKEND, --backend BACKEND
                             backend port for receiving data
       -m MONITOR, --monitor MONITOR
                             monitor port for publishing data

Forwarder's parameters are all optional and will use default values if not provided, so you can run a forwarder using only :

.. code-block:: bash

   zerolog forwarder

Only monitor socket will not be set if the ``-m`` option is not provided. The monitor socket only role is to output messages received by the forwarder, so you can easily check if logs messages are able to hit the forwarder and are correctly sending back messages to receivers.

Running receiver
----------------

The receiver is in charge to filter messages incomming from forwarder and dispatch them to a pool of workers. By default, receiver will not filter on any topic and will receive all messages from forwarder.

Command usage :

.. code-block:: bash

   usage: zerolog receiver [-h] [-t TOPIC] [-l LOG_CONFIG]
                        [--output-port OUTPUT_PORT | --output-socket OUTPUT_SOCKET]
                        forwarder_address forwarder_port

   positional arguments:
   forwarder_address     address of running forwarder
   forwarder_port        port of running forwarder

   optional arguments:
     -h, --help         show this help message and exit
     -t TOPIC, --topic TOPIC
                        optional topic to subscribe
     -l LOG_CONFIG, --log-config LOG_CONFIG
                        location of logging configuration file (python
                        standard logging configuration file)
     --output-port OUTPUT_PORT
                        output TCP port for workers (default to 6200)
     --output-socket OUTPUT_SOCKET
                        output unix socket for workers

``forwarder_address`` and ``forwarder_port`` are both mandatory. The first one need to be a valid address for connecting to your forwarder (e.g: ``"127.0.0.1"`` and the second one is the ``frontend`` port of your forwarder.

``topic`` parameter is optional and default is to accept any message from forwarder. But you can configure your can use specific topic for filtering messages, for example if you only want nginx logs for this receiver. This allow you to use only one forwarder for all messages and all processes.

``--log-config`` parameter is pretty obvious here. This one can be usefull for sending an email, or logging to sentry (for example) if the receiver crash.

``output-port`` and ``output-socket`` parameters will be used to bind the ventilator socket (the one in charge of sending messages to workers). You can't set them both, but you can choose between unix socket (if workers are on the same machine for example) or classic TCP port

Running workers
---------------

The worker is in charge of processing logs messages and apply your own logic on them.

Command :

.. code-block:: bash

   usage: zerolog worker [-h] [-d DIRECTORY] backend worker_class

   positional arguments:
       backend               backend to connect for receiving message (e.g:
                             tcp://127.0.0.1:6200)
       worker_class          class to use as worker

   optional arguments:
       -h, --help            show this help message and exit
       -d DIRECTORY, --directory DIRECTORY
                             directory to append to sys.path for import (optional)

As you can see, this command aim to allow you to start your own workers. Only restriction is that your workers must take a ``backend`` parameter in ``__init__`` method, and have a ``run`` method.

For simplicity you can simply extends the ``BaseWorker`` class avaible in zerolog.

``backend`` parameter here is a full zeromq connection string, allowing you to connect to any backend (TCP or unix socket)

``worker_class`` represent a full import path to the wanted worker class (e.g: ``zerolog.worker.BaseWorker``. 

``--directory`` parameter allow you to append a specific directory to python path. With this you can use a ``worker_class`` from anywhere and without installing anything, a simple python file could be used to declare your worker
