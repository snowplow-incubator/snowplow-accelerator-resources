SELECT REFR_URLHOST, SUM(PAGE_VIEWS_IN_SESSION) AS number_of_pageviews
FROM $1.$2.snowplow_web_page_views
WHERE REFR_URLHOST IS NOT NULL
-- filter data range, if needed, example: AND START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
GROUP BY REFR_URLHOST
ORDER BY number_of_pageviews DESC
LIMIT 10
