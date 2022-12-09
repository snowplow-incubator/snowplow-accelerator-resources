SELECT date(START_TSTAMP) as Date, count(1) AS number_of_sessions
FROM snowplow_mobile_sessions
-- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
group BY date(START_TSTAMP)
order BY date(START_TSTAMP)
