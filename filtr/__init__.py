""" Create a filtered view of sequences through indices. """
from functools import wraps
from typing import (
    Any,
    Generator,
    Sequence,
    Tuple,
)
import operator as op


def _binaryop_filtration(bin_op):
    @wraps(bin_op)
    def __class_op__(self, other):
        return self.__class__(
            self.seq,
            tuple(bin_op(set(self.filter), set(other.filter))),
        )
    return __class_op__


class Filtration:
    """ Create a filtered view of sequences through indices. """

    def __init__(
            self,
            seq: Sequence[Any],
            filter: Sequence[int] = None,
    ):
        """ Initialize view.

        :param seq: sequence to be filtered.
        :param filter: subsequence of indices.
        """
        self.seq = seq
        if filter is not None:
            self.filter = tuple(sorted(
                (f for f in filter if f < len(seq)),
            ))
        else:
            self.filter = tuple(range(len(self.seq)))

    def __call__(self) -> Tuple[Any, ...]:
        """ Get filtered sequence. """
        return tuple(iter(self))

    def __iter__(self) -> Generator[Any, None, None]:
        """ Iterate over filtered sequence. """
        for ind in self.filter:
            yield self.seq[ind]

    def iter_intersect(self) -> Generator[Any, None, None]:
        """  """
        return NotImplemented

    def __eq__(self, other) -> bool:
        """ Two Filtrations are equal if their sequences are
        identical and their filter sequence are equal by value.
        """
        other_seq = getattr(other, "seq", None)
        if id(self.seq) != id(other_seq):
            return False
        other_filt = getattr(other, "filter", -1)
        return self.filter.__eq__(other_filt)

    def __bool__(self) -> bool:
        """ False if the filter is empty."""
        return bool(self.filter)

    def __getitem__(self, index) -> Any:
        """ Get sequence element at filter index `index`."""
        filter_index = index
        try:
            seq_index = self.filter.__getitem__(filter_index)
        except IndexError:
            raise
        except TypeError:
            raise
        try:
            val = self.seq.__getitem__(seq_index)
        except IndexError:
            raise
        except TypeError:
            raise
        return val

    def __len__(self) -> int:
        """ Length of filter. """
        return len(self.filter)

    def __length_hint__(self) -> int:
        return self.__len__()

    def __hash__(self) -> int:
        return hash((self.seq, self.filter))

    def __neg__(self):
        """A filtration alwas satisfy
        $f | ( - f ) == Filtration(seq)$.
        """
        return (self.__class__(self.seq) - self)

    def __invert__(self):
        """ The same as a negative filtration."""
        return self.__neg__()

    def isdisjoint(self, other):
        """ Test for common elements of two filters. """
        return set(self.filter).isdisjoint(set(other.filter))

    def __repr__(self) -> str:
        return (
            self.__class__.__name__ +
            "(seq=" + repr(self.seq) +
            ", filter=" + repr(self.filter) +
            ")"
        )

    __sub__ = _binaryop_filtration(op.__sub__)
    __and__ = _binaryop_filtration(op.__and__)
    __or__ = _binaryop_filtration(op.__or__)
