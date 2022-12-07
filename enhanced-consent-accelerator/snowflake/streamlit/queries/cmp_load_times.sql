select
  'within 2 sec' as base,
  count(case when cmp_load_time <= 2 then 1 end) as value
from snowplow_web_consent_cmp_stats

union all

select
  'between 2 and 5 seconds' as base,
  count(case when cmp_load_time > 2 and cmp_load_time <= 5 then 1 end) as value
from snowplow_web_consent_cmp_stats

union all

select
  'between 5 and 10 seconds' as base,
  count(case when cmp_load_time >5 and cmp_load_time <= 10 then 1 end) as value
from snowplow_web_consent_cmp_stats

union all

select
  'between 10 and 30 seconds' as base,
  count(case when cmp_load_time >10 and cmp_load_time <= 30 then 1 end) as value
from snowplow_web_consent_cmp_stats

union all

select
  'after 30+ seconds' as base,
  count(case when cmp_load_time > 30 then 1 end) as value
from snowplow_web_consent_cmp_stats
