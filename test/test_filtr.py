import operator as op
import string
import unittest

from filtr import Filtration


class TestFiltration(unittest.TestCase):

    def setUp(self):
        self.seq = tuple(range(10))

    def test_construct(self):
        f1 = Filtration(self.seq, range(1, 10**2, 3))
        self.assertEqual(
            tuple(range(1, len(self.seq), 3)),
            f1(),
        )
        f3 = Filtration(self.seq)
        self.assertEqual(self.seq, f3())
        with self.assertRaises(TypeError):
            Filtration()

    def test__eq__(self):
        f1 = Filtration(self.seq, range(1, 10**2, 3))
        f2 = Filtration(self.seq, range(1, 10**2, 3))

        self.assertEqual(f1, f2)
        self.assertEqual(f1(), f2())

        f3 = Filtration(self.seq)
        for f in (f1, f2):
            self.assertNotEqual(f3, f)
            self.assertNotEqual(f3(), f())

    def test__iter__(self):
        f1 = Filtration(self.seq, range(1, 10**2, 3))
        for v, s in zip(f1, range(1, 10**2, 3)):
            self.assertEqual(v, s)
        self.assertEqual(list(f1), list(range(1, 10, 3)))

    def test__hash__(self):
        f1 = Filtration(self.seq, range(1, 10**2, 3))
        f2 = Filtration(self.seq)
        self.assertNotEqual(hash(f1), hash(f2))

    def test__invert__(self):
        f1 = Filtration(self.seq, range(1, 10**2, 3))
        self.assertEqual(f1, ~ (~ f1))
        f2 = Filtration(self.seq)
        self.assertEqual(f2, ~ (~ f2))
        self.assertFalse((~ f2)())

    def test__neg__(self):
        f1 = Filtration(self.seq, range(1, 10**2, 3))
        self.assertEqual(f1, - (- f1))
        f2 = Filtration(self.seq)
        self.assertEqual(f2, - (- f2))
        self.assertFalse((- f2)())

    def test_is_disjoint(self):
        f1 = Filtration(self.seq, range(1, 10**2, 3))
        f2 = Filtration(self.seq, range(2, 10**2, 3))
        self.assertTrue(f1.isdisjoint(f2))

    def test__bool__(self):
        f0 = Filtration(self.seq)
        self.assertTrue(f0)
        self.assertFalse(- f0)
        f1 = Filtration(self.seq, (4, 5, 8))
        self.assertTrue(f0)
        self.assertTrue(f1)

    def test__getitem__(self):
        f0 = Filtration(self.seq)
        for i in range(len(f0)):
            self.assertEqual(i, f0[i])
        f1 = Filtration(string.ascii_letters, (1, 3, 5))
        self.assertEqual(
            'b',
            f1[0],
        )
        self.assertEqual(
            'd',
            f1[1],
        )
        self.assertEqual(
            'f',
            f1[2],
        )
        with self.assertRaises(IndexError):
            f1[3]
        self.assertEqual(len(f1), 3)

    def test__len__(self):
        f0 = Filtration(self.seq)
        f_ = - f0
        f1 = Filtration(self.seq, (1, 2, 3))
        self.assertEqual(len(f0), len(self.seq))
        self.assertEqual(len(f_), 0)
        self.assertEqual(len(f1), 3)

    def test__sub__(self):
        f1 = Filtration(self.seq, (1, 2, 3))
        f2 = Filtration(self.seq, (2, 3, 7))
        f3 = f1 - f2
        f4 = f2 - f1
        f5 = (- Filtration(self.seq)) - f3
        for f in (f1, f2, f4):
            self.assertNotEqual(id(f3), id(f))
        for f in (f1, f2, f4):
            self.assertNotEqual(f3, f)
        self.assertEqual(f3, Filtration(self.seq, (1,)))
        self.assertEqual(f3(), (1,))
        self.assertEqual(f4, Filtration(self.seq, (7,)))
        self.assertEqual(f4(), (7,))
        self.assertFalse(f5)

        self.assertEqual(
            Filtration.__sub__.__doc__,
            op.__sub__.__doc__,
        )

    def test__and__(self):
        f1 = Filtration(self.seq, (1, 2, 3))
        f2 = Filtration(self.seq, (2, 3, 7))
        f3 = f1 & f2
        f4 = f2 & f1
        for f in (f1, f2, f4):
            self.assertNotEqual(id(f3), id(f))
        for f in (f1, f2):
            self.assertNotEqual(f3, f)
        self.assertEqual(f3, f4)
        self.assertEqual(f3(), f4())
        self.assertEqual(f3(), (2, 3))
        self.assertEqual(
            f3,
            Filtration(self.seq, (2, 3,))
        )

        self.assertEqual(
            Filtration.__and__.__doc__,
            op.__and__.__doc__,
        )

    def test__or__(self):
        f1 = Filtration(self.seq, (1, 2, 3))
        f2 = Filtration(self.seq, (2, 3, 7))
        f3 = f1 | f2
        f4 = f2 | f1
        for f in (f1, f2, f4):
            self.assertNotEqual(id(f3), id(f))
        for f in (f1, f2):
            self.assertNotEqual(f3, f)
        self.assertEqual(f3, f4)
        self.assertEqual(f3(), f4())
        tup = (1, 2, 3, 7)
        self.assertEqual(f3(), tup)
        self.assertEqual(
            f3,
            Filtration(self.seq, tup)
        )

        self.assertEqual(
            Filtration.__or__.__doc__,
            op.__or__.__doc__,
        )

    def test__repr__(self):
        f1 = Filtration(tuple(range(5)), (1, 2, 3))
        self.assertEqual(
            "Filtration(seq=(0, 1, 2, 3, 4), filter=(1, 2, 3))",
            repr(f1),
        )

    def test__str__(self):
        f1 = Filtration(tuple(range(5)), (1, 2, 3))
        self.assertEqual(
            "Filtration(seq=(0, 1, 2, 3, 4), filter=(1, 2, 3))",
            str(f1),
        )

    def test__reversed__(self):
        f1 = Filtration(string.ascii_letters, (1, 3, 5))
        self.assertEqual(['f', 'd', 'b'], list(reversed(f1)))

    def test__contains__(self):
        f1 = Filtration(['a', 'b', 'c', 'd', 'e'], (0, 2, 3))
        self.assertTrue('a' in f1)
        self.assertFalse('b' in f1)
        self.assertTrue('c' in f1)
        self.assertTrue('d' in f1)
        self.assertFalse('e' in f1)
        self.assertFalse(1110 in f1)
