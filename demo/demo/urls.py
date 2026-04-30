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

# Import | Standard Library

# Import | Libraries
from django.contrib import admin
from django.urls import path, include

# Import | Local Modules


# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin site URL
    path("status/", include("swing.status.urls")),
    path("", include("swing.status.urls")),
]
