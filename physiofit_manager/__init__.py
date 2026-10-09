from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("physiofit_manager")
except PackageNotFoundError:
    # Running from a source tree that has not been installed
    __version__ = "unknown"
