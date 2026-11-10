"""pypercepthor: the Python wrapper of libauth, the authentication of the services of
Percepthor, over pycerver.

Every public name of the subpackages is importable from the package itself, like
``from percepthor import PercepthorGroup, percepthor_handle_body_input``.
"""

from . import auth, routes, validations

# the module version is shadowed by its dict version when its names are imported
from .version import __all__ as version_names
from .version import *

from .auth import *
from .routes import *
from .validations import *

__version__ = PERCEPTHOR_VERSION

__all__ = auth.__all__ + routes.__all__ + validations.__all__ + version_names + ["__version__"]
