try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    # Shim for Python 3.7. Remove when support is dropped.
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)

from . import schema  # NOQA
