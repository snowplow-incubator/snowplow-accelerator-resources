WITH
single_pageviews AS
    (
        SELECT DATE(START_TSTAMP) AS Date, count(1) AS single_pageviews
        FROM $1.$2.snowplow_web_sessions
        WHERE PAGE_VIEWS = 1
        -- filter data range, if needed, example: AND START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
        GROUP BY DATE(START_TSTAMP)
    ),

total_pageviews AS
    (
        SELECT DATE(START_TSTAMP) AS Date,  SUM(PAGE_VIEWS) AS total_pageviews
        FROM $1.$2.snowplow_web_sessions
        -- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
        GROUP BY DATE(START_TSTAMP)
    )

SELECT total_pageviews.Date, SUM(single_pageviews.single_pageviews) / SUM(total_pageviews.total_pageviews) AS BounceRate
FROM total_pageviews
JOIN single_pageviews
ON single_pageviews.Date = total_pageviews.Date
GROUP BY total_pageviews.Date
ORDER BY total_pageviews.Date
