import colander
import deform

from deform import ZPTRendererFactory
from pkg_resources import resource_filename
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request
from pyramid.view import view_config
from deformdemo import demonstrate, DeformDemo

from deform_bootstrap import includeme as base_includeme
from deform_bootstrap.widget import TypeaheadInputWidget

# Code here exists solely to allow the running of deformdemo.  Use the
# 'includeme' from the __init__.py or similar in your production code,
# not code from here:

search_path = (
        resource_filename('deform_bootstrap', 'templates'),
        resource_filename('deform', 'templates'),
        )


def translator(term):
    return get_localizer(get_current_request()).translate(term)

zpt_renderer = ZPTRendererFactory(search_path, translator=translator)


def includeme(config):
    base_includeme(config)
    config.override_asset(
        to_override='deformdemo:templates/main.pt',
        override_with='deform_bootstrap:demo/main.pt',
        )

    def onerror(*arg):
        pass
    config.scan('deform_bootstrap.demo', onerror=onerror)


class DeformBootstrapDemo(DeformDemo):

    @view_config(renderer='deformdemo:templates/form.pt', name='typeahead_input')
    @demonstrate('Typeahead Input Widget')
    def typeahead_input(self):
        class Schema(colander.Schema):
            text = colander.SchemaNode(
                colander.String(),
                validator=colander.Length(max=100),
                widget=TypeaheadInputWidget(size=60,
                    source=[u'Foo', u'Bar', u'Baz'],
                    items=4),
                description='Enter some text')
        schema = Schema()
        form = deform.Form(schema, buttons=('submit',))
        return self.render_form(form)
