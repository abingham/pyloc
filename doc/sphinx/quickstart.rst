==========
Quickstart
==========

Basic Output
============

By default, pyloc walks through each directory tree you specify,
counts the lines of each file it recognizes, and generates a table
listing the counts indexed by *category* (the type of a line: code,
comment, etc.) and *file-type* (the type of a file: python, c++,
etc.). So, the command::

  pyloc foo/src bar/src

would walk the directory structures under ``foo/src`` and ``bar/src`` and
generate a table something like this::

    type code comment total docstring empty
  ------ ---- ------- ----- --------- -----
  Python  381      77   573        72   103 
     C++    6       3    11               2 
  ------ ---- ------- ----- --------- -----
     SUM  387      80   584        72   105 

Raw Data
========

While this is a useful view of the line counts, you might want a
lower-level version of the LOC data. By default, pyloc accumulates its data
in a temporary, in-memory sqlite database. If you would rather have
access to that data for other purposes, you can ask pyloc to save that
database to a file with the ``-d`` or ``--dbname`` argument::

  pyloc --dbname=test.db foo/src bar/src

In this case, pyloc would store the raw LOC data in a database named
test.db (see :ref:`db-format-document` for a description of the
database.)

.. topic:: A Note of Caution

  The ``-d, --dbname`` arguments both *load* and *save* the specified
  database. Any data present in the database when you run pyloc (if it
  exists) is preserved, and pyloc will simply add to the stored
  data. This means that you can run pyloc multiple times with the same
  ``--dbname`` over different directories and accumulate the results
  into a single database. This also means that if you run pyloc multiple
  times with the same ``--dbname`` over the *same* directory, you will
  end up with duplicate counts.