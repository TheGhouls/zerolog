Creating your own workers
=========================

One of the main goal of zerolog is to provide all needed elements to start receive and process logs easily. Principales parts of the chain are built-in and can be used "as-is" but
one must be implemented: the worker.

The worker is the core of your process, it's in charge of processing logs to fit your needs.

To help you creating your worker, zerolog provide a ``BaseWorker`` class that can be inherited. This class provide anything needed to start (binding to receiver, run loop).
All you need to do to create your own worker is to implement ``process_data`` method in your worker class. Let's take a simple example :


.. code-block:: python

   import sqlite3
   from zerolog.worker import BaseWorker


   class MyWorker(BaseWorker):

       def __init__(self, backend, *args, **kwargs):
           super(MyWorker, self).__init__(backend, *args, **kwargs)
           self.connection = sqlite3.connect("/tmp/example.db")
           self.cursor = self.connection.cursor()

       def process_data(self, data):
           print(data)
           self.cursor.execute('''
           INSERT INTO logs (message) values (?)''', [data])
           self.connection.commit()


This example is very simple, it will only print data on stdout and save received message in sqlite database. But this example give you a good start for creating your own worker.

Now let's start this worker. Let's assume that your ``worker.py`` file is located in ``/home/user/`` directory.

.. code-block:: bash

   zerolog worker "tcp://127.0.0.1:6001" worker.MyWorker -d /home/user/

And that's it ! Your worker is running, ready to receive messages and process them
