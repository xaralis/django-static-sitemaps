from importlib import import_module

from django.core.exceptions import ImproperlyConfigured


def _lazy_load(class_path):
    module, attr = class_path.rsplit('.', 1)
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                   (module, e))
    try:
        instance = getattr(mod, attr)
        return instance
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                   'class.' % (module, attr))
