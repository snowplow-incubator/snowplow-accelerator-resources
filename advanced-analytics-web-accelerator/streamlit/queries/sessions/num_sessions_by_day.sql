SELECT date(START_TSTAMP) AS Date, count(1) AS number_of_sessions
FROM $1.$2.snowplow_web_sessions
-- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
GROUP BY DATE(START_TSTAMP)
ORDER BY DATE(START_TSTAMP)
