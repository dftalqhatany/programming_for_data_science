--Provide a table with the region for each sales_rep and associated accounts.
--This time only for the Midwest region. 
--Your final table should include three columns: the region name, the sales rep name, and the account name.
--Sort the accounts alphabetically (A-Z) according to the account name.

SELECT a.name AS NameAccount ,s.name AS Name_salesreps, r.name AS nameRegion
FROM accounts a
JOIN sales_reps s
ON a.sales_rep_id = s.id
JOIN region r
ON r.id=s.region_id
WHERE r.name = 'Midwest'
ORDER BY a.name 
