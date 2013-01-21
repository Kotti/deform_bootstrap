from mock import Mock


def test_config_searchpath():
    config = Mock()
    config.add_static_view = Mock()
    from deform_bootstrap import includeme
    includeme(config)
    config.add_static_view.assert_called_once_with('static-deform_bootstrap', 'deform_bootstrap:static')

def test_config_resources():
    from deform_bootstrap import add_resources_to_registry
    add_resources_to_registry()
    from deform.widget import default_resource_registry
    assert default_resource_registry((("chosen",None),)) is not None
    assert default_resource_registry((("bootstrap", None),)) is not None


