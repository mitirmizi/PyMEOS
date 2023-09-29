from copy import copy
from datetime import datetime, timezone, timedelta
from typing import List

import pytest

from pymeos import Period, PeriodSet, TimestampSet, TFloatInst, TFloatSeq, STBox, TFloatSeqSet, TBox
from tests.conftest import TestPyMEOS


class TestTimestampSet(TestPyMEOS):
    ts_set = TimestampSet('{2019-09-01 00:00:00+0, 2019-09-02 00:00:00+0, 2019-09-03 00:00:00+0}')

    @staticmethod
    def assert_timestampset_equality(ts_set: TimestampSet,
                                     timestamps: List[datetime]):
        assert ts_set.num_elements() == len(timestamps)
        assert ts_set.elements() == timestamps


class TestTimestampSetConstructors(TestTimestampSet):

    def test_string_constructor(self):
        self.assert_timestampset_equality(self.ts_set, [datetime(2019, 9, 1, 0, 0, 0, tzinfo=timezone.utc),
                                                        datetime(2019, 9, 2, 0, 0, 0, tzinfo=timezone.utc),
                                                        datetime(2019, 9, 3, 0, 0, 0, tzinfo=timezone.utc)])

    def test_list_constructor(self):
        ts_set = TimestampSet(elements=[datetime(2019, 9, 1, 0, 0, 0, tzinfo=timezone.utc),
                                        datetime(2019, 9, 2, 0, 0, 0, tzinfo=timezone.utc),
                                        datetime(2019, 9, 3, 0, 0, 0, tzinfo=timezone.utc)])
        self.assert_timestampset_equality(ts_set, [datetime(2019, 9, 1, 0, 0, 0, tzinfo=timezone.utc),
                                                   datetime(2019, 9, 2, 0, 0, 0, tzinfo=timezone.utc),
                                                   datetime(2019, 9, 3, 0, 0, 0, tzinfo=timezone.utc)])

    def test_hexwkb_constructor(self):
        ts_set = TimestampSet.from_hexwkb('012000010300000000A01E4E713402000000F66B853402000060CD8999340200')
        self.assert_timestampset_equality(ts_set, [datetime(2019, 9, 1, 0, 0, 0, tzinfo=timezone.utc),
                                                   datetime(2019, 9, 2, 0, 0, 0, tzinfo=timezone.utc),
                                                   datetime(2019, 9, 3, 0, 0, 0, tzinfo=timezone.utc)])

    def test_from_as_constructor(self):
        assert self.ts_set == TimestampSet(str(self.ts_set))
        assert self.ts_set == TimestampSet.from_wkb(self.ts_set.as_wkb())
        assert self.ts_set == TimestampSet.from_hexwkb(self.ts_set.as_hexwkb())

    def test_copy_constructor(self):
        ts_set_copy = copy(self.ts_set)
        assert self.ts_set == ts_set_copy
        assert self.ts_set is not ts_set_copy


class TestTimestampSetOutputs(TestTimestampSet):

    def test_str(self):
        assert str(self.ts_set) == '{"2019-09-01 00:00:00+00", "2019-09-02 00:00:00+00", "2019-09-03 00:00:00+00"}'

    def test_repr(self):
        assert repr(self.ts_set) == 'TimestampSet({"2019-09-01 00:00:00+00", "2019-09-02 00:00:00+00", "2019-09-03 00:00:00+00"})'

    def test_as_hexwkb(self):
        assert self.ts_set.as_hexwkb() == '012000010300000000A01E4E713402000000F66B853402000060CD8999340200'


class TestTimestampConversions(TestTimestampSet):

    def test_to_periodset(self):
        assert self.ts_set.to_periodset() == PeriodSet(
            '{[2019-09-01 00:00:00+00, 2019-09-01 00:00:00+00], '
            '[2019-09-02 00:00:00+00, 2019-09-02 00:00:00+00], '
            '[2019-09-03 00:00:00+00, 2019-09-03 00:00:00+00]}')


