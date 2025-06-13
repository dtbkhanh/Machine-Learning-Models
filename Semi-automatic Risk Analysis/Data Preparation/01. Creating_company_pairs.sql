/*------------------------------------------------------------------------------------------
------------------------------   Section 1: Data Cleansing    ------------------------------
------------------------------------------------------------------------------------------ */

-- Step #1: Initial review of the raw financial data
-- Displays all records from the raw dataset, ordered by company ID and year.
SELECT * FROM FinancialDataset_raw ORDER BY company_id, dataset_year

-- Counts the total number of rows in the raw dataset.
SELECT COUNT(*) FROM FinancialDataset_raw -- 1728 rows

-- Step #2: Validate and clean the 'dataset_year' column
-- Identifies records where the 'dataset_year' column does not have a 4-character length,
-- indicating potential formatting issues.
SELECT dataset_year, year_khanh FROM FinancialDataset_raw 
WHERE LENGTH(dataset_year) <> 4 -- AND dataset_year != '20,13'
ORDER BY company_id, dataset_year;

-- Previews the first 4 characters of 'dataset_year' for entries longer than 4 characters.
SELECT SUBSTR(dataset_year, 1, 4) FROM FinancialDataset_raw  WHERE LENGTH(dataset_year) > 4

-- Adds a new column to store the cleaned year data.
-- Then updates it with 'dataset_year' for records that already have a valid 4-character year.
ALTER TABLE FinancialDataset_raw ADD year_khanh varchar(100);
UPDATE FinancialDataset_raw SET year_khanh = dataset_year WHERE LENGTH(dataset_year) = 4; -- 1654 rows

UPDATE FinancialDataset_raw SET year_khanh = SUBSTR(dataset_year, 1, 4) 
WHERE LENGTH(dataset_year) <> 4 AND dataset_year != '20,13'; -- 73 rows

-- Corrects the specific problematic entry '20,13' to '2013'.
UPDATE FinancialDataset_raw SET year_khanh = '2013' WHERE dataset_year = '20,13'; -- 1 row

-- Step #3: Remove duplicate values and create a clean FinancialDataset table
-- Creates a new table 'FinancialDataset' by selecting desired columns from the raw dataset.
-- Duplicates are removed by selecting the entry with the maximum 'dataset_id' for each
-- unique combination of 'company_id' and 'year_khanh'.

DROP TABLE FinancialDataset;

CREATE TABLE FinancialDataset
SELECT company_id, company_name, year_khanh, revenue, depreciation_amortization, operating_profit, interest_expense
FROM FinancialDataset_raw 
WHERE dataset_id = (
	SELECT MAX(dataset_id) FROM FinancialDataset_raw AS f 
	WHERE f.company_id= FinancialDataset_raw.company_id AND f.year_khanh = FinancialDataset_raw.year_khanh
)
ORDER BY company_id, year_khanh
-- Expected: 1580 rows updated

-- Review the newly created clean table.
SELECT * FROM FinancialDataset

-- Quality Check (QC): Verify row count and specific company data in the clean table.
SELECT COUNT(*) FROM FinancialDataset
SELECT * FROM FinancialDataset WHERE company_id = '1094' ORDER BY year_khanh


/*-----------------------------------------------------------------------------------------
--------------------------   Section 2: Creating Company Pairs   --------------------------
------------------------------------------------------------------------------------------ */
-- Step #4: Create all possible unique company pairs with mutual years
-- Self-joins the clean financial data to form unique pairs with mutual years.

-- DROP TABLE Joined_Dataset
CREATE TABLE Joined_Dataset
SELECT DISTINCT 
	a.company_id AS 'company_id_1'
	, a.company_name AS 'company_name_1'
	, a.year_khanh AS 'year_1'
	, a.revenue AS 'revenue_1'
	, a.depreciation_amortization AS 'depreciation_amortization_1'
	, a.operating_profit AS 'operating_profit_1'
	, a.interest_expense AS 'interest_expense_1'
	, b.company_id AS 'company_id_2'
	, b.company_name AS 'company_name_2'
	, b.year_khanh AS 'year_2'
	, b.revenue AS 'revenue_2'
	, b.depreciation_amortization AS 'depreciation_amortization_2'
	, b.operating_profit AS 'operating_profit_2'
	, b.interest_expense AS 'interest_expense_2'
