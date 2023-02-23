select
  'Consent Granted' as base,
  count(case when is_latest_version and last_consent_event_type='allow_all' then 1 end) as value
from $1.$2.snowplow_web_consent_users

union all

select
  'Partially Granted (Customised)' as base,
  count(case when is_latest_version and last_consent_event_type ='allow_selected' then 1 end) as value
from $1.$2.snowplow_web_consent_users

union all

select
  'Consent Pending' as base,
  count(case when is_latest_version and last_consent_event_type = 'pending' then 1 end) as value
from $1.$2.snowplow_web_consent_users

union all

select
  'Denied' as base,
  count(case when is_latest_version and last_consent_event_type = 'deny_all'  then 1 end) as value
from $1.$2.snowplow_web_consent_users

union all

select
  'Expired' as base,
  count(case when is_latest_version and last_consent_event_type = 'expired'  then 1 end) as value
from $1.$2.snowplow_web_consent_users

union all

select
  'Withdrawn' as base,
  count(case when is_latest_version and last_consent_event_type = 'withdrawn'  then 1 end) as value
from $1.$2.snowplow_web_consent_users
