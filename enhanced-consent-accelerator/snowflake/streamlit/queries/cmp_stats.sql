select
  event_id,
  domain_userid,
  round(cmp_load_time, 2) as "CMP load time",
  cmp_tstamp,
  first_consent_event_tstamp,
  first_consent_event_type as "First consent event type",
  cmp_interaction_time as "CMP interaction time"
from snowplow_web_consent_cmp_stats
