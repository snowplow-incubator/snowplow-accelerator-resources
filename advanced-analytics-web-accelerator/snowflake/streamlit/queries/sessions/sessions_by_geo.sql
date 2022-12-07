SELECT geo_country, count(1) AS number_of_sessions
FROM snowplow_web_sessions
WHERE geo_country IS NOT NULL
-- filter data range, if needed, example: AND START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
GROUP BY 1
ORDER BY 2 DESC
