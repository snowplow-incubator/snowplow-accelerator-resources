SELECT
  l.domain_userid,
  l.derived_tstamp AS event_tstamp,
  u.last_consent_event_type AS actual_status,
  l.geo_country,
  l.event_name,
  l.event_id,
  l.event_type,
  l.consent_scopes,
  l.consent_version,
  l.consent_url,
  lag(l.derived_tstamp , 1) over(partition by l.domain_userid order by l.derived_tstamp) previous_event_tstamp,
  lag(l.event_type, 1) over(partition by l.domain_userid order by l.derived_tstamp) previous_event_type,
  lag(l.consent_scopes, 1) over(partition by l.domain_userid order by l.derived_tstamp) previous_consent_scopes,
  lag(l.consent_version, 1) over(partition by l.domain_userid order by l.derived_tstamp) previous_consent_version,
  lag(l.consent_url, 1) over(partition by l.domain_userid order by l.derived_tstamp) previous_consent_url

FROM snowplow_web_consent_LOG l

left join $1.$2.snowplow_web_consent_users u
on u.domain_userid = l.domain_userid

where event_name <> 'cmp_visible'

order by 2
