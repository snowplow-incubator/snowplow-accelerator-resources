select date(START_TSTAMP) as Date,  round(avg(session_duration_s), 0) as Avg_Session_Duration
from snowplow_mobile_sessions
-- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
group BY date(START_TSTAMP)
order BY date(START_TSTAMP)
