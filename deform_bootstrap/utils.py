#!/usr/bin/env python
# -*- coding: utf-8 -*-

from colander import Mapping


def tabify_form(form):
    """
        A function that returns data from the form in a nice way ready for
        tabbed view.
    """
    children = []
    mappings = []
    for i in form.children:
        if type(i.typ) is Mapping:
            mappings.append({'title': i.title,
                             'name': i.name,
                             'children': i,
                             })
        else:
            children.append(i)

    return {
        'basic': children,
        'other': mappings,
        'only_one': mappings == [],
        'have_basic': len(children) > 1 or len(children) == 1 and children[0].name != 'csrf_token'
    }
