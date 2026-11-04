CREATE DATABASE peru_tourism;

/* Creating Tables */
CREATE TABLE site_inventory(
    department TEXT,
    province TEXT,
    district TEXT,
    resource_id SERIAL PRIMARY KEY,
    resource_name TEXT,
    category TEXT,
    sub_category TEXT,
    resource_site TEXT,
    longitud FLOAT,
    latitud FLOAT, 
    cutoff_date DATE,
    entrance_type TEXT,
    observation TEXT,
    entrance_fee NUMERIC
);

CREATE TABLE site_visitors(
    cutoff_date DATE,
    year SMALLINT,
    month_id SMALLINT,
    month TEXT,
    department TEXT,
    site_name TEXT,
    visitor_type TEXT,
    num_visitors INT,
    PRIMARY KEY (year, month_id, site_name, visitor_type)
);

CREATE TABLE international_visitors(
    cutoff_date TEXT,
    year SMALLINT,
    month_id SMALLINT,
    month TEXT,
    country_id SMALLINT,
    country TEXT,
    continent_id SMALLINT,
    continent TEXT,
    ocm_id SMALLINT,
    ocm TEXT,
    ocm_department TEXT,
    num_visitors INT,
    visitor_type TEXT,
    PRIMARY KEY (year, month_id, country_id, ocm_id, visitor_type)
);



/* Copying CSV to Postgresql */
\copy site_inventory(
    department,
    province,
    district,
    resource_id,
    resource_name,
    category,
    sub_category,
    resource_site,
    longitud,
    latitud,
    cutoff_date,
    entrance_type,
    observation,
    entrance_fee    
) FROM 'C:\Datos\Limpios\inventario_recursos_turisticos.csv' 
DELIMITER ',' CSV HEADER;

\copy site_visitors(
    cutoff_date,
    year,
    month_id,
    month,
    department,
    site_name,
    visitor_type,
    num_visitors
) FROM 'C:\Datos\Limpios\visitantes_sitios_turisticos.csv' 
DELIMITER ',' CSV HEADER;

\copy international_visitors(
    cutoff_date,
    year,
    month_id,
    month,
    country_id,
    country,
    continent_id,
    continent,
    ocm_id,
    ocm,
    ocm_department,
    num_visitors,
    visitor_type
) FROM 'C:\Datos\Limpios\visitantes_internacionales.csv'
DELIMITER ',' CSV HEADER;




/* Tourism Inventory by Dept and Category*/
SELECT
    department,
    category,
    COUNT(*) AS total_resources,
    COUNT(DISTINCT province) AS total_provinces,
    COUNT(DISTINCT district) AS total_districts,
    ROUND(AVG(entrance_fee)::NUMERIC, 2) AS avg_entrance_fee,
    MIN(entrance_fee) AS min_entrance_fee,
    MAX(entrance_fee) AS max_entrance_fee
FROM site_inventory
WHERE department IS NOT NULL
GROUP BY
    department,
    category
ORDER BY
    total_resources DESC;






/* International Visitors by Country and Continent*/
WITH country_visitors AS (
    SELECT
        country,
        continent,
        SUM(num_visitors) AS total_visitors
    FROM international_visitors
    GROUP BY
        country,
        continent
),
total_visitors AS (
    SELECT
        SUM(total_visitors) AS grand_total
    FROM country_visitors
)
SELECT
    cv.country,
    cv.continent,
    cv.total_visitors,
    ROUND(
        cv.total_visitors * 100.0 /
        NULLIF(tv.grand_total, 0),
        2
    ) AS visitor_percentage,
    CASE
        WHEN cv.total_visitors * 100.0 /
             NULLIF(tv.grand_total, 0) >= 10
            THEN 'Major Market'
        WHEN cv.total_visitors * 100.0 /
             NULLIF(tv.grand_total, 0) >= 3
            THEN 'Medium Market'
        ELSE 'Small Market'
    END AS market_segment
FROM country_visitors cv
CROSS JOIN total_visitors tv
ORDER BY cv.total_visitors DESC;



/* Monthly Tourism */
WITH monthly_visitors AS (
    SELECT
        year,
        month_id,
        month,
        SUM(num_visitors) AS total_visitors
    FROM international_visitors
    GROUP BY
        year,
        month_id,
        month
),
monthly_analysis AS (
    SELECT
        year,
        month_id,
        month,
        total_visitors,

        AVG(total_visitors) OVER (
            PARTITION BY month_id
        ) AS historical_monthly_average,

        SUM(total_visitors) OVER (
            PARTITION BY year
        ) AS annual_visitors

    FROM monthly_visitors
)
SELECT
    year,
    month_id,
    month,
    total_visitors,
    ROUND(
        100.0 * total_visitors /
        NULLIF(annual_visitors, 0),
        2
    ) AS percentage_of_annual_visitors,
    ROUND(
        historical_monthly_average::NUMERIC,
        0
    ) AS historical_monthly_average,
    CASE
        WHEN month_id IN (7, 8) THEN 'Peak Season'
        WHEN month_id IN (1, 2, 3) THEN 'Low Season'
        ELSE 'Regular Season'
    END AS tourism_season
FROM monthly_analysis
ORDER BY
    year,
    month_id;