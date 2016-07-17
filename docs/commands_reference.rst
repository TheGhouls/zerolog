Commands reference
==================

forwarder
---------

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


receiver
--------

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


worker
------

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
