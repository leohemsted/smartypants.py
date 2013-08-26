smartypants
===========

smartypants_ is a Python port of SmartyPants__.

.. _smartypants: https://bitbucket.org/livibetter/smartypants.py
__ SmartyPantsPerl_
.. _SmartyPantsPerl: http://daringfireball.net/projects/smartypants/


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

You can read smartypants' documentation_ or visit smartypants_ on Bitbucket.

.. _documentation: http://pythonhosted.org/smartypants/
