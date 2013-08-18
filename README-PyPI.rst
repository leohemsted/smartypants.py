smartypants.py
==============

smartypants.py_ is a Python port of SmartyPants_.

.. _smartypants.py: https://bitbucket.org/livibetter/smartypants.py
.. _SmartyPants: http://daringfireball.net/projects/smartypants/

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

  text = '"SmartyPants" is smart, so is <code>smartypants.py</code> -- a Python port'
  print(smartypants.smartypants(text))

To use the command-line script ``smartypants``:

.. code:: sh

  echo '"SmartyPants" is smart, so is <code>smartypants.py</code> -- a Python port' | smartypants

Both produce::

  &#8220;SmartyPants&#8221; is smart, so is <code>smartypants.py</code> &#8212; a Python port

More information
----------------

Please visit smartypants.py_ on Bitbucket.
