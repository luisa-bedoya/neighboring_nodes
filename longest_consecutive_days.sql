WITH consecutives_dates AS
(   SELECT  username,
            userdate,
            groupingset = DATEADD(DAY, 
                      -ROW_NUMBER() OVER(PARTITION BY username ORDER BY userdate), 
                      userdate)
    FROM  UserTable
)
SELECT  username,
        DATEDIFF(DAY, min(userdate), max(userdate)) +1 AS consecutive
INTO #consecutives_days
FROM    consecutives_dates
GROUP BY username, groupingset
ORDER BY username;

SELECT MAX(consecutive) AS consec, username 
FROM #consecutives_days 
GROUP BY username