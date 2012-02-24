import json
from colander import null
from deform.widget import AutocompleteInputWidget


class TypeaheadInputWidget(AutocompleteInputWidget):
    """
    Renders an ``<input type="text"/>`` widget which provides
    autocompletion via a list of values using bootstrap's typeahead plugin
    http://twitter.github.com/bootstrap/javascript.html#typeahead.

    When this option is used, the :term:`bootstrap-typeahead`
    library must be loaded into the page serving the form for
    autocompletion to have any effect.

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

    source
        A list of strings.
        Defaults to ``[]``.

    items
        The max number of items to display in the dropdown. Defaults to
        ``8``.

    """
    readonly_template = 'readonly/textinput'
    size = None
    strip = True
    template = 'typeahead_input'
    source = []
    items = 8

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (null, None):
            cstruct = ''
        options = dict(
            size=self.size,
            source=self.source)
        template = readonly and self.readonly_template or self.template
        return field.renderer(template,
            cstruct=cstruct,
            field=field,
            options=json.dumps(options))
