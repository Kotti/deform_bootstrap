import datetime
import colander
import deform

from colander import iso8601
from deform import ZPTRendererFactory
from deform.i18n import _
from pkg_resources import resource_filename
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request
from pyramid.view import view_config
from deformdemo import demonstrate, DeformDemo

from deform_bootstrap import includeme as base_includeme
from deform_bootstrap.widget import TypeaheadInputWidget
from deform_bootstrap.widget import DateTimeInputWidget
from deform_bootstrap.widget import ChosenSingleWidget, ChosenMultipleWidget

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

    @view_config(renderer='deformdemo:templates/form.pt', name='datetime_input')
    @demonstrate('DateTime Input Widget')
    def datetime_input(self):
        class Schema(colander.Schema):
            date_time = colander.SchemaNode(
                colander.DateTime(),
                validator=colander.Range(
                    min=datetime.datetime(
                        2010, 5, 5, 12, 30, tzinfo=iso8601.Utc()),
                    min_err=_('${val} is earlier than earliest datetime ${min}')),
                widget=DateTimeInputWidget()
                )
        schema = Schema()
        form = deform.Form(schema, buttons=('submit',))
        when = datetime.datetime(2010, 5, 6, 12)
        return self.render_form(form, appstruct={'date_time': when})

    @view_config(renderer='deformdemo:templates/form.pt', name='chosen_single')
    @demonstrate('Chosen Widget (Single Select)')
    def chosen_single(self):
        choices = (
            ('', ''),
            ('AT', 'Austria'), ('BE', 'Belgium'), ('BG', 'Bulgaria'),
            ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'),
            ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'),
            ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'),
            ('IE', 'Ireland'), ('IT', 'Italy'), ('LV', 'Latvia'),
            ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'),
            ('NL', 'Netherlands'), ('PL', 'Poland'), ('PT', 'Portugal'),
            ('RO', 'Romania'), ('SK', 'Slovakia'), ('SI', 'Slovenia'),
            ('ES', 'Spain'), ('SE', 'Sweden'), ('UK', 'United Kingdom'),
            )
        class Schema(colander.Schema):
            country = colander.SchemaNode(
                colander.String(),
                widget=ChosenSingleWidget(values=choices,
                                          placeholder=u'Select a country'),
                missing=colander.required,
                )
        schema = Schema()
        form = deform.Form(schema, buttons=('submit',))
        return self.render_form(form)

    @view_config(renderer='deformdemo:templates/form.pt', name='chosen_multiple')
    @demonstrate('Chosen Widget (Multiple Select)')
    def chosen_multiple(self):
        choices = (
            ('', ''),
            ('AT', 'Austria'), ('BE', 'Belgium'), ('BG', 'Bulgaria'),
            ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'),
            ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'),
            ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'),
            ('IE', 'Ireland'), ('IT', 'Italy'), ('LV', 'Latvia'),
            ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'),
            ('NL', 'Netherlands'), ('PL', 'Poland'), ('PT', 'Portugal'),
            ('RO', 'Romania'), ('SK', 'Slovakia'), ('SI', 'Slovenia'),
            ('ES', 'Spain'), ('SE', 'Sweden'), ('UK', 'United Kingdom'),
            )
        class Schema(colander.Schema):
            countries = colander.SchemaNode(
                deform.Set(allow_empty=True),
                widget=ChosenMultipleWidget(values=choices,
                                            placeholder=u'Select countries'),
                missing=colander.null,
                )
        schema = Schema()
        form = deform.Form(schema, buttons=('submit',))
        return self.render_form(form)

    @view_config(renderer='deformdemo:templates/form.pt',
                 name='inline_radiochoice')
    @demonstrate('Inline RadioChoice Widget')
    def inline_radiochoice(self):
        class Schema(colander.Schema):
            choice = colander.SchemaNode(
                colander.String(),
                widget=deform.widget.RadioChoiceWidget(
                    values=[('a', 'Arrow'),
                            ('b', 'Brick'),
                            ('c', 'Cardamom')],
                    inline=True),
                description='Pick one')
        schema = Schema()
        form = deform.Form(schema, buttons=('submit',))
        return self.render_form(form)

    @view_config(renderer='deformdemo:templates/form.pt',
                 name='inline_checkboxchoice')
    @demonstrate('Inline CheckboxChoice Widget')
    def inline_checkboxchoice(self):
        class Schema(colander.Schema):
            choice = colander.SchemaNode(
                deform.schema.Set(),
                widget=deform.widget.CheckboxChoiceWidget(
                    values=[('a', 'Awesome'),
                            ('b', 'Bogus'),
                            ('c', 'Crud')],
                    inline=True),
                description='Pick as many as apply')
        schema = Schema()
        form = deform.Form(schema, buttons=('submit',))
        return self.render_form(form)
