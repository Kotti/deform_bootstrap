================
deform_bootstrap
================

``deform_bootstrap`` provides `Bootstrap
<http://twitter.github.com/bootstrap/>`_ compatible templates for the
`deform form library <http://pypi.python.org/pypi/deform/0.9.3>`_.

Currently, it only overrides a handful of templates to make deform
forms look OK with bootstrap.  Eventually, this package might grow to
contain widgets for Bootstrap.

How to use it
=============

In your Paste Deploy configuration file (e.g. ``development.ini``) add
``deform_bootstrap`` to the list of ``pyramid_includes``, or add a
this line if a ``pyramid.includes`` setting does not exist::

  [app:main]
  ...
  pyramid.includes = deform_bootstrap

This will put the templates in ``deform_bootstrap/templates`` into the
`deform search path
<http://docs.pylonsproject.org/projects/deform/en/latest/templates.html>`_.

Work in progress
================

Work still needs to be done on individual widget templates.
Contributions the in form of markup changes and style corrections are
most welcome.

``deform_bootstrap`` passes 100% of the `deformdemo
<http://deformdemo.repoze.org/>`_ tests.  Please do run the Selenium
tests before submitting a patch.

If you want to quickly try out ``deform_bootstrap`` and see how it
looks in practice you can run these commands, assuming that you have a
`virtualenv <http://pypi.python.org/pypi/virtualenv>`_ set up in your
``deform_bootstrap`` directory::

  $ git clone https://github.com/Pylons/deformdemo.git
  $ cd deformdemo
  $ ../bin/python setup.py develop
  $ cd ..
  $ bin/pserve demo.ini

You should now be able to access the demo site at http://0.0.0.0:8521

Running Selenium tests
======================

Follow the instructions in ``deformdemo`` to install Selenium.  Then
install deform_bootstrap in your virtualenv and from within
the ``deform_bootstrap`` package run this command:

  $ bin/python deform_bootstrap/demo/test.py

API
===

input_prepend / input_append
----------------------------

Bootstrap has a nice feature to prepend/append text to input[type=text]
form elements (see http://twitter.github.com/bootstrap/base-css.html#forms).
To use it with ``deform_bootstrap`` you can simply pass ``input_prepend``
or ``input_append`` as keyword arguments to the widget constructor in your
``colander.Schema`` subclass::
  
  class PersonSchema(colander.Schema):
      weight = colander.SchemaNode(
          colander.Integer(),
          title=u"Weight",
          widget=deform.widget.TextInputWidget(
              input_append="kg",
              css_class="span1",
          ))
