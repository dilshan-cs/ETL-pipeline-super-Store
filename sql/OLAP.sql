-- Q1
SELECT
    CASE
        WHEN GROUPING(l."Region") = 1 THEN 'ALL REGIONS'
        ELSE l."Region"
    END AS "Region",

    CASE
        WHEN GROUPING(p."Category") = 1 THEN 'ALL CATEGORIES'
        ELSE p."Category"
    END AS "Category",

    ROUND(SUM(f."Sales"), 2) AS "Total Sales",
    ROUND(SUM(f."Profit"), 2) AS "Total Profit"

FROM "FACT SALES" f

JOIN "DIM LOCATION" l
    ON f."Location Key" = l."Location Key"

JOIN "DIM PRODUCT" p
    ON f."Product Key" = p."Product Key"

GROUP BY ROLLUP(
    l."Region",
    p."Category"
)

ORDER BY
    GROUPING(l."Region"),
    l."Region",
    GROUPING(p."Category"),
    p."Category";


-- Q2
SELECT
    CASE
        WHEN GROUPING(l."Region") = 1 THEN 'ALL REGIONS'
        ELSE l."Region"
    END AS "Region",

    CASE
        WHEN GROUPING(p."Category") = 1 THEN 'ALL CATEGORIES'
        ELSE p."Category"
    END AS "Category",

    ROUND(SUM(f."Sales"), 2) AS "Total Sales",
    ROUND(SUM(f."Profit"), 2) AS "Total Profit"

FROM "FACT SALES" f

JOIN "DIM LOCATION" l
    ON f."Location Key" = l."Location Key"

JOIN "DIM PRODUCT" p
    ON f."Product Key" = p."Product Key"

GROUP BY GROUPING SETS (
    (l."Region", p."Category"),
    (l."Region"),
    (p."Category"),
    ()
)

ORDER BY
    GROUPING(l."Region"),
    l."Region",
    GROUPING(p."Category"),
    p."Category";    

-- Q3
WITH monthly_sales AS (
    SELECT
        t."Year",
        t."Month",
        t."Month Name",
        ROUND(SUM(f."Sales"), 2) AS "Total Sales"

    FROM "FACT SALES" f

    JOIN "DIM TIME" t
        ON f."Order_Date_Key" = t."Time Key"

    GROUP BY
        t."Year",
        t."Month",
        t."Month Name"
)

SELECT
    "Year",
    "Month",
    "Month Name",
    "Total Sales",

    LAG("Total Sales") OVER (
        ORDER BY "Year", "Month"
    ) AS "Previous Month Sales",

    ROUND(
        "Total Sales" -
        LAG("Total Sales") OVER (
            ORDER BY "Year", "Month"
        ),
        2
    ) AS "Sales Change"

FROM monthly_sales

ORDER BY
    "Year",
    "Month"

LIMIT 20;

-- Q4
WITH monthly_sales AS (
    SELECT
        t."Year",
        t."Month",
        t."Month Name",
        ROUND(SUM(f."Sales"), 2) AS "Monthly Sales"

    FROM "FACT SALES" f

    JOIN "DIM TIME" t
        ON f."Order_Date_Key" = t."Time Key"

    GROUP BY
        t."Year",
        t."Month",
        t."Month Name"
)

SELECT
    "Year",
    "Month",
    "Month Name",
    "Monthly Sales",

    ROUND(
        SUM("Monthly Sales") OVER (
            ORDER BY "Year", "Month"
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ),
        2
    ) AS "Running Total Sales"

FROM monthly_sales

ORDER BY
    "Year",
    "Month"

LIMIT 20;

-- Q5
WITH product_sales AS (
    SELECT
        p."Category",
        p."Product Name",
        ROUND(SUM(f."Sales"), 2) AS "Total Sales"

    FROM "FACT SALES" f

    JOIN "DIM PRODUCT" p
        ON f."Product Key" = p."Product Key"

    GROUP BY
        p."Category",
        p."Product Name"
),

ranked_products AS (
    SELECT
        "Category",
        "Product Name",
        "Total Sales",

        DENSE_RANK() OVER (
            PARTITION BY "Category"
            ORDER BY "Total Sales" DESC
        ) AS "Sales Rank"

    FROM product_sales
)

SELECT
    "Category",
    "Product Name",
    "Total Sales",
    "Sales Rank"

FROM ranked_products

WHERE "Sales Rank" <= 3

ORDER BY
    "Category",
    "Sales Rank",
    "Product Name";

-- Q6
SELECT
    l."Region",
    p."Category",
    t."Year",
    ROUND(SUM(f."Sales"), 2) AS "Total Sales",
    ROUND(SUM(f."Profit"), 2) AS "Total Profit",
    SUM(f."Quantity") AS "Total Quantity"

FROM "FACT SALES" f

JOIN "DIM LOCATION" l
    ON f."Location Key" = l."Location Key"

JOIN "DIM PRODUCT" p
    ON f."Product Key" = p."Product Key"

JOIN "DIM TIME" t
    ON f."Order_Date_Key" = t."Time Key"

WHERE
    l."Region" = 'West'
    AND p."Category" = 'Technology'
    AND t."Year" = 2017

GROUP BY
    l."Region",
    p."Category",
    t."Year";
