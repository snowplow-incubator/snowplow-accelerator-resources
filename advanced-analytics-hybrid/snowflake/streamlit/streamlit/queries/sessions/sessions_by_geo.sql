select geo_country, count(1) as number_of_sessions
from snowplow_mobile_sessions
where geo_country is not null
-- filter data range, if needed, example: AND START_TSTAMP BETWEEN DATEADD(day, -7, GETDATE()) AND  DATEADD(day, -1, GETDATE())
group by 1
order by 2 desc
