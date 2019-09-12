<!-- 
[![Build Status](https://travis-ci.com/earonesty/pystrict.svg?branch=master)](https://travis-ci.com/earonesty/pystrict)
-->

## strict

Python strict tag

    pip install strict


Using @strict on classes can prevent serious errors by raising an exception when an instance has a variable created outside of init.
Unfortunately, linters don't (cannot) always catch this.  I can't express how much time this has saved me recently.

Example:
    from strict import strict

    # not allowed, missing type specifier
    @strict
    def foo(x: int, y):
        ...


    # not allowed, missing type specifier in __init__
    @strict
    class Foo():
        def __init__(self, x: int, y):
            ...

    # not allowed, object modified outside of init
    @strict
    class Foo():
        def __init__(self, x: int):
            self.x = 1

    z=[Foo(1)]

    # oops...
    z[0].y = 4

