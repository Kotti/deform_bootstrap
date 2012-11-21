import json
from colander import null, Invalid
from deform.i18n import _
from deform.widget import AutocompleteInputWidget
from deform.widget import DateTimeInputWidget as DateTimeInputWidgetBase
from deform.widget import SelectWidget
from deform.widget import Widget
from deform.widget import _normalize_choices
import warnings


class TypeaheadInputWidget(AutocompleteInputWidget):
    """
    Renders an ``<input type="text"/>`` widget which provides
    autocompletion via a list of values using bootstrap's typeahead plugin
    http://twitter.github.com/bootstrap/javascript.html#typeahead.

    **Attributes/Arguments**

    size
        The size, in columns, of the text input field.  Defaults to
        ``None``, meaning that the ``size`` is not included in the
        widget output (uses browser default size).

    template
        The template name used to render the widget.  Default:
        ``typeahead_textinput``.

    readonly_template
        The template name used to render the widget in read-only mode.
        Default: ``readonly/typeahead_textinput``.

    strip
        If true, during deserialization, strip the value of leading
        and trailing whitespace (default ``True``).

    values
        A list of strings or string.
        Defaults to ``[]``.

        If ``values`` is a string it will be treated as a
        URL. If values is an iterable which can be serialized to a
        :term:`json` array, it will be treated as local data.

        If a string is provided to a URL, an :term:`xhr` request will
        be sent to the URL. The response should be a JSON
        serialization of a list of values.  For example:

          ['foo', 'bar', 'baz']

    min_length
        ``min_length`` is an optional argument to
        :term:`jquery.ui.autocomplete`. The number of characters to
        wait for before activating the autocomplete call.  Defaults to
        ``1``.

    style
        A string that will be placed literally in a ``style`` attribute on
        the text input tag.  For example, 'width:150px;'.  Default: ``None``,
        meaning no style attribute will be added to the input tag.

    items
        The max number of items to display in the dropdown. Defaults to
        ``8``.

    """
    template = 'typeahead_input'
    values = []
    requirements = (('bootstrap', None), )

    def serialize(self, field, cstruct, **kw):
        if cstruct in (null, None):
            cstruct = ''
        readonly = kw.get('readonly', self.readonly)
        if 'source' in self.__dict__:
            warnings.warn('"Source" argument is now deprecated, use "values" instead',
                category=DeprecationWarning)
            self.values = self.source
        if isinstance(self.values, basestring):
            url = self.values
            source = (
                'function (query, process){$.getJSON("%s", {"term": query}, process);}'
                % (url))
        else:
            source = json.dumps(self.values)
        options = {}
        if 'min_length' in self.__dict__ or 'min_length' in kw:
            options['minLength'] = kw.pop('min_length', self.min_length)
        if 'items' in self.__dict__ or 'items' in kw:
            options['items'] =  kw.pop('items', self.items)
        options = json.dumps(options)[1:-1]
        kw['options'] = ', '+options if options else options
        kw['values'] = source
        tmpl_values = self.get_template_values(field, cstruct, kw)
        template = readonly and self.readonly_template or self.template
        return field.renderer(template, **tmpl_values)


class DateTimeInputWidget(DateTimeInputWidgetBase):

    template = 'splitted_datetimeinput'
    readonly_template = 'readonly/textinput'
    requirements = ()

    def serialize(self, field, cstruct, readonly=False):
        if cstruct is null or not cstruct:
            _date = ''
            _time = ''
        else:
            if len(cstruct) == 25:  # strip timezone if it's there
                cstruct = cstruct[:-6]
            try:
                _date, _time = cstruct.split('T')
            except ValueError:
                _date, _time = cstruct.split(' ')
        template = readonly and self.readonly_template or self.template
        return field.renderer(template, field=field, cstruct=cstruct,
                              date=_date, time=_time)

    def deserialize(self, field, pstruct):
        if pstruct is null:
            return null
        else:
            _date = pstruct['date'].strip()
            _time = pstruct['time'].strip()

            if (not _date and not _time):
                return null

            if not _date:
                raise Invalid(field.schema, _('Incomplete date'), "")

            if not _time:
                _time = "00:00:00"

            result = ' '.join([_date, _time])

            return result


class ChosenSingleWidget(SelectWidget):
    template = 'chosen_single'
    requirements = (('chosen', None), )


class ChosenOptGroupWidget(SelectWidget):
    template = 'chosen_optgroup'
    requirements = (('chosen', None), )


class ChosenMultipleWidget(Widget):
    template = 'chosen_multiple'
    values = ()
    size = 1
    requirements = (('chosen', None), )

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (null, None):
            cstruct = ()
        template = readonly and self.readonly_template or self.template
        return field.renderer(template, field=field, cstruct=cstruct,
                              values=_normalize_choices(self.values))

    def deserialize(self, field, pstruct):
        if pstruct is null:
            return null
        if isinstance(pstruct, basestring):
            return (pstruct,)
        return tuple(pstruct)
