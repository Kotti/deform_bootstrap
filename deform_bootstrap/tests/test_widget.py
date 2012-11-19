import unittest
from StringIO import StringIO

from deform.tests.test_widget import DummyField, DummyRenderer, DummySchema


class TestTypeaheadInputWidget(unittest.TestCase):
    def _makeOne(self, **kw):
        from deform_bootstrap.widget import TypeaheadInputWidget
        return TypeaheadInputWidget(**kw)

    def test_serialize_null(self):
        from colander import null
        widget = self._makeOne()
        renderer = DummyRenderer()
        field = DummyField(None, renderer=renderer)
        widget.serialize(field, null)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], '')

    def test_serialize_None(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        field = DummyField(None, renderer=renderer)
        widget.serialize(field, None)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], '')

    def test_serialize_iterable(self):
        import json
        widget = self._makeOne()
        values = [1, 2, 3, 4]
        widget.values = values
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        cstruct = 'abc'
        widget.serialize(field, cstruct)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], cstruct)
        renderer_options = json.loads('{"source": '+renderer.kw['values']
                                      +renderer.kw['options']+'}')
        self.assertEqual(renderer_options['source'], values)

    def test_serialize_remote(self):
        import json
        widget = self._makeOne(min_length=2, items=5)
        values = '/items'
        widget.source = values
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        cstruct = 'abc'
        widget.serialize(field, cstruct)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], cstruct)
        self.assertEqual(renderer.kw['values'],
            'function (query, process){$.getJSON("/items", {"term": query}, process);}')
        self.assertEqual(renderer.kw['options'],', "minLength": 2, "items": 5')

    def test_serialize_not_null_readonly(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        cstruct = 'abc'
        widget.serialize(field, cstruct, readonly=True)
        self.assertEqual(renderer.template, widget.readonly_template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], cstruct)
