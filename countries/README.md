## Schema
 * Country (**code**, name, capital, area)
 * Population (**country**, population, children, adult, birth_rate, death_rate, sex_ratio)
 * Economy (**country**, gdp, inflation, military, poverty_rate)
 * Language (**country, language**, percentage)

**Table Country:**
 * code (key)
 * name
 * capital
 * area

**Table Population:**
 * country (refers to country code)
 * population (total population)
 * children (percentage of children, defined as those aged 0 to 14)
 * adult (likewise for adults, defined as people between 15 and 64)
 * birth_rate
 * death_rate
 * sex_ratio (male/female)

**Table Economy:**
 * country (refers to country code)
 * gdp (gross domestic product)
 * inflation (annual inflation rate)
 * military (military spending as percentage of the gdp)
 * poverty_rate (percentage of population below the poverty line)

**Table Language:**
 * country (refers to country code)
 * language
 * percentage (percentage of population speaking the language)

**Constains:**
 * Code is a key for Country (name need not be a key)
 * Country is a key for Population adn Economy but not necessarily for Language

##Questions

**1. Find the percentage of elderly population (65 and over) int the country with the highest GDP.**
```sql
SELECT 100 - p.children - p.adult as eldery
FROM population p natural join economy e
where e.gdp = (SELECT MAX(gdp) from economy)
```
**2. Find the dominant language (dominant means: spoken by more than 50% of the population) of the country with the hightest male/female ratio. Same for the lowest ratio.**

```sql
SELECT l.language
FROM language l NATURAL JOIN population p1
WHERE l.percentage > 50 AND p1.sex_ratio = (SELECT MAX(p2.sex_ratio) FROM population p2)
```
```sql
SELECT l.language
FROM language l NATURAL JOIN population p1
WHERE l.percentage > 50 AND p1.sex_ratio = (SELECT MIN(p2.sex_ratio) FROM population p2)
```

**3. List 5 countries with the hightest military spending (not the percentage, but the actual spending), and for each of them list their capital and area.**
```sql
SELECT c.name, c.capital, c.area
FROM economy e JOIN country c ON e.country = c.code
ORDER BY e.military * e.gdp / 100 DESC
LIMIT 5
```

**4. Find the poverty rate in country/countries with the largest number of language spoken.**
```sql
SELECT l.country, e.poverty_rate
FROM language l NATURAL JOIN economy e
GROUP BY l.country
HAVING COUNT(*) = (SELECT MAX(count) FROM (SELECT COUNT(*) AS count FROM language l GROUP BY l.country))
```

**5. Find all countries where English is the dominant language, and the poverty rate is higher than that of Italy.**
```sql
SELECT l.country
FROM language l NATURAL JOIN economy e
WHERE l.language = 'English'AND l.percentage > 50
AND e.poverty_rate > (SELECT poverty_rate FROM economy WHERE country = 'IT')
```

**6. Find the country with the fastest declining population (that is the maximum death_rate - birth_rate).**
```sql
SELECT *
FROM population
ORDER BY death_rate - birth_rate DESC
LIMIT 1
```

**7. For each language, find the percentage of the world population that speaks it.**
```sql
SELECT l.language, SUM(p.population * l.percentage) / (SELECT SUM(population) FROM population) AS global_percentage
FROM language l NATURAL JOIN population p
GROUP BY l.language
```

Willo version:
```sql
SELECT language, SUM(tot) / (SELECT SUM(population) FROM population) AS global_percentage
FROM (SELECT l.language, l.percentage * p.population AS tot
      FROM language l NATURAL JOIN population p )
GROUP BY language
```

**8. Same as (7), but restricted to countries whose population is declining.**
```sql
SELECT l.language, (SUM(p.population * l.percentage) / ( SELECT SUM(population) 
											             FROM population
												         WHERE death_rate - birth_rate > 0)) AS declining_percentage
FROM language l NATURAL JOIN population p
WHERE p.death_rate - p.birth_rate > 0
GROUP BY l.language
```

