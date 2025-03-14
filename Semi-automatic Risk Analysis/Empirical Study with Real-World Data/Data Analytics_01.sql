USE KhanhDB2;
SELECT * FROM action_capture;

-- ========== Quality check ========== --
-- Check number of votes of each user:
SELECT user, COUNT(1) FROM action_capture GROUP BY user;

# Check for duplicated vote, i.e. if a user vote for the same pair more than once:
SELECT CONCAT(pair_id, "+", user), COUNT(*) FROM action_capture 
GROUP BY CONCAT(pair_id, "+", user)
HAVING COUNT(*) > 1

-- Now we see that user 4 has voted for pair_id = 6739 twice:
SELECT * FROM action_capture WHERE pair_id = 6739 AND user = 4; -- id = 123 or id = 124 

-- Check how many pairs get voted from all users (received all 4 votes): 
SELECT pair_id, COUNT(*) FROM action_capture
WHERE id != 123
GROUP BY pair_id HAVING COUNT(*) = 4
-- 105 pairs
-- SELECT * FROM action_capture WHERE pair_id= 6764;


-- ====== Check for overlaped decisions ======
-- *** 4 overlapping decisions:
SELECT DISTINCT a.*, b.company_name_voted, b.company_name_compared
FROM (
	WITH all_voted AS(
		-- Find pairs that get voted by all 4 users:
		SELECT pair_id, COUNT(*) FROM action_capture
		WHERE id != 123
		GROUP BY pair_id HAVING COUNT(*) = 4
	) SELECT all_voted.pair_id, t.sum_click
	FROM all_voted 
	INNER JOIN (
		SELECT pair_id, SUM(button1_clicked) AS sum_click 
		FROM action_capture AS a
		GROUP BY pair_id
		HAVING SUM(button1_clicked) = 4 OR SUM(button1_clicked) = 0
	) AS t
	ON all_voted.pair_id = t.pair_id
	) a
INNER JOIN action_capture AS b
ON a.pair_id = b.pair_id;
-- 55 overlaps


-- *** Exactly 3 overlapping decisions:
SELECT pair_id, COUNT(*) FROM action_capture
WHERE id != 123
GROUP BY pair_id HAVING COUNT(*) IN (3, 4); -- 152 pairs
			
-- Pairs that get voted by 4 users:
WITH all_voted AS(
	SELECT pair_id, COUNT(*) FROM action_capture
	WHERE id != 123
	GROUP BY pair_id HAVING COUNT(*) = 4
) SELECT all_voted.pair_id, t.sum_click
FROM all_voted 
INNER JOIN (
	SELECT pair_id, SUM(button1_clicked) AS sum_click 
	FROM action_capture AS a
	GROUP BY pair_id
	HAVING SUM(button1_clicked) = 3 OR SUM(button1_clicked) = 1
) AS t
ON all_voted.pair_id = t.pair_id
-- 41 pairs

-- Pairs that get voted by 3 users:
SELECT DISTINCT a.*, b.company_name_voted, b.company_name_compared
FROM (
	WITH all_voted AS(
		SELECT pair_id, COUNT(*) FROM action_capture
		WHERE id != 123
		GROUP BY pair_id HAVING COUNT(*) = 3
	) SELECT all_voted.pair_id, t.sum_click 
	FROM all_voted 
		INNER JOIN (
			SELECT pair_id, SUM(button1_clicked) AS sum_click 
			FROM action_capture AS a
			GROUP BY pair_id
			HAVING SUM(button1_clicked) = 3 OR SUM(button1_clicked) = 0
		) AS t
		ON all_voted.pair_id = t.pair_id
		) a
INNER JOIN action_capture AS b
ON a.pair_id = b.pair_id;
-- 29 pairs
-- Hence in total we have 29 + 41 = 70 pairs with exactly 3 votes overlap


-- *** At least 3 overlapping decisions:
-- Pairs that get voted by 4 users:
WITH all_voted AS(
	SELECT pair_id, COUNT(*) FROM action_capture
	WHERE id != 123
	GROUP BY pair_id HAVING COUNT(*) = 4
) SELECT all_voted.pair_id, t.sum_click
FROM all_voted 
INNER JOIN (
	SELECT pair_id, SUM(button1_clicked) AS sum_click 
	FROM action_capture AS a
	GROUP BY pair_id
	HAVING SUM(button1_clicked) >= 3 OR SUM(button1_clicked) IN (0, 1)
) AS t
ON all_voted.pair_id = t.pair_id
-- 96 votes
-- Hence in total we have 29 + 96 = 125 pairs with at least 3 votes overlap

SELECT * FROM action_capture WHERE pair_id = 2921;



-- ========== DATA DISTRIBUTION ========== --
SELECT * FROM Joined_Dataset_clustered 
WHERE cluster_id IN (1, 2, 3) AND pair_id != 193;

SELECT 
	revenue_1, depreciation_amortization_1, operating_profit_1, interest_expense_1
FROM Joined_Dataset_clustered WHERE cluster_id IN (1, 2, 3) AND pair_id != 193
UNION ALL 
SELECT 
	revenue_2, depreciation_amortization_2, operating_profit_2, interest_expense_2
FROM Joined_Dataset_clustered WHERE cluster_id IN (1, 2, 3) AND pair_id != 193;




