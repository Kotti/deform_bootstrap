from pkg_resources import resource_filename

from deform import Form

deform_templates = resource_filename('deform', 'templates')
deform_bootstrap_templates = resource_filename('deform_bootstrap', 'templates')
search_path = (deform_bootstrap_templates, deform_templates)

def set_search_path(path=search_path):
    Form.set_zpt_renderer(path)

def includeme(config):
    set_search_path()
    config.add_static_view('static-deform_boostrap', 'deform_bootstrap:static')
