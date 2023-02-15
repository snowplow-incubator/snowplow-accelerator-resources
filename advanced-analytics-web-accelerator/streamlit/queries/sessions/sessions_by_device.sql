SELECT device_family, count(*) AS number_of_sessions
FROM $1.$2.snowplow_web_sessions
-- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
GROUP BY 1
ORDER BY 2 DESC
LIMIT 8
