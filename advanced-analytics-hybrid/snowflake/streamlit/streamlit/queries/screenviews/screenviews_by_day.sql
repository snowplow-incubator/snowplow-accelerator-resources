SELECT date(DVCE_CREATED_TSTAMP) as Date, count(1) AS number_of_screenviews
FROM snowplow_mobile_screen_views
-- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
group BY date(DVCE_CREATED_TSTAMP)
order BY date(DVCE_CREATED_TSTAMP)
