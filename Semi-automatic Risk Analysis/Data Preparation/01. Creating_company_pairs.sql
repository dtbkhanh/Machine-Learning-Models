/*------------------------------------------------------------------------------------------
------------------------------ 			Data cleansing 		------------------------------
------------------------------------------------------------------------------------------ */
SELECT * FROM FinancialDataset_raw ORDER BY company_id, dataset_year

SELECT COUNT(*) FROM FinancialDataset_raw -- 1728 rows

-- Check year column:
SELECT dataset_year, year_khanh FROM FinancialDataset_raw 
WHERE LENGTH(dataset_year) <> 4 -- AND dataset_year != '20,13'
ORDER BY company_id, dataset_year;

SELECT SUBSTR(dataset_year, 1, 4) FROM FinancialDataset_raw  WHERE LENGTH(dataset_year) > 4

# Cleaning dataset_year and put it into a new column:
ALTER TABLE FinancialDataset_raw ADD year_khanh varchar(100);

UPDATE FinancialDataset_raw  SET year_khanh = dataset_year WHERE LENGTH(dataset_year) = 4; -- 1654 rows

UPDATE FinancialDataset_raw SET year_khanh = SUBSTR(dataset_year, 1, 4) 
WHERE LENGTH(dataset_year) <> 4 AND dataset_year != '20,13'; -- 73 rows

UPDATE FinancialDataset_raw SET year_khanh = '2013' WHERE dataset_year = '20,13'; -- 1 row

# Remove duplicate values by choosing entries with the most recent dataset_id (max dataset_id)
# Put all desired column in a new table
-- DROP TABLE FinancialDataset
CREATE TABLE FinancialDataset
SELECT company_id, company_name, year_khanh, revenue, depreciation_amortization, operating_profit, interest_expense
FROM FinancialDataset_raw 
WHERE dataset_id = (
	SELECT MAX(dataset_id) FROM FinancialDataset_raw AS f 
	WHERE f.company_id= FinancialDataset_raw.company_id AND f.year_khanh = FinancialDataset_raw.year_khanh
)
ORDER BY company_id, year_khanh
-- Updated 1580 Rows	

-- Have a look
SELECT * FROM FinancialDataset

-- QC
SELECT COUNT(*) FROM FinancialDataset
SELECT * FROM FinancialDataset WHERE company_id = '1094' ORDER BY year_khanh


/*-----------------------------------------------------------------------------------------
--------------------------- 		 Creating company pairs		 --------------------------
------------------------------------------------------------------------------------------ */
-- 1/ Creating all possible company pairs with same years:
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
-- Updated 214844 Rows

-- Have a look
SELECT company_id_1, company_id_2, year_1 FROM Joined_Dataset ORDER BY company_id_1, company_id_2, year_1


-- 2/ Select only pairs with 2 mutual years and up:
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
-- Updated Rows	185708

-- Have a look
SELECT company_id_1, company_id_2, year_1 FROM Joined_Dataset_2 ORDER BY company_id_1, company_id_2, year_1


-- 3/ Createa list of all pairs with unique ID for each pair:
CREATE TABLE Pairs_list
SELECT company_id_1, company_id_2 FROM Joined_Dataset_2 GROUP BY company_id_1, company_id_2;

-- ALTER TABLE Pairs_list DROP COLUMN pair_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY;
ALTER TABLE Pairs_list ADD COLUMN pair_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY; -- Updated Rows 74340

-- Have a look
SELECT * FROM Pairs_list -- 74340 rows


-- 4/ Now Join with our Financial Dataset so that each pairs in the dataset will have an unique ID:
-- DROP TABLE Joined_Dataset_final
CREATE TABLE Joined_Dataset_final
SELECT b.pair_ID AS pair_id, a.*
FROM Joined_Dataset_2 AS a
JOIN Pairs_list AS b
ON a.company_id_1 = b.company_id_1 AND a.company_id_2 = b.company_id_2
-- Updated Rows	185708

ALTER TABLE Joined_Dataset_final ADD id MEDIUMINT NOT NULL AUTO_INCREMENT KEY -- add Primary Key
-- DROP TABLE Joined_Dataset
-- DROP TABLE Joined_Dataset_2

-- Have a look
SELECT * FROM Joined_Dataset_final ORDER BY pair_ID;
SELECT COUNT(DISTINCT(pair_id))from Joined_Dataset_final -- QC: 74340 pairs

-- 5/ Cluster company pairs into different groups with an unique ID, each group has 20 pairs:
SELECT * FROM Pairs_list -- We have 74340 pairs

-- Test with small sample dataset:
-- DROP TABLE sampleset 
CREATE TABLE sampleset SELECT * FROM Joined_Dataset_final ORDER BY RAND() LIMIT 200; 
SELECT * FROM sampleset

-- Relate to Python file "02. pairs_grouping.py" then have a look:
-- DROP TABLE Joined_Dataset_clustered
SELECT * FROM Joined_Dataset_clustered

-- QC
SELECT COUNT(1) FROM Joined_Dataset_clustered -- 185708 rows
SELECT MAX(cluster_id) FROM Joined_Dataset_clustered -- We have in total 3717 groups (74340/20 = 3717)

SELECT COUNT(DISTINCT(pair_id))from Joined_Dataset_clustered  -- 74340 pairs
