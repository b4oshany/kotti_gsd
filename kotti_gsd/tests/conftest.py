# -*- coding: utf-8 -*-

"""
Created on 2017-05-11
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

pytest_plugins = "kotti"

from pytest import fixture


@fixture(scope='session')
def custom_settings():
    import kotti_gsd.resources
    kotti_gsd.resources  # make pyflakes happy
    return {
        'kotti.configurators': 'kotti_tinymce.kotti_configure '
                               'kotti_gsd.kotti_configure'}
