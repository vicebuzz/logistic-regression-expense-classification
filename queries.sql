
-- Queries for analysis and visualisation of user expenses

CREATE EXTENSION tablefunc;
SELECT * 
FROM crosstab(
	'SELECT SUM(amount), source, CONCAT(date_part("Month", date), "/", date_part("year", date))
	FROM public."AccountBalanceManagement"
	WHERE expenditure
	GROUP BY source, 3;'
) AS ct (date text, "Bills" int, "Transport" int, "Groceries" int, "Food" int, "Presents" int, "Entertainment" int, "Education" int, "Other" int);

SELECT SUM(amount), source, TO_CHAR(date, 'YYYY-MM')
FROM public."AccountBalanceManagement"
WHERE expenditure
GROUP BY source, 3
ORDER BY 3;

select distinct trim(both ' ' from source) from "AccountBalanceManagement" where expenditure order by 1

select distinct to_char(date, 'Month YYYY') from "AccountBalanceManagement"

SELECT 
  SUM(amount), 
  trim(both ' ' from source), 
  TO_CHAR(date, 'YYYY-MM') AS "Month"
FROM "AccountBalanceManagement" 
WHERE expenditure = true
GROUP BY 2,3
ORDER BY 3,2;