#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import colander


class DummyForm(object):
    def __init__(self, children=[], typ=colander.String()):
        self.children = children
        self.typ = typ


class DummyField(object):
    def __init__(self, title, name, children=[], typ=colander.String()):
        self.title = title
        self.name = name
        self.children = children
        self.typ = typ


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

    def test_tabify_form_empty(self):
        from deform_bootstrap.utils import tabify_form

        form = DummyForm()

        result = tabify_form(form)
        expected_result = {
            'basic': [],
            'other': [],
            'only_one': True,
            'have_basic': False,
        }
        self.assertEqual(result, expected_result)

    def test_tabify_form_no_mappings(self):
        from deform_bootstrap.utils import tabify_form
        children = [
            DummyField("Title", "title"),
            DummyField("Description", "description")
        ]
        form = DummyForm(children)

        result = tabify_form(form)
        expected_result = {
            'basic': children,
            'other': [],
            'only_one': True,
            'have_basic': True,
        }
        self.assertEqual(result, expected_result)

    def test_tabify_form_mappings(self):
        from deform_bootstrap.utils import tabify_form
        children = [
            DummyField("Title", "title"),
            DummyField("Description", "description")
        ]
        mappings = [
            DummyField("Mapping", "mapping", typ=colander.Mapping(), children=[
                DummyField("Name", "name"),
                DummyField("Phone number", "phone-number")
            ])
        ]

        form = DummyForm(children + mappings)

        result = tabify_form(form)
        expected_result = {
            'basic': children,
            'other': [{'title': "Mapping",
                       'name': "mapping",
                       'children': mappings[0],
                       }],
            'only_one': False,
            'have_basic': True,
        }
        self.assertEqual(result, expected_result)

    def test_tabify_form_mappings_no_basic(self):
        from deform_bootstrap.utils import tabify_form
        mappings = [
            DummyField("Mapping", "mapping", typ=colander.Mapping(), children=[
                DummyField("Name", "name"),
                DummyField("Phone number", "phone-number")
            ])
        ]

        form = DummyForm(mappings)

        result = tabify_form(form)
        expected_result = {
            'basic': [],
            'other': [{'title': "Mapping",
                       'name': "mapping",
                       'children': mappings[0],
                       }],
            'only_one': False,
            'have_basic': False,
        }
        self.assertEqual(result, expected_result)
