SELECT company.company_id, company.company_name, company.company_city, foods.company_id, foods.item_name
FROM company
LEFT JOIN foods
ON company.company_id = foods.company_id;
