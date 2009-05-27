.. _format-function-document:

Format Functions
================

The Short Version
-----------------

1. Write a function of the form `def myFormatterFunc(results)`
   returning a string

2. Pass the name of that function to the `-f` argument of pyloc::

     pyloc -f my_module.myFormatterFunc

3. If your function takes other arguments after the results object,
   set them with the -a argument. Given the function::

     def fancy_formatter(results, title):
      . . .

   you could set the title argument as follows::

     pyloc -f my_module.fancy_formatter -a "\"My Title\""

4. pyloc will pass the results object (of type pyloc.db.Results) to
   your function and will use the return value of your function as its
   output.

The Long Version
----------------

The pyloc formatter system allows you to write arbitrarily complex
functions for producing pyloc's output. There are several formatting
functions built into pyloc, but it is easy to use externally defined
python functions as well.

In general, you select which formatting function to use with the `-f`
parameter. The value of this parameter should be the fully-qualified
name of a python function. The default value for this parameter is
`pyloc.format.by_language`, so this::

  pyloc project/src

is equivalent to::

  pyloc -f pyloc.format.by_language project/src

To generate output, pyloc first scans all of the requested source and
builds a database of information. Once this database is complete,
pyloc passes a connection to this database into the specified
formatter function.

How to make a formatter
-----------------------

Formatting functions are simple to write. The only requirements are
that:

 - Their first parameter must be the database connection
 - The must return a string holding their formatted output

Formatters can take an arbitrary number of parameters after the connection.

See :ref:`db-format-document` for information on how to get data out
of the Results object.

Passing parameters to a formatter
---------------------------------

To pass extra parameters to a formatter function, use the `-a`
argument. The value you provide for `-a` will be pasted directly into
the function call string used to invoke your formatter. In code terms,
something like this is happening::

  exec('output = %s(rslt, %s)' % (value_of_dash_f_argument,
                                  value_of_dash_a_argument)')

So, the command::

  pyloc -f my_mod.my_func -a "\"a string\", 42" proj/src

would result in the following function call (assuming your shell is
vaguely bash-like)::

  output = my_mod.my_func(rslt, "a string", 42)

Clearly, this is a pretty low-powered way to pass arguments to a
function, but it works well for simple cases. If you need to pass in
more complex configuation info, you might consider using a config file
and simply passing that file's name with `-a`.
