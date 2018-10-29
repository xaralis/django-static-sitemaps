import os
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured

from .conf import STORAGE_CLASS, ROOT_DIR


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


def get_storage(site):
    storage = _lazy_load(STORAGE_CLASS)()
    if STORAGE_CLASS == 'django.core.files.storage.FileSystemStorage':
        try:
            storage = _lazy_load(STORAGE_CLASS)(
                location=os.path.join(ROOT_DIR, site.domain))
        except TypeError:
            storage = _lazy_load(STORAGE_CLASS)()
    return storage
