# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Demo URL Patterns
==========================

Defines URL patterns for the demo project. This includes:

- Admin panel routes for managing the application.
- Routes for the `swing_hello` app, including a default route.

"""


# =============================================================================
# Imports
# =============================================================================

from django.contrib import admin
from django.urls import include, path

# Import | Local Modules


# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin site URL
    path("", include("swing.status.urls")),
]
