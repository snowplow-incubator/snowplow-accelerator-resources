select
  l.domain_userid,
  l.derived_tstamp as event_tstamp,
  l.event_name,
  l.event_type,
  l.geo_country,
  l.consent_url as PRIVACY_POLICY_URL,
  l.consent_version,
  l.consent_scopes,
  l.domains_applied,
  u.last_consent_event_type as ACTUAL_STATUS

from $1.$2.snowplow_web_consent_log l
left join $1.$2.snowplow_web_consent_users u
on u.domain_userid = l.domain_userid

order by 2
