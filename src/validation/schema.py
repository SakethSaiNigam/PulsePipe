import pandera as pa
from pandera import Column, Check
from datetime import datetime

EventsSchema = pa.DataFrameSchema({
    "user_id": Column(str, Check.str_length(6, 64)),
    "event": Column(str, Check.isin(["view","add_to_cart","purchase"])),
    "ts": Column(pa.DateTime),
    "latency_ms": Column(float, Check.ge(0) & Check.le(5000)),
    "date": Column(object),
    "hour": Column(int, Check.ge(0) & Check.le(23))
}, strict=True, coerce=True)

# KPI-level expectations
DailyFunnelSchema = pa.DataFrameSchema({
    "date": Column(object),
    "views": Column(int, Check.ge(0)),
    "adds": Column(int, Check.ge(0)),
    "purchases": Column(int, Check.ge(0)),
    "avg_latency_ms": Column(float, Check.ge(0))
}, strict=True, coerce=True)
