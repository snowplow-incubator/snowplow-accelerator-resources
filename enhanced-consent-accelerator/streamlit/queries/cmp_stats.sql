select
  event_id,
  domain_userid,
  round(cmp_load_time, 2) as cmp_load_time,
  cmp_tstamp,
  first_consent_event_tstamp,
  first_consent_event_type as First_consent_event_type,
  cmp_interaction_time as CMP_interaction_time
from $1.$2.snowplow_web_consent_cmp_stats
