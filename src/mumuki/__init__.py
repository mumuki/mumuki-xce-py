from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

try:
    dist_name = "mumuki_xce"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from mumuki.standard import Mumuki
from mumuki.interactive import IMumuki