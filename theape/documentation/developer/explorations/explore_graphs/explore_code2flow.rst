Code2Flow Explorations
======================

This is a look at what `code2flow <https://github.com/scottrogowski/code2flow>`_ does. It does not appear to be on pypi but you can use git to get it and do the usual installation::

   git clone https://github.com/scottrogowski/code2flow.git
   cd code2flow
   python setup.py install

A dump of the ``--help``:

.. literalinclude:: code2flow_help.txt

A fairly minimal interface.

::

    file_name = plugin.__file__.rstrip('c')
    command = 'code2flow --language py -o plugin_flow.png {0}'.format(file_name)
    subprocess.call(shlex.split(command))
    



.. image:: plugin_flow.png

It does not seem to be as successful as pyreverse in finding things.