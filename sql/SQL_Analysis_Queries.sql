-- E-commerce Sales Analysis SQL Queries
-- This file contains SQL queries for analyzing the E-commerce Sales dataset

-- 1. Total Sales by Region
SELECT 
    region,
    COUNT(*) as total_orders,
    SUM(total_price) as total_sales,
    AVG(total_price) as average_order_value
FROM orders
GROUP BY region
ORDER BY total_sales DESC;

-- 2. Product Category Revenue Analysis
SELECT 
    category,
    COUNT(*) as total_orders,
    SUM(total_price) as total_revenue,
    AVG(total_price) as average_price
FROM orders
GROUP BY category
ORDER BY total_revenue DESC;

-- 3. Average Shipping Fee by Region
SELECT 
    region,
    COUNT(*) as total_orders,
    AVG(shipping_fee) as average_shipping_fee,
    MIN(shipping_fee) as min_shipping_fee,
    MAX(shipping_fee) as max_shipping_fee
FROM orders
GROUP BY region
ORDER BY average_shipping_fee DESC;

-- 4. Customer Age Impact Analysis
SELECT 
    CASE 
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 35 THEN '25-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age > 45 THEN 'Over 45'
    END as age_group,
    COUNT(*) as total_orders,
    SUM(total_price) as total_spent,
    AVG(total_price) as average_order_value
FROM orders
GROUP BY 
    CASE 
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 35 THEN '25-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age > 45 THEN 'Over 45'
    END
ORDER BY total_spent DESC;

-- 5. Popular Products by Gender
SELECT 
    gender,
    category,
    COUNT(*) as total_orders,
    SUM(total_price) as total_revenue
FROM orders
GROUP BY gender, category
ORDER BY gender, total_revenue DESC;

-- 6. Order Fulfillment Analysis
SELECT 
    shipping_status,
    COUNT(*) as total_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as percentage
FROM orders
GROUP BY shipping_status
ORDER BY total_orders DESC;

-- 7. Shipping Status Trends Over Time
SELECT 
    strftime('%Y-%m', order_date) as month,
    shipping_status,
    COUNT(*) as total_orders
FROM orders
GROUP BY strftime('%Y-%m', order_date), shipping_status
ORDER BY month, shipping_status; 