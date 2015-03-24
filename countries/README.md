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
