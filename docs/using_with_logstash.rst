Using zerolog with logstash
===========================

Since logstash got a zeromq output, you can simply integrate it with zerolog.

Replacing zerolog forwarder with logstash
-----------------------------------------

Logstash can act like the forwarder, all you need to do is to configure your logstash to output logs to a zeromq pub socket, for example :

.. code-block:: bash

   input {
     tcp {
       port => 6000
     }
    }
    output {
      zeromq {
        address => ["tcp://*:6001"]
        mode => "server"
        topology => "pubsub"
        topic => "apache-logs"
      }
    }

Note that in pubsub mode you can also specify a topic to route logs to correct receivers.


Replacing zerolog receiver with logstash
----------------------------------------

Maybe you don't need any forwarder at all and you only want a simple receiver to workers pattern. Logstash can also replaces
receiver or sends logs directly to workers, for example :

.. code-block:: bash

   input {
     tcp {
       port => 6000
     }
    }
    output {
      zeromq {
        address => ["tcp://*:6200"]
        mode => "server"
        topology => "pushpull"
      }
    }

With this configuration file, all workers will receive tasks directly from logstash, avoiding the use of receiver