class TestTimestampSetAccessors(TestTimestampSet):

    def test_duration(self):
        assert self.ts_set.duration() == timedelta(days=2)

    def test_period(self):
        assert self.ts_set.to_period() == Period('[2019-09-01 00:00:00+00, 2019-09-03 00:00:00+00]')

    def test_num_timestamps(self):
        assert self.ts_set.num_elements() == 3
        assert len(self.ts_set) == 3

    def test_start_timestamp(self):
        assert self.ts_set.start_element() == datetime(2019, 9, 1, 0, 0, 0, tzinfo=timezone.utc)

    def test_end_timestamp(self):
        assert self.ts_set.end_element() == datetime(2019, 9, 3, 0, 0, 0, tzinfo=timezone.utc)

    def test_timestamp_n(self):
        assert self.ts_set.element_n(1) == datetime(2019, 9, 2, 0, 0, 0, tzinfo=timezone.utc)

    def test_timestamp_n_out_of_range(self):
        with pytest.raises(IndexError):
            self.ts_set.element_n(3)

    def test_timestamps(self):
        assert self.ts_set.elements() == [datetime(2019, 9, 1, 0, 0, 0, tzinfo=timezone.utc),
                                          datetime(2019, 9, 2, 0, 0, 0, tzinfo=timezone.utc),
                                          datetime(2019, 9, 3, 0, 0, 0, tzinfo=timezone.utc),
                                          ]

    def test_hash(self):
        assert hash(self.ts_set) == 527267058


class TestTimestampSetPositionFunctions(TestTimestampSet):
    timestamp = datetime(year=2020, month=1, day=1)
    timestampset = TimestampSet('{2020-01-01 00:00:00+0, 2020-01-31 00:00:00+0}')

    @pytest.mark.parametrize(
        'other, expected',
        [(timestampset, False)],
        ids=['timestampset']
    )
    def test_is_contained_in(self, other, expected):
        assert self.ts_set.is_contained_in(other) == expected

    @pytest.mark.parametrize(
        'other',
        [timestamp, timestampset],
        ids=['timestamp', 'timestampset']
    )
    def test_contains(self, other):
        self.ts_set.contains(other)
        _ = other in self.timestampset

    @pytest.mark.parametrize(
        'other',
        [timestampset],
        ids=['timestampset']
    )
    def test_overlaps(self, other):
        self.ts_set.overlaps(other)

    @pytest.mark.parametrize(
        'other',
        [timestamp, timestampset],
        ids=['timestamp', 'timestampset']
    )
    def test_is_before(self, other):
        self.ts_set.is_before(other)

    @pytest.mark.parametrize(
        'other',
        [timestamp, timestampset],
        ids=['timestamp', 'timestampset']
    )
    def test_is_over_or_before(self, other):
        self.ts_set.is_over_or_before(other)

    @pytest.mark.parametrize(
        'other',
        [timestamp, timestampset],
        ids=['timestamp', 'timestampset']
    )
    def test_is_after(self, other):
        self.ts_set.is_after(other)

    @pytest.mark.parametrize(
        'other',
        [timestamp, timestampset],
        ids=['timestamp', 'timestampset']
    )
    def test_is_over_or_after(self, other):
        self.ts_set.is_over_or_after(other)

    @pytest.mark.parametrize(
        'other',
        [timestamp, timestampset],
        ids=['timestamp', 'timestampset']
    )
    def test_distance(self, other):
        self.ts_set.distance(other)


class TestTimestampSetSetFunctions(TestTimestampSet):
    timestamp = datetime(year=2020, month=1, day=1)
    timestampset = TimestampSet('{2020-01-01 00:00:00+0, 2020-01-31 00:00:00+0}')
    period = Period('(2020-01-01 00:00:00+0, 2020-01-31 00:00:00+0)')
    periodset = PeriodSet(
        '{(2020-01-01 00:00:00+0, 2020-01-31 00:00:00+0), (2021-01-01 00:00:00+0, 2021-01-31 00:00:00+0)}')

    @pytest.mark.parametrize(
        'other',
        [period, periodset, timestamp, timestampset],
        ids=['period', 'periodset', 'timestamp', 'timestampset']
    )
    def test_intersection(self, other):
        self.timestampset.intersection(other)
        self.timestampset * other

    @pytest.mark.parametrize(
        'other',
        [period, periodset, timestamp, timestampset],
        ids=['period', 'periodset', 'timestamp', 'timestampset']
    )
    def test_union(self, other):
        self.timestampset.union(other)
        self.timestampset + other

    @pytest.mark.parametrize(
        'other',
        [period, periodset, timestamp, timestampset],
        ids=['period', 'periodset', 'timestamp', 'timestampset']
    )
    def test_minus(self, other):
        self.timestampset.minus(other)
        self.timestampset - other


