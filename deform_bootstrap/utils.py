#!/usr/bin/env python
# -*- coding: utf-8 -*-


def tabifyForm(form):
    """
        A function that returns data from the form in a nice way ready for
        tabbed view.
    """
    children = []
    mappings = []

    for i in form.children:
        if i.children:
            mappings.append({'title': i.title,
                             'name': i.name,
                             'children': i,
                             })
        else:
            children.append(i)

    return {
        'default': children,
        'other': mappings,
        'only_one': mappings == [],
        'have_default': len(children) > 1
    }
