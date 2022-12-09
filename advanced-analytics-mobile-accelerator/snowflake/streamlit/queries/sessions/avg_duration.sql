select round(avg(session_duration_s), 0) as average_session_session_duration_s
from snowplow_mobile_sessions
-- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
