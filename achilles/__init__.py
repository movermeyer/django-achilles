__version__ = (0, 0, 1)


def get_version(*args, **kwargs):
    return '.'.join([str(x) for x in __version__])
