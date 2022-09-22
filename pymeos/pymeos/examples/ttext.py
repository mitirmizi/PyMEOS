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

from datetime import datetime, timedelta
from dateutil.parser import parse

from .. import TInterpolation
from ..time import TimestampSet, Period, PeriodSet
from ..main import TTextInst, TTextSeq, TTextSeqSet

print("\nConstructors for TTextInst")
inst = TTextInst(string='A@2019-09-08')
print(inst)
inst = TTextInst(value='A', timestamp='2019-09-08')
print(inst)
t = parse('2019-09-08')
inst = TTextInst(value='A', timestamp=t)
print(inst)

print("\nConstructors for TTextInstSet")
ti = TTextSeq(string='{A@2019-09-08, B@2019-09-09, B@2019-09-10}')
print(ti)
ti = TTextSeq(instant_list=['A@2019-09-08', 'B@2019-09-09', 'B@2019-09-10'], interpolation=TInterpolation.DISCRETE)
print(ti)
t1 = TTextInst(string='A@2019-09-08')
t2 = TTextInst(string='B@2019-09-09')
t3 = TTextInst(string='B@2019-09-10')
ti = TTextSeq(instant_list=[t1, t2, t3], interpolation=TInterpolation.DISCRETE)
print(ti)

print("\nConstructors for TTextSeq")
seq = TTextSeq(string='[A@2019-09-08, B@2019-09-09, B@2019-09-10]')
print(seq)
seq = TTextSeq(instant_list=['A@2019-09-08', 'B@2019-09-09', 'B@2019-09-10'])
print(seq)
seq = TTextSeq(instant_list=[t1, t2, t3])
print(seq)
seq = TTextSeq(instant_list=[t1, t2, t3], lower_inc=False, upper_inc=True)
print(seq)

print("\nConstructors for TTextSeqSet")
ts = TTextSeqSet(string='{[A@2019-09-08, B@2019-09-09, B@2019-09-10],[B@2019-09-11, C@2019-09-12]}')
print(ts)
ts = TTextSeqSet(sequence_list=['[A@2019-09-08, B@2019-09-09, B@2019-09-10]', '[B@2019-09-11, C@2019-09-12]'])
print(ts)
seq1 = TTextSeq(string='[A@2019-09-08, B@2019-09-09, B@2019-09-10]')
seq2 = TTextSeq(string='[B@2019-09-11, C@2019-09-12]')
ts = TTextSeqSet(sequence_list=[seq1, seq2])
print(ts)

print("\n__class__ ")
print(inst.__class__.__name__)
print(ti.__class__.__name__)
print(seq.__class__.__name__)
print(ts.__class__.__name__)

print("\n__bases__ ")
print(inst.__class__.__bases__)
print(ti.__class__.__bases__)
print(seq.__class__.__bases__)
print(ts.__class__.__bases__)

print("\ntempSubtype")
print(inst.temp_subtype())
print(ti.temp_subtype())
print(seq.temp_subtype())
print(ts.temp_subtype())

print("\ninterpolation")
print(seq.interpolation)
print(ts.interpolation)

print("\ngetValue")
print(inst.value)

print("\ngetValues")
print(inst.values)
print(ti.values)
print(seq.values)
print(ts.values)

print("\nstartValue")
print(inst.start_value)
print(ti.start_value)
print(seq.start_value)
print(ts.start_value)

print("\nendValue")
print(inst.end_value)
print(ti.end_value)
print(seq.end_value)
print(ts.end_value)

print("\nminValue")
print(inst.min_value)
print(ti.min_value)
print(seq.min_value)
print(ts.min_value)

print("\nmaxValue")
print(inst.max_value)
print(ti.max_value)
print(seq.max_value)
print(ts.max_value)

print("\ngetTimestamp")
print(inst.timestamp)

print("\ngetTime")
print(inst.time)
print(ti.time)
print(seq.time)
print(ts.time)

print("\nduration")
print(inst.duration)
print(ti.duration)
print(seq.duration)
print(ts.duration)

print("\ntimespan")
print(inst.timespan)
print(ti.timespan)
print(seq.timespan)
print(ts.timespan)

print("\nperiod")
print(inst.period)
print(ti.period)
print(seq.period)
print(ts.period)

print("\nnumInstants")
print(inst.num_instants)
print(ti.num_instants)
print(seq.num_instants)
print(ts.num_instants)

print("\nstartInstant")
print(inst.start_instant)
print(ti.start_instant)
print(seq.start_instant)
print(ts.start_instant)

print("\nendInstant")
print(inst.end_instant)
print(ti.end_instant)
print(seq.end_instant)
print(ts.end_instant)

print("\ninstantN")
print(inst.instant_n(1))
print(ti.instant_n(1))
print(seq.instant_n(1))
print(ts.instant_n(1))

print("\ninstants")
print(inst.instants)
print(ti.instants)
print(seq.instants)
print(ts.instants)

print("\nnumTimestamps")
print(inst.num_timestamps)
print(ti.num_timestamps)
print(seq.num_timestamps)
print(ts.num_timestamps)

print("\nstartTimestamp")
print(inst.start_timestamp)
print(ti.start_timestamp)
print(seq.start_timestamp)
print(ts.start_timestamp)

print("\nendTimestamp")
print(inst.end_timestamp)
print(ti.end_timestamp)
print(seq.end_timestamp)
print(ts.end_timestamp)

print("\ntimestampN")
print(inst.timestamp_n(1))
print(ti.timestamp_n(1))
print(seq.timestamp_n(1))
print(ts.timestamp_n(1))

print("\ntimestamps")
print(inst.timestamps)
print(ti.timestamps)
print(seq.timestamps)
print(ts.timestamps)

print("\nnumSequences")
print(seq.num_sequences)
print(ts.num_sequences)

print("\nstartSequence")
print(seq.start_sequence)
print(ts.start_sequence)

print("\nendSequence")
print(seq.end_sequence)
print(ts.end_sequence)

print("\nsequenceN")
print(seq.sequence_n(1))
print(ts.sequence_n(1))

print("\nsequences")
print(seq.sequences)
print(ts.sequences)

print("\nshift")
print(inst.shift_tscale(timedelta(days=1)))
print(ti.shift_tscale(timedelta(days=1)))
print(seq.shift_tscale(timedelta(days=1)))
print(ts.shift_tscale(timedelta(days=1)))

print("\nintersectsTimestamp")
t = datetime.strptime('2019-09-09', '%Y-%m-%d')
print(inst.intersects(t))
print(ti.intersects(t))
print(seq.intersects(t))
print(ts.intersects(t))

print("\nintersectsTimestampSet")
tss = TimestampSet(string='{2019-09-09, 2019-09-10}')
print(inst.intersects(tss))
print(ti.intersects(tss))
print(seq.intersects(tss))
print(ts.intersects(tss))

print("\nintersectsPeriod")
p = Period(lower='2019-09-09', upper='2019-09-10', lower_inc=True, upper_inc=True)
print(inst.intersects(p))
print(ti.intersects(p))
print(seq.intersects(p))
print(ts.intersects(p))

print("\nintersectsPeriodSet")
ps = PeriodSet(string='{[2019-09-09,2019-09-10], [2019-09-11,2019-09-12]}')
print(inst.intersects(ps))
print(ti.intersects(ps))
print(seq.intersects(ps))
print(ts.intersects(ps))
