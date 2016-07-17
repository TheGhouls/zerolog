Using supervisor
================

All your elements are ready to be used and can be start using CLI, but it's not realy suitable for production.

For starting and managing your processes you can use for example supervisor. Here is a simple configuration file :

.. code-block:: INI

   [program:zerolog-forwarder]
   command=zerolog forwarder
   autostart=true
   autorestart=true

   [program:zerolog-receiver]
   command=zerolog receiver 127.0.0.1 6001
   autostart=true
   autorestart=true

   [program:zerolog-worker]
   command=zerolog worker "tcp://127.0.0.1:6001" worker.MyWorker -d /home/user
   numprocs=8
    
With this file, all your work chain is ready to get messages and process them
