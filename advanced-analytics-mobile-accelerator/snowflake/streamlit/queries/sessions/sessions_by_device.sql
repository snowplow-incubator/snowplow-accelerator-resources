select device_model, count(*) as number_of_sessions
from snowplow_mobile_sessions
-- filter data range, if needed, example: WHERE START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
group by 1
order by 2 desc
limit 8
