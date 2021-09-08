# -*- coding: utf-8 -*-


import importlib


def import_module(module_str):
    if module_str is None or module_str == '':
        return None
    name = module_str.split('.')[-1]
    package = '.'.join(module_str.split('.')[:-1])
    module = importlib.import_module(package)
    return getattr(module, name)