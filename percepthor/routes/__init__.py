"""The routes of cerver authenticated by libauth: the AuthRoute, the routes of the first API,
the groups and endpoints of the routes tree, and the admin routes.
"""

from . import admin, groups, legacy, routes

from .admin import *
from .groups import *
from .legacy import *
from .routes import *

__all__ = admin.__all__ + groups.__all__ + legacy.__all__ + routes.__all__
