Logging error in receiver
=========================


Receiver start command can take a logging file in parameter. If provided this file will be used to configure the logger of the module.

For example, here is a simple log file :

.. code-block:: ini

   [loggers]
   keys=root,simpleExample

   [handlers]
   keys=consoleHandler

   [formatters]
   keys=simpleFormatter

   [logger_root]
   level=DEBUG
   handlers=consoleHandler

   [logger_simpleExample]
   level=DEBUG
   handlers=consoleHandler
   qualname=simpleExample
   propagate=0

   [handler_consoleHandler]
   class=StreamHandler
   level=DEBUG
   formatter=simpleFormatter
   args=(sys.stdout,)

   [formatter_simpleFormatter]
   format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
   datefmt=

As you can see this is standard python logging configuration file.

Receiver is configured to log an error in case of exception and keyboard interruption. Using a custom logger can allow you to have quick informations in case of failure and will be very helpful in case of receiver crash.
