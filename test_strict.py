# pylint: disable=attribute-defined-outside-init, no-self-use, too-few-public-methods

import unittest

from pystrict import strict, StrictError

class TestStrict(unittest.TestCase):
    def test_frozen(self):
        @strict
        class Foo:
            cdef: int = 1
            idef: int

            def __init__(self):
                self.idef = 2

        with self.assertRaises(StrictError):
            x = Foo()
            x.bad = 1

        x = Foo()
        x.cdef = 2
        x.idef = 3

    def test_frozen_inherit(self):
        @strict
        class Foo:
            cdef: int = 1
            idef: int

            def __init__(self):
                self.idef = 2

        @strict
        class Bar(Foo):
            def __init__(self):
                self.bdef = 2
                super().__init__()
                self.edef = 2

        with self.assertRaises(StrictError):
            x = Foo()
            x.bad = 1

        x = Foo()
        x.cdef = 2
        x.idef = 3
        
        y = Bar()
        y.cdef = 2
        y.idef = 3
        y.bdef = 4
        y.edef = 4


    def test_untagged_inherit(self):
        @strict
        class Foo:
            cdef: int = 1
            idef: int

            def __init__(self):
                self.idef = 2

        class Bar(Foo):
            def __init__(self):
                self.bdef = 2
                super().__init__()
                self.edef = 2

        # parent still strict
        with self.assertRaises(StrictError):
            x = Foo()
            x.bad = 1

        # child not tagged strict... so ... not strict at all
        y = Bar()
        y.whatever = 9

    def test_init_typing(self):
        with self.assertRaises(StrictError):
            @strict
            class Foo:
                def __init__(self, z):
                    pass
            Foo(1)

    def test_strict_function(self):
        with self.assertRaises(StrictError):
            @strict
            def plusone(x) -> int:
                return x + 1
            plusone(2)

        with self.assertRaises(StrictError):
            @strict
            def plusone2(x: int):
                return x + 1
            plusone2(2)


        @strict
        def bop(x: int) -> int:
            return x + 1

        bop(1)
