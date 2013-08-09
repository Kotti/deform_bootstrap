# -*- coding: utf-8 -*-

from pkg_resources import resource_filename
from deform import Form
from .resources import default_resources


def add_resources_to_registry():
    """
        Register deform_bootstrap widget specific requirements to deform's
        default resource registry
    """
    registry = Form.default_resource_registry
    for rqrt, versions in default_resources.items():
        for version, resources in versions.items():
            registry.set_js_resources(rqrt, version, *resources.get('js'))
            registry.set_css_resources(rqrt, version, *resources.get('css'))


def add_search_path():
    loader = Form.default_renderer.loader
    try:
        path = resource_filename('deform_bootstrap', 'templates')
    except ImportError:
        # On Google AppEngine resource_filename() uses os.path.expanduser()
        # which uses pwd which isn't available, so we work around that mess:
        from os.path import dirname, join
        path = join(dirname(__file__), 'templates')
    loader.search_path = (path,) + loader.search_path


def includeme(config):
    add_search_path()
    add_resources_to_registry()
    config.add_static_view(
        'static-deform_bootstrap', 'deform_bootstrap:static')
