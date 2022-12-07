select
  l.domain_userid,
  l.derived_tstamp as event_tstamp,
  l.event_name,
  l.event_type,
  l.geo_country,
  l.consent_url as "PRIVACY POLICY URL",
  l.consent_version,
  l.consent_scopes,
  l.domains_applied,
  u.last_consent_event_type as "ACTUAL STATUS"

from snowplow_web_consent_log l
left join snowplow_web_consent_users u
on u.domain_userid = l.domain_userid

order by 2
