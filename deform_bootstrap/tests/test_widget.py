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
        source = [1, 2, 3, 4]
        widget.source = source
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        cstruct = 'abc'
        widget.serialize(field, cstruct)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], cstruct)
        renderer_options = json.load(StringIO(renderer.kw['options']))
        self.assertEqual(renderer_options['source'],
            source)

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
