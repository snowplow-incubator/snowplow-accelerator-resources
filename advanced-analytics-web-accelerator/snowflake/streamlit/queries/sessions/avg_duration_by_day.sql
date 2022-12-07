SELECT DATE(START_TSTAMP) AS Date,  round(avg(engaged_time_in_s), 0) AS Avg_Engaged_Time
FROM snowplow_web_sessions
-- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
GROUP BY DATE(START_TSTAMP)
ORDER BY DATE(START_TSTAMP)
