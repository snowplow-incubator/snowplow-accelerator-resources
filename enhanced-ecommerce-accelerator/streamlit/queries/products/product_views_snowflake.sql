-- Product views in out-of-stock products
with latest_date AS (
    select
        MAX(DATE(derived_tstamp)) as max_date
    from $1.$2.SNOWPLOW_ECOMMERCE_PRODUCT_INTERACTIONS
), temp AS (
    select
        ld.max_date - seq4() as dates

    FROM TABLE(GENERATOR(rowcount => 30))
    JOIN latest_date as ld ON 1=1
    ORDER BY 1 ASC
),

product_views as (
    SELECT
        DATE_TRUNC(DAY, CAST(derived_tstamp AS DATE)) AS Dates,
        COUNT(DISTINCT event_id) AS number_views
    FROM
        $1.$2.snowplow_ecommerce_product_interactions
    WHERE
        is_product_view
    group by 1
)

SELECT
    temp.dates AS Date,
    coalesce(number_views, 0) AS product_views
FROM
    TEMP
    LEFT JOIN product_views b
        ON temp.dates = b.dates
;
