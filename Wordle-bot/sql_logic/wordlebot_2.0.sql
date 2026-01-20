CREATE PROCEDURE Wordlebot
	@green1 CHAR(1),
	@green2 CHAR(1),
	@green3 CHAR(1),
	@green4 CHAR(1),
	@green5 CHAR(1),
	@yellow1 NVARCHAR(25),
	@yellow2 NVARCHAR(25),
	@yellow3 NVARCHAR(25),
	@yellow4 NVARCHAR(25),
	@yellow5 NVARCHAR(25),
	@misses NVARCHAR(25)
AS
BEGIN
	DECLARE @included NVARCHAR(25) = CONCAT_WS(',', @yellow1, @yellow2, @yellow3, @yellow4, @yellow5);
	WITH scored_words AS (
		SELECT word,
			((SELECT score from letter_frequency WHERE letter = SUBSTRING(word, 1, 1)) + 
			(SELECT score from letter_frequency WHERE letter = SUBSTRING(word, 2, 1)) +
			(SELECT score from letter_frequency WHERE letter = SUBSTRING(word, 3, 1)) +
			(SELECT score from letter_frequency WHERE letter = SUBSTRING(word, 4, 1)) +
			(SELECT score from letter_frequency WHERE letter = SUBSTRING(word, 5, 1))) *
			(5 - (
				(SELECT len(word) - len(replace(word, SUBSTRING(word, 1, 1), '')) - 1) +
				(SELECT len(word) - len(replace(word, SUBSTRING(word, 2, 1), '')) - 1) +
				(SELECT len(word) - len(replace(word, SUBSTRING(word, 3, 1), '')) - 1) +
				(SELECT len(word) - len(replace(word, SUBSTRING(word, 4, 1), '')) - 1) +
				(SELECT len(word) - len(replace(word, SUBSTRING(word, 5, 1), '')) - 1)
			) / 2) / 5
		AS score
		FROM words
		WHERE len(word) = 5
	)

	SELECT TOP(1) word
	FROM scored_words
	WHERE (@green1 = '' OR @green1 = SUBSTRING(word, 1, 1))
		AND (@green2 = '' OR @green2 = SUBSTRING(word, 2, 1))
		AND (@green3 = '' OR @green3 = SUBSTRING(word, 3, 1))
		AND (@green4 = '' OR @green4 = SUBSTRING(word, 4, 1))
		AND (@green5 = '' OR @green5 = SUBSTRING(word, 5, 1))
		AND (SUBSTRING(word, 1, 1) NOT IN (SELECT VALUE FROM STRING_SPLIT(@yellow1, ',')))
		AND (SUBSTRING(word, 2, 1) NOT IN (SELECT VALUE FROM STRING_SPLIT(@yellow2, ',')))
		AND (SUBSTRING(word, 3, 1) NOT IN (SELECT VALUE FROM STRING_SPLIT(@yellow3, ',')))
		AND (SUBSTRING(word, 4, 1) NOT IN (SELECT VALUE FROM STRING_SPLIT(@yellow4, ',')))
		AND (SUBSTRING(word, 5, 1) NOT IN (SELECT VALUE FROM STRING_SPLIT(@yellow5, ',')))
		AND (@included = '' OR NOT EXISTS (SELECT 1 FROM STRING_SPLIT(@included, ',') WHERE VALUE != '' AND CHARINDEX(VALUE, word) = 0))
		AND (NOT EXISTS (SELECT 1 FROM STRING_SPLIT(@misses, ',') WHERE CHARINDEX(VALUE, word) > 0))
	ORDER BY score DESC
END;