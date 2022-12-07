SELECT PAGE_TITLE, SUM(PAGE_VIEWS_IN_SESSION) AS number_of_pageviews
FROM snowplow_web_page_views
WHERE PAGE_TITLE IS NOT NULL
-- filter data range, if needed, example: AND START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
GROUP BY PAGE_TITLE
ORDER BY number_of_pageviews DESC
LIMIT 10
