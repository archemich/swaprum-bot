import pkg_resources as pkr

__pkg__ = 'swaprum_register_bot'

try:
    __distribution__ = pkr.get_distribution(__pkg__)
    __version__ = 'v' + __distribution__.version
except pkr.DistributionNotFound:  # pragma: no cover
    # package is not installed
    __distribution__ = pkr.Distribution()
    __version__ = 'v0.0.0 (source)'
