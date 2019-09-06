__author__ = "David J. Skelton"
__copyright__ = "Copyright 2019, David J. Skelton"
__license__ = "MIT"
__version__ = "0.1.8"
__maintainer__ = "David J. Skelton"
__email__ = "d.j.skelton1@gmail.com"
__status__ = "Production"

from collections import namedtuple as _nt

_GT = {"g", "gt", ">", "greater"}
_LT = {"l", "lt", "<", "lower"}
_BOTH = {"both"}
_RESULT = _nt("Result", ["lower", "upper", "confidence"])

from mcpt.permutation_test import permutation_test
from mcpt.correlation_permutation_test import correlation_permutation_test
