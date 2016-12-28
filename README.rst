smartypants
===========

smartypants_ is a Python fork of SmartyPants__.

.. _smartypants: https://bitbucket.org/livibetter/smartypants.py
__ SmartyPantsPerl_
.. _SmartyPantsPerl: http://daringfireball.net/projects/smartypants/

.. important::

   As of 2016-12-28, smartypants is looking for new maintainer to take over,
   please contact project owner on Bitbucket.


Installation
------------

To install it:

.. code:: sh

  pip install smartypants


Quick usage
-----------

To use it as a module:

.. code:: python

  import smartypants

  text = '"SmartyPants" is smart, so is <code>smartypants</code> -- a Python port'
  print(smartypants.smartypants(text))

To use the command-line script ``smartypants``:

.. code:: sh

  echo '"SmartyPants" is smart, so is <code>smartypants</code> -- a Python port' | smartypants

Both produce::

  &#8220;SmartyPants&#8221; is smart, so is <code>smartypants</code> &#8212; a Python port


More information
----------------

* Documentation_
* `Source code`_
* PyPI_

.. _documentation: http://pythonhosted.org/smartypants/
.. _Source code: smartypants_
.. _PyPI: https://pypi.python.org/pypi/smartypants/
