/*
Q1:Find the total amount of poster_qty paper ordered in the orders table.
Q2:Find the total amount of standard_qty paper ordered in the orders table.
Q3:Find the total dollar amount of sales using the total_amt_usd in the orders table.
Q4:Find the total amount spent on standard_amt_usd and gloss_amt_usd paper for each order in the orders table. This should give a dollar amount for each order in the table.
Q5:Find the standard_amt_usd per unit of standard_qty paper. Your solution should use both aggregation and a mathematical operator.
*/
--Find the total amount of poster_qty paper ordered in the orders table.
SELECT SUM(poster_qty) AS total_poster_sales
FROM orders;
ORDER BY num_accounts ;
--Find the total amount of standard_qty paper ordered in the orders table.
SELECT SUM(standard_qty) AS total_standard_sales
FROM orders;
--Find the total dollar amount of sales using the total_amt_usd in the orders table.
SELECT SUM(total_amt_usd) AS total_dollar_sales
FROM orders;
--Find the total amount for each individual order that was spent on standard and gloss paper in the orders table.
--This should give a dollar amount for each order in the table. Notice, this solution did not use an aggregate.
SELECT standard_amt_usd + gloss_amt_usd AS total_standard_gloss
FROM orders;
--Though the price/standard_qty paper varies from one order to the next.
--I would like this ratio across all of the sales made in the orders table.
--Notice, this solution used both an aggregate and our mathematical operators

SELECT SUM(standard_amt_usd)/SUM(standard_qty) AS standard_price_per_unit
FROM orders;How many of the sales reps have more than 5 accounts that they manage?

--How many of the sales reps have more than 5 accounts that they manage?

-- Soltion 
SELECT s.id, s.name, COUNT(*) num_accounts
FROM accounts a
JOIN sales_reps s
ON s.id = a.sales_rep_id
GROUP BY s.id, s.name
HAVING COUNT(*) > 5
ORDER BY num_accounts;

--Write a query to display for each order, the account ID, the total amount of the order, 
--and the level of the order - ‘Large’ or ’Small’ - depending on if the order is $3000 or more, or smaller than $3000.

-- Soltion 
SELECT account_id ID ,total_amt_usd Total_order ,
CASE 
WHEN total_amt_usd >3000 THEN 'Large'
WHEN total_amt_usd <3000 THEN 'Small' 
END AS Level 
FROM orders;
