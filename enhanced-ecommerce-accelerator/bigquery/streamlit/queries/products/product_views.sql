-- Product views in out-of-stock products
with temp as (
    SELECT dates , CAST(FLOOR(590*RAND()) AS INT64) as random_number FROM (
        SELECT
            MAX(date_trunc(CAST(derived_tstamp AS DATE), DAY)) max_date
        FROM
            `$1`.`$2`.snowplow_ecommerce_product_interactions
    ), UNNEST(GENERATE_DATE_ARRAY(max_date - 30, max_date)) dates
),

product_views as (
    SELECT
        DATE_TRUNC(CAST(derived_tstamp AS DATE), DAY) AS Dates,
        COUNT(DISTINCT event_id) AS number_views
    FROM
        `$1`.`$2`.snowplow_ecommerce_product_interactions
    WHERE
        is_product_view
    group by 1
)

SELECT
    temp.dates AS Date,
    --coalesce(number_views, 0) AS product_views
    random_number as product_views -- demo purpose only!
FROM
    TEMP
    LEFT JOIN product_views b
        ON temp.dates = b.dates
