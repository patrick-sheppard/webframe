"""
A collection of assertion functions.

Each throws an AssertionError when condition is not met.
"""

class _AssertionCounter:

    count = 0
    total = 0

    @staticmethod
    def clearCount():
        _AssertionCounter.count = 0

    @staticmethod
    def getCount():
        return _AssertionCounter.count

    @staticmethod
    def getTotal():
        return _AssertionCounter.total

def _assertion(func):
    def wrapper(*args, **kwargs):
        _AssertionCounter.count += 1
        _AssertionCounter.total += 1
        func(*args, *kwargs)
    return wrapper


@_assertion
def true(condition):
    if not condition:
        raise AssertionError('Failed asserting ' + str(condition) + ' is true.')

@_assertion
def false(condition):
    if not condition:
        raise AssertionError('Failed asserting ' + str(condition) + ' is false.')

@_assertion
def equals(val1, val2):
    if val1 != val2:
        raise AssertionError(
            'Failed asserting ' + str(val1) + ' == ' + str(val2)
        )

@_assertion
def not_equals(val1, val2):
    if val1 == val2:
        raise AssertionError(
            'Failed asserting ' + str(val1) + ' != ' + str(val2)
        )

@_assertion
def contains(val, ls):
    if val not in ls:
        raise AssertionError(
            'Failed asserting that ' + str(val) + ' is in ' + str(ls)
        )

@_assertion
def is_type(_type, obj):
    if not isinstance(obj, _type):
        raise AssertionError(
            'Failed asserting that ' + str(obj) + ' is type ' + str(_type)
        )
