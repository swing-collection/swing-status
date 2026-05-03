"""Smoke tests for the moved swing.status package layout."""

# Import | Standard Library
from importlib import import_module


def test_package_imports() -> None:
    package = import_module("swing.status")
    urls = import_module("swing.status.urls")

    assert package.__name__ == "swing.status"
    assert hasattr(urls, "urlpatterns")