class TestTimestampSetComparisons(TestTimestampSet):
    timestampset = TimestampSet('{2020-01-01 00:00:00+0, 2020-01-31 00:00:00+0}')
    other = TimestampSet('{2020-01-02 00:00:00+0, 2020-03-31 00:00:00+0}')

    def test_eq(self):
        _ = self.timestampset == self.other

    def test_ne(self):
        _ = self.timestampset != self.other

    def test_lt(self):
        _ = self.timestampset < self.other

    def test_le(self):
        _ = self.timestampset <= self.other

    def test_gt(self):
        _ = self.timestampset > self.other

    def test_ge(self):
        _ = self.timestampset >= self.other


class TestTimestampSetFunctionsFunctions(TestTimestampSet):
    timestampset = TimestampSet('{2020-01-01 00:00:00+0, 2020-01-02 00:00:00+0, 2020-01-04 00:00:00+0}')

    @pytest.mark.parametrize(
        'delta,result',
        [(timedelta(days=4),
          [datetime(2020, 1, 5, tzinfo=timezone.utc), datetime(2020, 1, 6, tzinfo=timezone.utc),
           datetime(2020, 1, 8, tzinfo=timezone.utc)]),
         (timedelta(days=-4),
          [datetime(2019, 12, 28, tzinfo=timezone.utc), datetime(2019, 12, 29, tzinfo=timezone.utc),
           datetime(2019, 12, 31, tzinfo=timezone.utc)]),
         (timedelta(hours=2),
          [datetime(2020, 1, 1, 2, tzinfo=timezone.utc), datetime(2020, 1, 2, 2, tzinfo=timezone.utc),
           datetime(2020, 1, 4, 2, tzinfo=timezone.utc)]),
         (timedelta(hours=-2),
          [datetime(2019, 12, 31, 22, tzinfo=timezone.utc), datetime(2020, 1, 1, 22, tzinfo=timezone.utc),
           datetime(2020, 1, 3, 22, tzinfo=timezone.utc)]),
         ],
        ids=['positive days', 'negative days', 'positive hours', 'negative hours']
    )
    def test_shift(self, delta, result):
        shifted = self.timestampset.shift(delta)
        self.assert_timestampset_equality(shifted, result)

    @pytest.mark.parametrize(
        'delta,result',
        [(timedelta(days=6),
          [datetime(2020, 1, 1, tzinfo=timezone.utc), datetime(2020, 1, 3, tzinfo=timezone.utc),
           datetime(2020, 1, 7, tzinfo=timezone.utc)]),
         (timedelta(hours=3),
          [datetime(2020, 1, 1, tzinfo=timezone.utc), datetime(2020, 1, 1, 1, tzinfo=timezone.utc),
           datetime(2020, 1, 1, 3, tzinfo=timezone.utc)]),
         ],
        ids=['days', 'hours']
    )
    def test_scale(self, delta, result):
        scaled = self.timestampset.scale(delta)
        self.assert_timestampset_equality(scaled, result)

    def test_shift_scale(self):
        shifted_scaled = self.timestampset.shift_scale(timedelta(days=4), timedelta(hours=3))
        self.assert_timestampset_equality(shifted_scaled,
                                          [datetime(2020, 1, 5, tzinfo=timezone.utc),
                                           datetime(2020, 1, 5, 1, tzinfo=timezone.utc),
                                           datetime(2020, 1, 5, 3, tzinfo=timezone.utc)])


class TestTimestampSetMiscFunctions(TestTimestampSet):
    timestampset = TimestampSet('{2020-01-01 00:00:00+0, 2020-01-02 00:00:00+0, 2020-01-04 00:00:00+0}')

    def test_hash(self):
        hash(self.timestampset)