**9. Consider the following hypothesis: the top 10 countries in terms of percentage of their elderly population are among the richest 20% (in terms of GDP per capita). Write an SQL query that checks if the hypotesis is true (if it is true, the ouput must contain those 10 countries).**
```sql
TODO
```

**10. The same for the hypothesis: 80% of the world population live in countries that are among the poorest 20%. The output should be 'yes' or 'no'.**
```sql
TODO
```

**11. List all the countries that belong to the top 10 in terms of both of the following criteria: the percentage of people in poverty and GDP per capita.**
```sql
SELECT *
FROM

/* top 10 by gdp */
(SELECT e.country
FROM economy e NATURAL JOIN population p
ORDER BY e.gdp / p.population DESC
LIMIT 10)

NATURAL JOIN

/* top 10 by poverty */
(SELECT e.country
FROM economy e
ORDER BY e.poverty_rate DESC
LIMIT 10)
```

**12. Assume that all the countries stop military spending, and distribuite the money back to their citizens. Find the average, maximum, and minimum increase of GDP per capita due to this action. For the minumum and maximum, also list the country (countries)**
```sql
/** max increase and countries **/
SELECT e.country, e.gdp * e.military / p.population / 100 AS increase
FROM economy e NATURAL JOIN population p
WHERE increase = ( SELECT MAX(gdp * military / population / 100) AS max_increase
				   FROM economy NATURAL JOIN population )
```
```sql
/** min increase and countries **/
SELECT e.country, e.gdp * e.military / p.population / 100 AS increase
FROM economy e NATURAL JOIN population p
WHERE increase = ( SELECT MIN(gdp * military / population / 100) AS min_increase
				   FROM economy NATURAL JOIN population )
```
```sql   
/** average **/
SELECT AVG(e.gdp * e.military / p.population / 100) AS average_increase
FROM economy e NATURAL JOIN population p
```

**13. Order languages by the average percentage of the adult population of countries in which they are spoken by at least 25% of the population (in decreasing order).**
```sql
SELECT l.language, AVG(p.adult) AS adult_average
FROM language l NATURAL JOIN population p
WHERE l.percentage > 25
GROUP BY l.language
ORDER BY AVG(p.adult) DESC
```

**14. Find the richest (highest GDP) , the poorest (lowest GDP), the most populus, and the largest country whose name starts with a 'C'.**

```sql
/** richest **/
SELECT e.country AS richest
FROM country c JOIN economy e ON c.code=e.country
WHERE c.name LIKE 'C%' AND e.gdp = ( SELECT MAX(e1.gdp)
									 FROM country c1 JOIN economy e1 ON c1.code=e1.country
									 WHERE c1.name LIKE 'C%' )
```
```sql
/** poorest **/
SELECT e.country AS poorest
FROM country c JOIN economy e ON c.code=e.country
WHERE c.name LIKE 'C%' AND e.gdp = ( SELECT MIN(e1.gdp)
									 FROM country c1 JOIN economy e1 ON c1.code=e1.country
									 WHERE c1.name LIKE 'C%' )
```
```sql
SELECT p.country AS most_populus
FROM country c JOIN population p ON c.code=p.country
WHERE c.name LIKE 'C%' AND p.population = ( SELECT p1.population
											FROM country c1 JOIN population p1 ON c1.code=p1.country
											WHERE c1.name LIKE 'C%' )
```

Assuming there is only one richest, one poorest and one most populus...
```sql
SELECT *
FROM

	/** richest **/
	(SELECT e.country AS richest
	FROM country c JOIN economy e ON c.code=e.country
	WHERE c.name LIKE 'C%'
	ORDER BY e.gdp DESC
	LIMIT 1),

	/** poorest **/
	(SELECT e.country AS poorest
	FROM country c JOIN economy e ON c.code=e.country
	WHERE c.name LIKE 'C%'
	ORDER BY e.gdp ASC
	LIMIT 1),

	/** most populus **/
	(SELECT p.country AS most_populus
	FROM country c JOIN population p ON c.code=p.country
	WHERE c.name LIKE 'C%'
	ORDER BY p.population DESC
	LIMIT 1)
```
