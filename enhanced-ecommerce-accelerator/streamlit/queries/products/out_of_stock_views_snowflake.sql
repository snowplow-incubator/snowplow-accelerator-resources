-- Product views in out-of-stock products
with latest_date AS (
    select
        MAX(DATE(derived_tstamp)) as max_date
    from $1.$2.SNOWPLOW_ECOMMERCE_PRODUCT_INTERACTIONS
), temp AS (
    select
        ld.max_date - seq4() as dates,
        uniform(1,590, random()) as random_number

    FROM TABLE(GENERATOR(rowcount => 30))
    JOIN latest_date as ld ON 1=1
    ORDER BY 1 ASC
),

out_of_stock_views as (
    SELECT
        DATE_TRUNC(DAY, CAST(derived_tstamp AS DATE)) AS Dates,
        COUNT(DISTINCT event_id) AS number_views
    FROM
        $1.$2.snowplow_ecommerce_product_interactions
    WHERE
        is_product_view
        AND product_inventory_status = 'out_of_stock'
    group by 1
)

SELECT
    temp.dates AS Date,
    coalesce(number_views, 0) AS out_of_stock_views
FROM
    TEMP
    LEFT JOIN out_of_stock_views b
        ON temp.dates = b.dates
