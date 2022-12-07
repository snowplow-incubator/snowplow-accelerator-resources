SELECT count(1) AS number_of_sessions
FROM snowplow_web_sessions
-- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
