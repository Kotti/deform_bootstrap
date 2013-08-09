import json
import unittest

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
            ('function (query, process){'
             '$.getJSON("/items", {"term": query}, process);}'))
        self.assertEqual(
            json.loads('{' + renderer.kw['options'][1:] + '}'),
            {'minLength': 2, 'items': 5}
            )

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


class TestDateTimeInputWidget(unittest.TestCase):

    def _makeOne(self, **kw):
        from deform_bootstrap.widget import DateTimeInputWidget
        return DateTimeInputWidget(**kw)

    def test_serialize_null(self):
        from colander import null
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        widget.serialize(field, null)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['date'], '')
        self.assertEqual(renderer.kw['time'], '')

    def test_serialize_None(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        widget.serialize(field, None)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['date'], '')
        self.assertEqual(renderer.kw['time'], '')

    def test_serialize_w_tz(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        widget.serialize(field, '2013-05-03T09:28:37-04:00')
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['date'], '2013-05-03')
        self.assertEqual(renderer.kw['time'], '09:28:37')

    def test_serialize_wo_tz(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        widget.serialize(field, '2013-05-03T09:28:37')
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['date'], '2013-05-03')
        self.assertEqual(renderer.kw['time'], '09:28:37')

    def test_serialize_w_space(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        widget.serialize(field, '2013-05-03 09:28:37')
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['date'], '2013-05-03')
        self.assertEqual(renderer.kw['time'], '09:28:37')

    def test_serialize_not_null_readonly(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        widget.serialize(field, '2013-05-03 09:28:37', readonly=True)
        self.assertEqual(renderer.template, widget.readonly_template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['date'], '2013-05-03')
        self.assertEqual(renderer.kw['time'], '09:28:37')

    def test_deserialize_null(self):
        from colander import null
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        self.assertTrue(widget.deserialize(field, null) is null)

    def test_deserialize_empty_date_and_time(self):
        from colander import null
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        pstruct = {'date': '', 'time': ''}
        self.assertTrue(widget.deserialize(field, pstruct) is null)

    def test_deserialize_empty_date(self):
        from colander import Invalid
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        pstruct = {'date': '', 'time': '09:28:37'}
        self.assertRaises(Invalid, widget.deserialize, field, pstruct)

    def test_deserialize_empty_time(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        pstruct = {'date': '2013-05-03', 'time': ''}
        cstruct = widget.deserialize(field, pstruct)
        self.assertEqual(cstruct, '2013-05-03 00:00:00')

    def test_deserialize_w_time_no_seconds(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        pstruct = {'date': '2013-05-03', 'time': '09:28'}
        cstruct = widget.deserialize(field, pstruct)
        self.assertEqual(cstruct, '2013-05-03 09:28:00')


class TestChosenOptGroupWidget(unittest.TestCase):

    def _makeOne(self, **kw):
        from deform_bootstrap.widget import ChosenOptGroupWidget
        return ChosenOptGroupWidget(**kw)

    def test_serialize_null(self):
        from colander import null
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        widget.serialize(field, null)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], '')

    def test_serialize_None(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        widget.serialize(field, None)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], '')

    def test_serialize_not_null(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        widget.values = [{'label': 'alphabet',
                          'values': [('abc', 'ABC'), ('def', 'DEF')],
                         }]
        widget.serialize(field, 'abc')
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], 'abc')


class TestChosenMultipleWidget(unittest.TestCase):

    def _makeOne(self, **kw):
        from deform_bootstrap.widget import ChosenMultipleWidget
        return ChosenMultipleWidget(**kw)

    def test_serialize_null(self):
        from colander import null
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        widget.serialize(field, null)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], ())

    def test_serialize_None(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        widget.serialize(field, None)
        self.assertEqual(renderer.template, widget.template)
        self.assertEqual(renderer.kw['field'], field)
        self.assertEqual(renderer.kw['cstruct'], ())

    def test_deserialize_null(self):
        from colander import null
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        self.assertTrue(widget.deserialize(field, null) is null)

    def test_deserialize_text(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        self.assertEqual(widget.deserialize(field, 'abc'), ('abc',))

    def test_deserialize_list(self):
        widget = self._makeOne()
        renderer = DummyRenderer()
        schema = DummySchema()
        field = DummyField(schema, renderer=renderer)
        self.assertEqual(widget.deserialize(field, ['abc', 'def']),
                         ('abc', 'def'))
