SELECT ROUND(AVG(engaged_time_in_s), 0) AS average_session_engaged_time_in_s
FROM $1.$2.snowplow_web_sessions
-- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
