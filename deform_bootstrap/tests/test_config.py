from mock import Mock


def test_config_searchpath():
    config = Mock()
    config.add_static_view = Mock()
    from deform_bootstrap import includeme
    includeme(config)
    config.add_static_view.assert_called_once_with('static-deform_bootstrap', 'deform_bootstrap:static')
