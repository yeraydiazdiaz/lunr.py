# coding: utf-8
from functools import singledispatch

__str = str


@singledispatch
def _str(obj):
    print(f'>> {obj}')
    return __str(obj)


@_str.register(type(None))
def _str_none(obj):
    print(f'>> {obj}')
    return ''

str = _str

print(str(None))
print(str([]))