FROM FinancialDataset a, FinancialDataset b 
WHERE a.company_id < b.company_id AND a.year_khanh = b.year_khanh
ORDER BY a.company_id, b.company_id, a.year_khanh, b.year_khanh 
-- Expected: 214844 rows updated

-- Review the initial joined dataset
SELECT company_id_1, company_id_2, year_1 FROM Joined_Dataset ORDER BY company_id_1, company_id_2, year_1


-- Step #5: Filter pairs to include only those with at least two mutual years
-- Refines the dataset to include pairs with sufficient overlapping historical data.

-- DROP TABLE Joined_Dataset_2
CREATE TABLE Joined_Dataset_2
SELECT d.* FROM Joined_Dataset AS d
INNER JOIN (
   SELECT company_id_1, company_id_2, COUNT(*)
   FROM Joined_Dataset 
   GROUP BY company_id_1, company_id_2
   HAVING COUNT(*) >= 2 
   ORDER BY company_id_1, company_id_2) t
ON d.company_id_1 = t.company_id_1 AND d.company_id_2 = t.company_id_2
ORDER BY d.company_id_1, d.company_id_2, d.year_1, d.year_2;
-- Expected: 185708 rows updated

-- Review the filtered joined dataset
SELECT company_id_1, company_id_2, year_1 FROM Joined_Dataset_2 ORDER BY company_id_1, company_id_2, year_1

-- Step #6: Create a unique list of all valid company pairs with an auto-incrementing ID
CREATE TABLE Pairs_list
SELECT company_id_1, company_id_2 FROM Joined_Dataset_2 GROUP BY company_id_1, company_id_2;

-- ALTER TABLE Pairs_list DROP COLUMN pair_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY;
ALTER TABLE Pairs_list ADD COLUMN pair_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY; -- Updated Rows 74340

-- Review the dataset
SELECT * FROM Pairs_list -- 74340 rows


-- Step #7: Join the pair IDs back to the main paired dataset
-- Integrates the unique 'pair_ID' into the final comprehensive dataset.

-- DROP TABLE Joined_Dataset_final
CREATE TABLE Joined_Dataset_final
SELECT b.pair_ID AS pair_id, a.*
FROM Joined_Dataset_2 AS a
JOIN Pairs_list AS b
ON a.company_id_1 = b.company_id_1 AND a.company_id_2 = b.company_id_2
-- Updated Rows	185708

ALTER TABLE Joined_Dataset_final ADD id MEDIUMINT NOT NULL AUTO_INCREMENT KEY -- add Primary Key

-- Review the dataset
SELECT * FROM Joined_Dataset_final ORDER BY pair_ID;
SELECT COUNT(DISTINCT(pair_id))from Joined_Dataset_final -- QC: 74340 pairs

-- Step #8: Prepare for external clustering (e.g., using Python)
-- Cluster company pairs into different groups with a unique ID, each group has 20 pairs:
SELECT * FROM Pairs_list -- We have 74340 pairs

-- Test with small sample dataset:
-- DROP TABLE sampleset 
CREATE TABLE sampleset SELECT * FROM Joined_Dataset_final ORDER BY RAND() LIMIT 200; 
SELECT * FROM sampleset

-- Relate to Python file "pairs_grouping.py" then have a look:
-- DROP TABLE Joined_Dataset_clustered
SELECT * FROM Joined_Dataset_clustered

-- Quality Check (QC)
SELECT COUNT(1) FROM Joined_Dataset_clustered -- 185708 rows
SELECT MAX(cluster_id) FROM Joined_Dataset_clustered -- We have in total 3717 groups (74340/20 = 3717)

SELECT COUNT(DISTINCT(pair_id))from Joined_Dataset_clustered  -- 74340 pairs
