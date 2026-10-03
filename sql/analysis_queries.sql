CREATE DATABASE IF NOT EXISTS uae_weather;
USE uae_weather;
CREATE TABLE climate_data (
    date DATE,
    city VARCHAR(50),
    max_temp DECIMAL(5,2),
    min_temp DECIMAL(5,2),
    mean_temp DECIMAL(5,2),
    humidity DECIMAL(5,2),
    precipitation DECIMAL(7,2)
);
SELECT *
FROM climate_data
LIMIT 10;
SELECT COUNT(*) AS total_records
FROM climate_data;
SELECT DISTINCT city
FROM climate_data;
SELECT 
    MIN(date) AS first_date,
    MAX(date) AS last_date
FROM climate_data;
CREATE VIEW climate_analysis AS
SELECT
    date,
    city,
    max_temp,
    min_temp,
    mean_temp,
    humidity,
    precipitation,
    (max_temp - min_temp) AS temperature_range
FROM climate_data;
SELECT *
FROM climate_analysis
LIMIT 10;
SELECT
    city,
    ROUND(AVG(mean_temp), 2) AS avg_temperature
FROM climate_analysis
GROUP BY city
ORDER BY avg_temperature DESC;
SELECT
    city,
    MAX(max_temp) AS highest_temperature
FROM climate_analysis
GROUP BY city
ORDER BY highest_temperature DESC;
SELECT
    city,
    MIN(min_temp) AS lowest_temperature
FROM climate_analysis
GROUP BY city
ORDER BY lowest_temperature;
SELECT
    city,
    ROUND(AVG(humidity), 2) AS avg_humidity
FROM climate_analysis
GROUP BY city
ORDER BY avg_humidity DESC;
SELECT
    city,
    ROUND(SUM(precipitation), 2) AS total_rainfall
FROM climate_analysis
GROUP BY city
ORDER BY total_rainfall DESC;
SELECT
    city,
    COUNT(*) AS rainy_days
FROM climate_analysis
WHERE precipitation > 0
GROUP BY city
ORDER BY rainy_days DESC;
SELECT
    date,
    city,
    max_temp
FROM climate_analysis
ORDER BY max_temp DESC
LIMIT 1;
SELECT
    date,
    city,
    min_temp
FROM climate_analysis
ORDER BY min_temp
LIMIT 1;
SELECT
    date,
    city,
    max_temp,
    min_temp,
    temperature_range
FROM climate_analysis
ORDER BY temperature_range DESC
LIMIT 1;
SELECT
    YEAR(date) AS year,
    city,
    ROUND(AVG(mean_temp), 2) AS avg_temperature
FROM climate_analysis
GROUP BY YEAR(date), city
ORDER BY year, avg_temperature DESC;
SELECT
    MONTH(date) AS month,
    ROUND(AVG(mean_temp), 2) AS avg_temperature
FROM climate_analysis
GROUP BY MONTH(date)
ORDER BY month;
SELECT
    MONTH(date) AS month,
    ROUND(SUM(precipitation), 2) AS total_rainfall
FROM climate_analysis
GROUP BY MONTH(date)
ORDER BY month;
SELECT
    city,
    MONTH(date) AS month,
    ROUND(AVG(mean_temp), 2) AS avg_temperature,
    ROUND(AVG(humidity), 2) AS avg_humidity,
    ROUND(SUM(precipitation), 2) AS total_rainfall
FROM climate_analysis
GROUP BY city, MONTH(date)
ORDER BY city, month;