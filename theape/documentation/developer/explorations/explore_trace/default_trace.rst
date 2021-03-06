The Default Trace
=================

::

    # python standard library
    from trace import Trace
    
    from test_class import TestExec
    



The ``exec`` Statement
----------------------

To use ``Trace`` you can pass its ``run`` method either a string or an object that the `exec <http://docs.python.org/2/reference/simple_stmts.html#the-exec-statement>`_ statement accepts.

::

    t = TestExec()
    exec('t.run_this()')
    



Getting that to work had me stumped for a bit. Since the documentation says `code object` I thought you would pass in the ``TestExec`` instance, but it has some kind of magic going on that allows you to import or define code and then run it using strings.

The Default Trace
-----------------

With that background out of the way we can see what the default behavior is.

::

    trace = Trace()
    try:
        trace.run('t.run_this_and_that()')
        print 'END_DEFAULT'
    except NameError:
        print NameError  
    

::

     --- modulename: Pweave, funcname: <module>
    <string>(1):   --- modulename: trace, funcname: _unsettrace
    trace.py(80):         sys.settrace(None)
    <type 'exceptions.NameError'>
    



Okay, it turns out that Pweave raises a NameError if you run a trace inside of it so I have to add it afterwards, but if you run the tangled python code the trace will dump to stdout:

.. literalinclude:: defaults.txt

