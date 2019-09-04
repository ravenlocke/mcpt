from collections import namedtuple as _nt

_GT = {"g", "gt", ">", "greater"}
_LT = {"l", "lt", "<", "lower"}
_BOTH = {"both"}
_RESULT = _nt("Result", ["lower", "upper", "confidence"])

from mcpt.permutation_test import permutation_test
from mcpt.correlation_permutation_test import correlation_permutation_test
