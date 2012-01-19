from deform import ZPTRendererFactory

from deform_bootstrap import includeme as base_includeme
from deform_bootstrap import search_path

# Code here exists solely to allow the running of deformdemo.  Use the
# 'includeme' from the __init__.py or similar in your production code,
# not code from here:

def translator(term):
    from pyramid.i18n import get_localizer
    from pyramid.threadlocal import get_current_request
    return get_localizer(get_current_request()).translate(term)

zpt_renderer = ZPTRendererFactory(search_path, translator)

def includeme(config):
    base_includeme(config)
    config.override_asset(
        to_override='deformdemo:templates/main.pt',
        override_with='deform_bootstrap:deformdemo-main.pt',
        )
