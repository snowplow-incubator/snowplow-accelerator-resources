WITH
single_screenviews as
    (
        SELECT date(START_TSTAMP) as Date, count(1) AS single_screenviews
        FROM $1.$2.snowplow_mobile_sessions
        WHERE SCREEN_VIEWS = 1
        -- filter data range, if needed, example: AND START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
        GROUP BY  date(START_TSTAMP)
    ),

total_screenviews as
    (
        SELECT date(START_TSTAMP) as Date,  sum(SCREEN_VIEWS) AS total_screenviews
        FROM $1.$2.snowplow_mobile_sessions
        -- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
        GROUP BY  date(START_TSTAMP)
    )

SELECT total_screenviews.Date, sum(single_screenviews.single_screenviews) / sum(total_screenviews.total_screenviews) as BounceRate
FROM total_screenviews
join single_screenviews
ON single_screenviews.Date = total_screenviews.Date
group by total_screenviews.Date
order by total_screenviews.Date
