SELECT SCREEN_VIEW_NAME, sum(SCREEN_VIEWS_IN_SESSION) AS number_of_screenviews
FROM snowplow_mobile_screen_views
WHERE SCREEN_VIEW_NAME IS NOT NULL
-- filter data range, if needed, example: AND DVCE_CREATED_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
GROUP BY SCREEN_VIEW_NAME
ORDER BY number_of_screenviews DESC
LIMIT 10
