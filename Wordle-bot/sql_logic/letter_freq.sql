cREATE TABLE letter_frequency (
	letter CHAR(1),
	score INT
)
GO

WITH letters AS (
	SELECT SUBSTRING(word, 1, 1) AS letter
	FROM words
	WHERE len(word) = 5
	UNION ALL
	SELECT SUBSTRING(word, 2, 1) AS letter
	FROM words
	WHERE len(word) = 5
	UNION ALL
	SELECT SUBSTRING(word, 3, 1) AS letter
	FROM words
	WHERE len(word) = 5
	UNION ALL
	SELECT SUBSTRING(word, 4, 1) AS letter
	FROM words
	WHERE len(word) = 5
	UNION ALL
	SELECT SUBSTRING(word, 5, 1) AS letter
	FROM words
	WHERE len(word) = 5
)

--INSERT INTO letter_frequency(letter, score)
SELECT letter, COUNT(letter) AS score
FROM letters
GROUP BY letter
ORDER BY score desc