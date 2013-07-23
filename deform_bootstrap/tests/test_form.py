#!/usr/bin/env python
# -*- coding: utf-8 -*-

from deform.tests.test_schema import DummySchemaNode
from deform.widget import TextAreaWidget
import unittest
import colander


class DummyForm(object):
    def __init__(self, children=[]):
        self.children = children


class DummyField(object):
    def __init__(self, title, name, children=[]):
        self.title = title
        self.name = name
        self.children = children


class TestSet(unittest.TestCase):
    def setUp(self):
        from zope.deprecation import __show__
        __show__.off()

    def tearDown(self):
        from zope.deprecation import __show__
        __show__.on()

    def _makeOne(self, **kw):
        from deform.schema import Set
        return Set(**kw)

    def test_tabifyForm_empty(self):
        from deform_bootstrap.utils import tabifyForm

        form = DummyForm()

        result = tabifyForm(form)
        expected_result = {
            'default': [],
            'other': [],
            'only_one': True,
            'have_default': False,
        }
        self.assertEqual(result, expected_result)

    def test_tabifyForm_no_mappings(self):
        from deform_bootstrap.utils import tabifyForm
        children = [
            DummyField("Title", "title"),
            DummyField("Description", "description")
        ]
        form = DummyForm(children)

        result = tabifyForm(form)
        expected_result = {
            'default': children,
            'other': [],
            'only_one': True,
            'have_default': True,
        }
        self.assertEqual(result, expected_result)

    def test_tabifyForm_mappings(self):
        from deform_bootstrap.utils import tabifyForm
        children = [
            DummyField("Title", "title"),
            DummyField("Description", "description")
        ]
        mappings = [
            DummyField("Mapping", "mapping", [
                DummyField("Name", "name"),
                DummyField("Phone number", "phone-number")
            ])
        ]

        form = DummyForm(children + mappings)

        result = tabifyForm(form)
        expected_result = {
            'default': children,
            'other': [{'title': "Mapping",
                       'name': "mapping",
                       'children': mappings[0],
                       }],
            'only_one': False,
            'have_default': True,
        }
        self.assertEqual(result, expected_result)

    def test_tabifyForm_mappings_no_default(self):
        from deform_bootstrap.utils import tabifyForm
        mappings = [
            DummyField("Mapping", "mapping", [
                DummyField("Name", "name"),
                DummyField("Phone number", "phone-number")
            ])
        ]

        form = DummyForm(mappings)

        result = tabifyForm(form)
        expected_result = {
            'default': [],
            'other': [{'title': "Mapping",
                       'name': "mapping",
                       'children': mappings[0],
                       }],
            'only_one': False,
            'have_default': False,
        }
        self.assertEqual(result, expected_result)
