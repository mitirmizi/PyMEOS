from pymeos_cffi import tbool_tand_transfn, tbool_tor_transfn

from pymeos.aggregators.aggregator import BaseAggregator


class TemporalAndAggregator(BaseAggregator):
    _add_function = tbool_tand_transfn


class TemporalOrAggregator(BaseAggregator):
    _add_function = tbool_tor_transfn