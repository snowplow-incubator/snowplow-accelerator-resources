SELECT DATE(START_TSTAMP) AS Date, COUNT(1) AS number_of_pageviews
FROM snowplow_web_page_views
-- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
GROUP BY DATE(START_TSTAMP)
ORDER BY DATE(START_TSTAMP)
