from pkg_resources import resource_filename

from deform import Form


def add_search_path():
    loader = Form.default_renderer.loader
    loader.search_path = (
        resource_filename('deform_bootstrap', 'templates'),
        ) + loader.search_path


def includeme(config):
    add_search_path()
    config.add_static_view('static-deform_bootstrap', 'deform_bootstrap:static')
