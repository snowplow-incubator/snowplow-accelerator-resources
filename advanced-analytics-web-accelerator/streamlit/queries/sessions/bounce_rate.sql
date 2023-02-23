WITH single_pageviews AS
    (SELECT DOMAIN_SESSIONID, count(1) AS single_pageviews
    FROM $1.$2.snowplow_web_sessions
    WHERE PAGE_VIEWS = 1
    -- filter data range, if needed, example: AND START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
    GROUP BY DOMAIN_SESSIONID),

total_pageviews AS
    (
        SELECT DOMAIN_SESSIONID, sum(PAGE_VIEWS)  AS total_pageviews
        FROM $1.$2.snowplow_web_sessions
        -- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
        GROUP BY DOMAIN_SESSIONID
    )

SELECT sum(single_pageviews.single_pageviews) / SUM(total_pageviews.total_pageviews) AS BounceRate
FROM  total_pageviews
LEFT JOIN single_pageviews
ON total_pageviews.DOMAIN_SESSIONID = single_pageviews.DOMAIN_SESSIONID
