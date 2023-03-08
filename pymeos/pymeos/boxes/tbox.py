###############################################################################
#
# This MobilityDB code is provided under The PostgreSQL License.
#
# Copyright (c) 2019-2022, Université libre de Bruxelles and MobilityDB
# contributors
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose, without fee, and without a written 
# agreement is hereby granted, provided that the above copyright notice and
# this paragraph and the following two paragraphs appear in all copies.
#
# IN NO EVENT SHALL UNIVERSITE LIBRE DE BRUXELLES BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
# LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION,
# EVEN IF UNIVERSITE LIBRE DE BRUXELLES HAS BEEN ADVISED OF THE POSSIBILITY 
# OF SUCH DAMAGE.
#
# UNIVERSITE LIBRE DE BRUXELLES SPECIFICALLY DISCLAIMS ANY WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON
# AN "AS IS" BASIS, AND UNIVERSITE LIBRE DE BRUXELLES HAS NO OBLIGATIONS TO 
# PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS. 
#
###############################################################################
from __future__ import annotations

from typing import Optional, Union, List

from pymeos_cffi import *
from spans import intrange, floatrange

from ..main import TNumber
from ..time import *


class TBox:
    """
    Class for representing numeric temporal boxes. Both numeric and temporal bounds may be inclusive or not.

    ``TBox`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TBox('TBox XT([0, 10),[2020-06-01, 2020-06-05])')

    Another possibility is to provide the ``xmin``/``xmax`` (of type str or float) and ``tmin``/``tmax`` (of type str or
    datetime) named parameters, and optionally indicate whether the bounds are inclusive or exclusive (by default,
    lower bounds are inclusive and upper bounds are exclusive):

        >>> TBox(xmin=0, xmax=10, tmin='2020-06-01', tmax='2020-06-0')
        >>> TBox(xmin=0, xmax=10, tmin='2020-06-01', tmax='2020-06-0', xmax_inc=True, tmax_inc=True)
        >>> TBox(xmin='0', xmax='10', tmin=parse('2020-06-01'), tmax=parse('2020-06-0'))

    Note that you can create a TBox with only the numerical or the temporal dimension. In these cases, it will be
    equivalent to a :class:`~pymeos.time.period.Period` (if it only has temporal dimension) or to a
    :class:`~spans.floatrange` (if it only has the numeric dimension.
    """
    __slots__ = ['_inner']

    def __init__(self, string: Optional[str] = None, *,
                 xmin: Optional[Union[str, float]] = None,
                 xmax: Optional[Union[str, float]] = None,
                 tmin: Optional[Union[str, datetime]] = None,
                 tmax: Optional[Union[str, datetime]] = None,
                 xmin_inc: bool = True,
                 xmax_inc: bool = True,
                 tmin_inc: bool = True,
                 tmax_inc: bool = True,
                 _inner=None):
        assert (_inner is not None) or (string is not None) != (
                (xmin is not None and xmax is not None) or (tmin is not None and tmax is not None)), \
            "Either string must be not None or at least a bound pair (xmin/max or tmin/max) must be not None"
        if _inner is not None:
            self._inner = _inner
        elif string is not None:
            self._inner = tbox_in(string)
        else:
            span = None
            period = None
            if xmin is not None and xmax is not None:
                span = floatspan_make(float(xmin), float(xmax), xmin_inc, xmax_inc)
            if tmin is not None and tmax is not None:
                period = Period(lower=tmin, upper=tmax, lower_inc=tmin_inc, upper_inc=tmax_inc)._inner
            self._inner = tbox_make(period, span)

    @staticmethod
    def from_hexwkb(hexwkb: str) -> TBox:
        """
        Returns a `TBox` from its WKB representation in hex-encoded ASCII.

        Args:
            hexwkb: WKB representation in hex-encoded ASCII

        Returns:
            A new :class:`TBox` instance

        MEOS Functions:
            tbox_from_hexwkb
        """
        result = tbox_from_hexwkb(hexwkb)
        return TBox(_inner=result)

    def as_hexwkb(self) -> str:
        """
        Returns the WKB representation of ``self`` in hex-encoded ASCII.

        Returns:
            A :class:`str` object with the WKB representation of ``self`` in hex-encoded ASCII.

        MEOS Functions:
            tbox_as_hexwkb
        """
        return tbox_as_hexwkb(self._inner, -1)[0]

    @staticmethod
    def from_value(value: Union[int, float, intrange, floatrange]) -> TBox:
        """
        Returns a `TBox` from a numeric value or range. The created `TBox` will only have a numerical
        dimension.

        Args:
            value: value to be canverted into a TBox

        Returns:
            A new :class:`TBox` instance

        MEOS Functions:
            int_to_tbox, float_to_tbox, span_to_tbox, intspan_make, span_to_tbox, floatspan_make
        """
        if isinstance(value, int):
            result = int_to_tbox(value)
        elif isinstance(value, float):
            result = float_to_tbox(value)
        elif isinstance(value, intrange):
            result = span_to_tbox(intspan_make(value.lower, value.upper, value.lower_inc, value.upper_inc))
        elif isinstance(value, floatrange):
            result = span_to_tbox(floatspan_make(value.lower, value.upper, value.lower_inc, value.upper_inc))
        else:
            raise TypeError(f'Operation not supported with type {value.__class__}')
        return TBox(_inner=result)

    @staticmethod
    def from_time(time: Time) -> TBox:
        """
        Returns a `TBox` from a :class:`~pymeos.time.time.Time` object. The created `TBox`
        will only have a temporal dimension.

        Args:
            time: value to be canverted into a TBox

        Returns:
            A new :class:`TBox` instance

        MEOS Functions:
            timestamp_to_tbox, timestampset_to_tbox, period_to_tbox, periodset_to_tbox
        """
        if isinstance(time, datetime):
            result = timestamp_to_tbox(datetime_to_timestamptz(time))
        elif isinstance(time, TimestampSet):
            result = timestampset_to_tbox(time)
        elif isinstance(time, Period):
            result = period_to_tbox(time)
        elif isinstance(time, PeriodSet):
            result = periodset_to_tbox(time)
        else:
            raise TypeError(f'Operation not supported with type {time.__class__}')
        return TBox(_inner=result)

    @staticmethod
    def from_value_time(value: Union[int, float, intrange, floatrange],
                        time: Union[datetime, Period]) -> TBox:
        """
        Returns a `TBox` from a numerical and a temporal object.

        Args:
            value: numerical span of the TBox
            time: temporal span of the TBox

        Returns:
            A new :class:`TBox` instance

        MEOS Functions:
        int_timestamp_to_tbox, int_period_to_tbox, float_timestamp_to_tbox, float_period_to_tbox,
        span_timestamp_to_tbox, span_period_to_tbox, intspan_make, floatspan_make
        """
        if isinstance(value, int) and isinstance(time, datetime):
            result = int_timestamp_to_tbox(value, datetime_to_timestamptz(time))
        elif isinstance(value, int) and isinstance(time, Period):
            result = int_period_to_tbox(value, time)
        elif isinstance(value, float) and isinstance(time, datetime):
            result = float_timestamp_to_tbox(value, datetime_to_timestamptz(time))
        elif isinstance(value, float) and isinstance(time, Period):
            result = float_period_to_tbox(value, time)
        elif isinstance(value, intrange) and isinstance(time, datetime):
            result = span_timestamp_to_tbox(intspan_make(value.lower, value.upper, value.lower_inc, value.upper_inc),
                                            datetime_to_timestamptz(time))
        elif isinstance(value, intrange) and isinstance(time, Period):
            result = span_period_to_tbox(intspan_make(value.lower, value.upper, value.lower_inc, value.upper_inc), time)
        elif isinstance(value, floatrange) and isinstance(time, datetime):
            result = span_timestamp_to_tbox(floatspan_make(value.lower, value.upper, value.lower_inc, value.upper_inc),
                                            datetime_to_timestamptz(time))
        elif isinstance(value, floatrange) and isinstance(time, Period):
            result = span_period_to_tbox(floatspan_make(value.lower, value.upper, value.lower_inc, value.upper_inc),
                                         time)
        else:
            raise TypeError(f'Operation not supported with types {value.__class__} and {time.__class__}')
        return TBox(_inner=result)

    @staticmethod
    def from_tnumber(temporal: TNumber) -> TBox:
        """
        Returns a `TBox` from a :class:`~pymeos.main.tnumber.TNumber` object.

        Args:
            temporal: temporal number to be canverted into a TBox

        Returns:
            A new :class:`TBox` instance

        MEOS Functions:
            tnumber_to_tbox
        """
        return TBox(_inner=tnumber_to_tbox(temporal._inner))

    def to_floatrange(self) -> floatrange:
        """
        Returns the numeric span of ``self``.

        Returns:
            A new :class:`~spans.floatrange` instance

        MEOS Functions:
            tbox_to_floatspan
        """
        return floatspan_to_floatrange(tbox_to_floatspan(self._inner))

    def to_period(self) -> Period:
        """
        Returns the temporal span of ``self``.

        Returns:
            A new :class:`~pymeos.time.period.Period` instance

        MEOS Functions:
            tbox_to_period
        """
        return Period(_inner=tbox_to_period(self._inner))

    def has_x(self) -> bool:
        """
        Returns whether ``self`` has a numeric dimension.

        Returns:
            True if ``self`` has a numeric dimension, False otherwise

        MEOS Functions:
            tbox_hasx
        """
        return tbox_hasx(self._inner)

    def has_t(self) -> bool:
        """
        Returns whether ``self`` has a temporal dimension.

        Returns:
            True if ``self`` has a temporal dimension, False otherwise

        MEOS Functions:
            tbox_hast
        """
        return tbox_hast(self._inner)

    def xmin(self) -> float:
        """
        Returns the numeric lower bound of ``self``.

        Returns:
            The numeric lower bound of the `TBox` as a :class:`float`

        MEOS Functions:
            tbox_xmin
        """
        return tbox_xmin(self._inner)

    def xmax(self) -> float:
        """
        Returns the numeric upper bound of ``self``.

        Returns:
            The numeric upper bound of the `TBox` as a :class:`float`

        MEOS Functions:
            tbox_xmax
        """
        return tbox_xmax(self._inner)

    def tmin(self):
        """
        Returns the temporal lower bound of ``self``.

        Returns:
            The temporal lower bound of the `TBox` as a :class:`~datetime.datetime`

        MEOS Functions:
            tbox_tmin
        """
        return timestamptz_to_datetime(tbox_tmin(self._inner))

    def tmax(self):
        """
        Returns the temporal upper bound of ``self``.

        Returns:
            The temporal upper bound of the `TBox` as a :class:`~datetime.datetime`

        MEOS Functions:
            tbox_tmax
        """
        return timestamptz_to_datetime(tbox_tmax(self._inner))

    def tile(self, size: float, duration: Union[timedelta, str],
             origin: float = 0.0, start: Union[datetime, str, None] = None) -> List[List[TBox]]:
        """
        Returns 2d matrix of TBoxes resulting of tiling ``self``.

        Args:
            size: size of the numeric dimension of the tiles
            duration: size of the temporal dimenstion of the tiles
            origin: origin of the numeric dimension of the tiles
            start: origin of the temporal dimension of the tiles

        Returns:
            A 2d array of :class:`TBox` instances.

        MEOS Functions:
            tbox_tile_list
        """
        dt = timedelta_to_interval(duration) if isinstance(duration, timedelta) else pg_interval_in(duration, -1)
        st = datetime_to_timestamptz(start) if isinstance(start, datetime) \
            else pg_timestamptz_in(start, -1) if isinstance(start, str) \
            else tbox_tmin(self._inner)
        tiles, rows, columns = tbox_tile_list(self._inner, size, dt, origin, st)
        return [[TBox(_inner=tiles + (c * rows + r)) for c in range(columns)] for r in range(rows)]

    def tile_flat(self, size: float, duration: Union[timedelta, str],
                  origin: float = 0.0, start: Union[datetime, str, None] = None) -> List[TBox]:
        """
        Returns an array of TBoxes resulting of tiling ``self``.

        Args:
            size: size of the numeric dimension of the tiles
            duration: size of the temporal dimenstion of the tiles
            origin: origin of the numeric dimension of the tiles
            start: origin of the temporal dimension of the tiles

        Returns:
            An array of :class:`TBox` instances.

        MEOS Functions:
            tbox_tile_list
        """
        tiles = self.tile(size, duration, origin, start)
        return [box for row in tiles for box in row]

    def expand(self, other: Union[TBox, float, timedelta]) -> TBox:
        """
        Returns the result of expanding ``self`` with the ``other``. Depending on the type of ``other``, the expansion
        will be of the numeric dimension (:class:`float`), temporal (:class:`~datetime.timedelta`) or both
        (:class:`TBox`).

        Args:
            other: object used to expand ``self``

        Returns:
            A new :class:`TBox` instance.

        MEOS Functions:
            tbox_copy, tbox_expand, tbox_expand_value, tbox_expand_time
        """
        if isinstance(other, TBox):
            result = tbox_copy(self._inner)
            tbox_expand(other._inner, result)
        elif isinstance(other, float):
            result = tbox_expand_value(self._inner, other)
        elif isinstance(other, timedelta):
            result = tbox_expand_time(self._inner, timedelta_to_interval(other))
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')
        return TBox(_inner=result)

    def shift_tscale(self, shift: Optional[timedelta] = None, duration: Optional[timedelta] = None) -> TBox:
        """
        Returns a new TBox with the temporal span shifted by `shift` and duration `duration`.

        Examples:
            >>> tbox = TBox('TBox XT([0, 10),[2020-06-01, 2020-06-05])')
            >>> tbox.shift_tscale(shift=timedelta(days=2), duration=timedelta(days=4))
            >>> 'TBOX XT([0, 10),[2020-06-03 00:00:00+02, 2020-06-07 00:00:00+02])'

        Args:
            shift: :class:`datetime.timedelta` instance to shift the start of the temporal span
            duration: :class:`datetime.timedelta` instance representing the duration of the temporal span

        Returns:
            A new :class:`TBox` instance

        MEOS Functions:
            tbox_shift_tscale
        """
        assert shift is not None or duration is not None, 'shift and duration deltas must not be both None'
        new_inner = temporal_copy(self._inner)
        tbox_shift_tscale(
            new_inner,
            timedelta_to_interval(shift) if shift else None,
            timedelta_to_interval(duration) if duration else None
        )
        return TBox(_inner=new_inner)

    def union(self, other: TBox) -> TBox:
        """
        Returns the union of `self` with `other`. Fails if the union is not contiguous.

        Args:
            other: temporal object to merge with

        Returns:
            A :class:`TBox` instance.

        MEOS Functions:
            union_tbox_tbox
        """
        return TBox(_inner=union_tbox_tbox(self._inner, other._inner))

    # TODO: Check returning None for empty intersection is the desired behaviour
    def intersection(self, other: TBox) -> Optional[TBox]:
        """
        Returns the intersection of `self` with `other`.

        Args:
            other: temporal object to merge with

        Returns:
            A :class:`TBox` instance if the instersection is not empty, `None` otherwise.

        MEOS Functions:
            intersection_tbox_tbox
        """
        result = intersection_tbox_tbox(self._inner, other._inner)
        return TBox(_inner=result) if result else None

    def is_adjacent(self, other: Union[TBox, TNumber]) -> bool:
        """
        Returns whether ``self`` is adjacent to ``other``. That is, they share only the temporal or numerical bound
        and only one of them contains it.

        Examples:
            >>> TBox('TBox XT([0, 1], [2012-01-01, 2012-01-02))').is_adjacent(TBox('TBox XT([0, 1], [2012-01-02, 2012-01-03])'))
            >>> True
            >>> TBox('TBox XT([0, 1], [2012-01-01, 2012-01-02])').is_adjacent(TBox('TBox XT([0, 1], [2012-01-02, 2012-01-03])'))
            >>> False  # Both contain bound
            >>> TBox('TBox XT([0, 1), [2012-01-01, 2012-01-02))').is_adjacent(TBox('TBox XT([1, 2], [2012-01-02, 2012-01-03])')
            >>> False  # Adjacent in both bounds

        Args:
            other: temporal object to compare with

        Returns:
            True if adjacent, False otherwise

        MEOS Functions:
            adjacent_tbox_tbox, adjacent_tbox_tnumber
        """
        if isinstance(other, TBox):
            return adjacent_tbox_tbox(self._inner, other._inner)
        elif isinstance(other, TNumber):
            return adjacent_tbox_tnumber(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def is_contained_in(self, container: Union[TBox, TNumber]) -> bool:
        """
        Returns whether ``self`` is contained in ``container``.

        Examples:
            >>> TBox('TBox XT([1, 2], [2012-01-02, 2012-01-03])').is_contained_in(TBox('TBox XT([1, 4], [2012-01-01, 2012-01-04])'))
            >>> True
            >>> TBox('TBox XT((1, 2), (2012-01-01, 2012-01-02))').is_contained_in(TBox('TBox XT([1, 4], [2012-01-01, 2012-01-02])'))
            >>> True
            >>> TBox('TBox XT([1, 2], [2012-01-01, 2012-01-02])').is_contained_in(TBox('TBox XT((1, 2), (2012-01-01, 2012-01-02))'))
            >>> False

        Args:
            container: temporal object to compare with

        Returns:
            True if contained, False otherwise

        MEOS Functions:
            contained_tbox_tbox, contained_tbox_tnumber
        """
        if isinstance(container, TBox):
            return contained_tbox_tbox(self._inner, container._inner)
        elif isinstance(container, TNumber):
            return contained_tbox_tnumber(self._inner, container._inner)
        else:
            raise TypeError(f'Operation not supported with type {container.__class__}')

    def contains(self, content: Union[TBox, TNumber]) -> bool:
        """
        Returns whether ``self`` temporally contains ``content``.

        Examples:
            >>> TBox('TBox XT([1, 4], [2012-01-01, 2012-01-04]').contains(TBox('TBox XT([2, 3], [2012-01-02, 2012-01-03]'))
            >>> True
            >>> TBox('TBox XT([1, 2], [2012-01-01, 2012-01-02]').contains(TBox('TBox XT((1, 2), (2012-01-01, 2012-01-02)'))
            >>> True
            >>> TBox('TBox XT((1, 2), (2012-01-01, 2012-01-02)').contains(TBox('TBox XT([1, 2], [2012-01-01, 2012-01-02]'))
            >>> False

        Args:
            content: temporal object to compare with

        Returns:
            True if contains, False otherwise

        MEOS Functions:
            contains_tbox_tbox, contains_tbox_tnumber
        """
        if isinstance(content, TBox):
            return contains_tbox_tbox(self._inner, content._inner)
        elif isinstance(content, TNumber):
            return contains_tbox_tnumber(self._inner, content._inner)
        else:
            raise TypeError(f'Operation not supported with type {content.__class__}')

    def overlaps(self, other: Union[TBox, TNumber]) -> bool:
        """
        Returns whether ``self`` overlaps ``other``. That is, both share at least an instant or a value.

        Examples:
            >>> Period('[2012-01-01, 2012-01-02]').overlaps(Period('[2012-01-02, 2012-01-03]'))
            >>> True
            >>> Period('[2012-01-01, 2012-01-02)').overlaps(Period('[2012-01-02, 2012-01-03]'))
            >>> False
            >>> Period('[2012-01-01, 2012-01-02)').overlaps(Period('(2012-01-02, 2012-01-03]'))
            >>> False

        Args:
            other: temporal object to compare with

        Returns:
            True if overlaps, False otherwise

        MEOS Functions:
            overlaps_tbox_tbox, overlaps_tbox_tnumber
        """
        if isinstance(other, TBox):
            return overlaps_tbox_tbox(self._inner, other._inner)
        elif isinstance(other, TNumber):
            return overlaps_tbox_tnumber(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def is_same(self, other: Union[TBox, TNumber]) -> bool:
        if isinstance(other, TBox):
            return same_tbox_tbox(self._inner, other._inner)
        elif isinstance(other, TNumber):
            return same_tbox_tnumber(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def is_left(self, other: Union[TBox, TNumber]) -> bool:
        if isinstance(other, TBox):
            return left_tbox_tbox(self._inner, other._inner)
        elif isinstance(other, TNumber):
            return left_tbox_tnumber(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def is_over_or_left(self, other: Union[TBox, TNumber]) -> bool:
        if isinstance(other, TBox):
            return overleft_tbox_tbox(self._inner, other._inner)
        elif isinstance(other, TNumber):
            return overleft_tbox_tnumber(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def is_right(self, other: Union[TBox, TNumber]) -> bool:
        if isinstance(other, TBox):
            return right_tbox_tbox(self._inner, other._inner)
        elif isinstance(other, TNumber):
            return right_tbox_tnumber(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def is_over_or_right(self, other: Union[TBox, TNumber]) -> bool:
        if isinstance(other, TBox):
            return overright_tbox_tbox(self._inner, other._inner)
        elif isinstance(other, TNumber):
            return overright_tbox_tnumber(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def is_before(self, other: Union[TBox, TNumber]) -> bool:
        if isinstance(other, TBox):
            return before_tbox_tbox(self._inner, other._inner)
        elif isinstance(other, TNumber):
            return before_tbox_tnumber(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def is_over_or_before(self, other: Union[TBox, TNumber]) -> bool:
        if isinstance(other, TBox):
            return overbefore_tbox_tbox(self._inner, other._inner)
        elif isinstance(other, TNumber):
            return overbefore_tbox_tnumber(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def is_after(self, other: Union[TBox, TNumber]) -> bool:
        if isinstance(other, TBox):
            return after_tbox_tbox(self._inner, other._inner)
        elif isinstance(other, TNumber):
            return after_tbox_tnumber(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def is_over_or_after(self, other: Union[TBox, TNumber]) -> bool:
        if isinstance(other, TBox):
            return overafter_tbox_tbox(self._inner, other._inner)
        elif isinstance(other, TNumber):
            return overafter_tbox_tnumber(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def nearest_approach_distance(self, other: TBox) -> float:
        if isinstance(other, TBox):
            return nad_tbox_tbox(self._inner, other._inner)
        else:
            raise TypeError(f'Operation not supported with type {other.__class__}')

    def __add__(self, other):
        """
        Returns the union of `self` with `other`. Fails if the union is not contiguous.

        Args:
            other: temporal object to merge with

        Returns:
            A :class:`TBox` instance.

        MEOS Functions:
            union_tbox_tbox
        """
        return self.union(other)

    def __mul__(self, other):
        """
        Returns the intersection of `self` with `other`.

        Args:
            other: temporal object to merge with

        Returns:
            A :class:`TBox` instance if the instersection is not empty, `None` otherwise.

        MEOS Functions:
            intersection_tbox_tbox
        """
        return self.intersection(other)

    def __contains__(self, item):
        """
        Returns whether ``self`` temporally contains ``item``.

        Examples:
            >>> TBox('TBox XT([2, 3], [2012-01-02, 2012-01-03]') in TBox('TBox XT([1, 4], [2012-01-01, 2012-01-04]')
            >>> True
            >>> TBox('TBox XT((1, 2), (2012-01-01, 2012-01-02)') in TBox('TBox XT([1, 2], [2012-01-01, 2012-01-02]')
            >>> True
            >>> TBox('TBox XT([1, 2], [2012-01-01, 2012-01-02]') in TBox('TBox XT((1, 2), (2012-01-01, 2012-01-02)')
            >>> False

        Args:
            item: temporal object to compare with

        Returns:
            True if contains, False otherwise

        MEOS Functions:
            contains_tbox_tbox, contains_tbox_tnumber
        """
        return self.contains(item)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return tbox_eq(self._inner, other._inner)
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return tbox_ne(self._inner, other._inner)
        return True

    def __cmp__(self, other):
        if isinstance(other, self.__class__):
            return tbox_cmp(self._inner, other._inner)
        raise TypeError(f'Operation not supported with type {other.__class__}')

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return tbox_lt(self._inner, other._inner)
        raise TypeError(f'Operation not supported with type {other.__class__}')

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return tbox_le(self._inner, other._inner)
        raise TypeError(f'Operation not supported with type {other.__class__}')

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return tbox_gt(self._inner, other._inner)
        raise TypeError(f'Operation not supported with type {other.__class__}')

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return tbox_ge(self._inner, other._inner)
        raise TypeError(f'Operation not supported with type {other.__class__}')

    def __copy__(self) -> TBox:
        inner_copy = tbox_copy(self._inner)
        return TBox(_inner=inner_copy)

    def __str__(self):
        return tbox_out(self._inner, 15)

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self})')

    def plot(self, *args, **kwargs):
        from ..plotters import BoxPlotter
        return BoxPlotter.plot_tbox(self, *args, **kwargs)

    @staticmethod
    def read_from_cursor(value, _=None):
        if not value:
            return None
        return TBox(string=value)
