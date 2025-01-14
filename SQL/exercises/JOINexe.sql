/*
Provide a table with the region for each sales_rep and associated accounts.
This time only for the Midwest region. 
Your final table should include three columns: the region name, the sales rep name, and the account name.
Sort the accounts alphabetically (A-Z) according to the account name.
*/

-- Solution
SELECT a.name AS NameAccount ,s.name AS Name_salesreps, r.name AS nameRegion
FROM accounts a
JOIN sales_reps s
ON a.sales_rep_id = s.id
JOIN region r
ON r.id=s.region_id
WHERE r.name = 'Midwest'
ORDER BY a.name 

/*
Provide a table that provides the region for each sales_rep along with their associated accounts.
This time only for accounts where the sales rep has a first name starting with S and in the Midwest region.
Your final table should include three columns: the region name, the sales rep name, and the account name.
Sort the accounts alphabetically (A-Z) according to the account name.  
*/
-- Solution
FROM region r
JOIN sales_reps s
ON s.region_id = r.id
JOIN accounts a
ON s.id = a.sales_rep_id
WHERE r.name = 'Midwest' AND s.name LIKE 'S%'
ORDER BY a.name;
/*
Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) for the order.
However, you should only provide the results if the standard order quantity exceeds 100. 
Your final table should have 3 columns: region name, account name, and unit price. 
In order to avoid a division by zero error, adding .01 to the denominator here is helpful total_amt_usd/(total+0.01).
*/
--Solution 
SELECT r.name region_name , a.name account_name , o.total_amt_usd/(o.total+0.01) unit_price
FROM region r
JOIN sales_reps s 
ON s.region_id=r.id
JOIN accounts a
ON s.id=a.sales_rep_id
JOIN orders o
ON o.account_id  =a.id 
WHERE standard_qty>100;
/*
What are the different channels used by account id 1001?
Your final table should have only 2 columns: account name and the different channels. 
You can try SELECT DISTINCT to narrow down the results to only the unique values.
*/
--Solution
SELECT DISTINCT a.name, w.channel
FROM accounts a
JOIN web_events w
ON a.id = w.account_id
WHERE a.id = '1001';

--Find all the orders that occurred in 2015. Your final table should have 4 columns: occurred_at, account name, order total, and order total_amt_usd.
SELECT o.occurred_at, a.name, o.total, o.total_amt_usd
FROM accounts a
JOIN orders o
ON o.account_id = a.id
WHERE o.occurred_at BETWEEN '01-01-2015' AND '01-01-2016'
ORDER BY o.occurred_at DESC;
