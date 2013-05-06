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
    loader.search_path = (
        resource_filename('deform_bootstrap', 'templates'),
        ) + loader.search_path


def includeme(config):
    add_search_path()
    add_resources_to_registry()
    config.add_static_view('static-deform_bootstrap', 'deform_bootstrap:static')
