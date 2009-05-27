.. _db-format-document:

===============
Database Format
===============

When you write a formatter function (:ref:`format-function-document`),
the first argument to the function is a `pyloc.db.Results`
object. The `conn` member of this object is an `sqlite3.Connection`
object, or, in other words, a open connection to a sqlite
database. This database contains all of the compiled results from
pyloc's scan of the source files.

Using the Connection is relatively simple. For example, to get a list
of all of the file types encountered in the scan::

   def my_formatter(rslt):
     cur = rslt.conn.cursor()
     cur.execute('SELECT type FROM types')
     return str([row[0] for row in cur])

For in-depth information on how to use a Connection object or sqlite
in general, refer to the python standard library documentation. 

Table Definitions
=================

There are four tables defined in the results database: types, files,
categories, and counts. 

*(While this documentation will be kept up-to-date as much as possible,
it's possible that it will get out of sync with the code. For the
definitive view of the database's structure, look in the source
code...it should be easy to spot where the tables are being created)*

`types` Table
-------------

`types` contains a row for each file type (e.g. Python, C++, etc.)::

  id: integer
    The unique ID for this file type
  type: text
    The textual name of this type

`files` Tables
--------------

`files` contains a row for each file scanned by pyloc::

  id: integer
    The unique ID for this file
  name: text
    The name of the file, including its root
  root: text
    The root directory under which this file was found
  type_id: integer (FK types.id)
    The type of the file

`categories` Tables
-------------------

`categories` contains a row for each category that was counted
(e.g. comment, code, blank, etc.)::

  id: integer
    The unique ID for this category
  category: text
    The name of this category

.. topic:: Categories across types

  Not all file types will have the same categories. There are a few
  categories that should be nearly universal, e.g. blank, comment,
  code. However, there may be categories that are only appropriate for
  a particular language (e.g. docstrings in python). And when custom
  parser support is added, there may be all manner of categories that
  formatters will see. This is important to keep in mind when
  designing format functions.
  
`counts` Table
--------------

`counts` contains a row for each each category in each file::

  id: integer
    The unique ID of this count
  cat_id: integer (FK categories.id)
    The category for this count
  file_id: integer (FK files.id)
    The file for this count
  count: integer
    The count for the given category in the specified file

