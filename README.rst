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

However, bootstrap requires a newer version of jquery than deform ships
with by default. This in turn would require a newer version of jquery.form
(> 2.43) which unfortunately is backward incompatible in its ajax handling.
Thus, deform_bootstrap cannot currently support deform's ``use_ajax`` feature.
The corresponding selenium tests have therefore been disabled until deform
catches up. Note, that you can still use jquery.form itself.

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

Getting rid of jQueryUI
=======================

Deform depends on ``jQueryUI`` for these wigdgets:

 - AutocompleteInputWidget
 - DateInputWidget
 - DateTimeInputWidget

If you don't use any of these, you can skip the remainder of this section
and just delete ``jQueryUI`` from your CSS and JS imports.  Otherwise you'll
need to add ``bootstrap-typeahead.js`` and/or ``bootstrap-datepicker.js``
to your JS includes.

You can then use deform_bootstrap's TypeaheadInputWidget as a drop in
replacement for deform's AutocompleteInputWidget.

Unfortunately things are a litte more complicated for DateInputWidget and
DateTimeInputWidget, because ``bootstrap`` does not provide native widgets
for that usecases (yet?).  Therefore you will need to either use
``deform_bootstrap.css`` provided by ``deform_bootstrap`` or build your own
``bootstrap.css`` using `LESS <http://lesscss.org/>`.  Once you have ``lessc``
installed it can be done like this::

 $ cd deform_bootstrap/static
 $ lessc deform_bootstrap.less

You'll then find your custom ``deform_bootstrap.css`` which immediately leads
to a shiny new look for DateInputWidgets.  For DateTimeInputWidgets you'll
have to replace your existing imports.  This is as easy as replacing
``from deform.widget import DateTimeInputWidget`` with
``from deform_bootstrap.widget import DateTimeInputWidget`` in your code.

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
