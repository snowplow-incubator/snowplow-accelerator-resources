-- guest checkout rate
select
    coalesce(COUNT(DISTINCT CASE WHEN ecommerce_user_is_guest THEN event_id END) /nullif(COUNT(DISTINCT event_id),0) * 1.0,0) as guest_checkout_rate
from
    `$1`.`$2`.snowplow_ecommerce_checkout_interactions
where
    checkout_succeeded
