-- E-commerce Sales Analysis SQL Queries
-- Enhanced version with statistical measures and validation

-- 1. Total Sales by Region with Statistical Measures
SELECT 
    region,
    COUNT(*) as total_orders,
    SUM(total_price) as total_sales,
    AVG(total_price) as average_order_value,
    MIN(total_price) as min_order_value,
    MAX(total_price) as max_order_value,
    ROUND(SUM(total_price) * 100.0 / (SELECT SUM(total_price) FROM orders), 2) as revenue_percentage,
    COUNT(DISTINCT customer_id) as unique_customers
FROM orders
GROUP BY region
ORDER BY total_sales DESC;

-- 2. Product Category Revenue Analysis with Trends
SELECT 
    category,
    COUNT(*) as total_orders,
    SUM(total_price) as total_revenue,
    AVG(total_price) as average_price,
    COUNT(DISTINCT customer_id) as unique_customers,
    ROUND(AVG(quantity), 2) as avg_quantity_per_order,
    ROUND(SUM(total_price) * 100.0 / (SELECT SUM(total_price) FROM orders), 2) as revenue_percentage,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as order_percentage
FROM orders
WHERE category IS NOT NULL
GROUP BY category
ORDER BY total_revenue DESC;

-- 3. Shipping Analysis by Region with Cost Metrics
SELECT 
    region,
    COUNT(*) as total_orders,
    ROUND(AVG(shipping_fee), 2) as average_shipping_fee,
    MIN(shipping_fee) as min_shipping_fee,
    MAX(shipping_fee) as max_shipping_fee,
    ROUND(AVG(shipping_fee / total_price) * 100, 2) as avg_shipping_percentage,
    SUM(shipping_fee) as total_shipping_cost,
    ROUND(SUM(shipping_fee) * 100.0 / SUM(total_price), 2) as shipping_cost_ratio
FROM orders
GROUP BY region
ORDER BY average_shipping_fee DESC;

-- 4. Customer Age Impact Analysis with Detailed Metrics
WITH age_groups AS (
    SELECT 
        CASE 
            WHEN age < 25 THEN 'Under 25'
            WHEN age BETWEEN 25 AND 35 THEN '25-35'
            WHEN age BETWEEN 36 AND 45 THEN '36-45'
            WHEN age > 45 THEN 'Over 45'
        END as age_group,
        *
    FROM orders
)
SELECT 
    age_group,
    COUNT(*) as total_orders,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(total_price) as total_spent,
    ROUND(AVG(total_price), 2) as average_order_value,
    ROUND(SUM(total_price) / COUNT(DISTINCT customer_id), 2) as avg_customer_value,
    MAX(total_price) as highest_order_value,
    ROUND(AVG(quantity), 2) as avg_items_per_order,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as order_percentage
FROM age_groups
WHERE age_group IS NOT NULL
GROUP BY age_group
ORDER BY total_spent DESC;

-- 5. Product Category Analysis by Gender with Market Share
SELECT 
    gender,
    category,
    COUNT(*) as total_orders,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(total_price) as total_revenue,
    ROUND(AVG(total_price), 2) as average_order_value,
    ROUND(AVG(quantity), 2) as avg_quantity_per_order,
    ROUND(SUM(total_price) * 100.0 / SUM(SUM(total_price)) OVER (PARTITION BY category), 2) as category_market_share,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY category), 2) as category_order_share
FROM orders
WHERE gender IS NOT NULL AND category IS NOT NULL
GROUP BY gender, category
ORDER BY gender, total_revenue DESC;

-- 6. Order Fulfillment Analysis with Time Metrics
SELECT 
    shipping_status,
    COUNT(*) as total_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as percentage,
    COUNT(DISTINCT customer_id) as unique_customers,
    ROUND(AVG(total_price), 2) as average_order_value,
    SUM(total_price) as total_revenue,
    ROUND(AVG(shipping_fee), 2) as avg_shipping_fee
FROM orders
GROUP BY shipping_status
ORDER BY total_orders DESC;

-- 7. Monthly Sales Trends with Year-over-Year Growth
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', order_date) as month,
        COUNT(*) as total_orders,
        SUM(total_price) as total_revenue,
        AVG(total_price) as avg_order_value,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM orders
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT 
    month,
    total_orders,
    total_revenue,
    avg_order_value,
    unique_customers,
    ROUND((total_revenue - LAG(total_revenue, 1) OVER (ORDER BY month)) * 100.0 / 
        NULLIF(LAG(total_revenue, 1) OVER (ORDER BY month), 0), 2) as revenue_growth_pct
FROM monthly_sales
ORDER BY month;

-- 8. Customer Purchase Frequency Analysis
WITH customer_frequency AS (
    SELECT 
        customer_id,
        COUNT(*) as purchase_count,
        SUM(total_price) as total_spent,
        MIN(order_date) as first_purchase,
        MAX(order_date) as last_purchase,
        COUNT(DISTINCT strftime('%Y-%m', order_date)) as active_months
    FROM orders
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN purchase_count = 1 THEN 'One-time'
        WHEN purchase_count = 2 THEN 'Two-time'
        WHEN purchase_count <= 5 THEN 'Regular'
        ELSE 'Frequent'
    END as customer_type,
    COUNT(*) as customer_count,
    ROUND(AVG(total_spent), 2) as avg_customer_value,
    ROUND(AVG(purchase_count), 2) as avg_purchase_frequency,
    ROUND(AVG(active_months), 2) as avg_active_months
FROM customer_frequency
GROUP BY 
    CASE 
        WHEN purchase_count = 1 THEN 'One-time'
        WHEN purchase_count = 2 THEN 'Two-time'
        WHEN purchase_count <= 5 THEN 'Regular'
        ELSE 'Frequent'
    END
ORDER BY avg_customer_value DESC; 