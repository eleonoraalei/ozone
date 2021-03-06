.. EOM documentation master file, created by
   sphinx-quickstart on Wed Jan 30 16:20:06 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to EOM's documentation!
===============================

.. toctree::
   :glob:
   :maxdepth: 2

   gettingstarted
   inputs
   _source/modules


Eleonora's Ozone Model is a 1D photochemical model that solves for
the production and loss of ozone in an atmosphere.  The goal of this
model is to determine if it is possible to create an ozone layer
in exoplanetary atmospheres.  In order to accomplish this, EOM
relies on photodissociation cross sections and irradiance values
that are supplied by the user.  Currently, EOM uses a small set
of chemical equations that are necessary to produce an ozone layer
at Earth under current atmospheric (T and P) conditions.

If this is the first time using the model, start with :ref:`gettingstarted` and then be sure to review the
:ref:`inputs` prior to running the model for the first time.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. todo::

 - Time dependent irradiances
 - Realistic orbit option
 - Alternative temperature and pressure profiles
