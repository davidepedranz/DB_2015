##Questions

**1. Find the percentage of elderly population (65 and over) int the country with the highest GDP.**
```sql
SELECT 100 - p.children - p.adult as eldery
FROM population p natural join economy e
where e.gdp = (SELECT MAX(gdp) from economy)
```
**2. Find the dominant language (dominant means: spoken by more than 50% of the population) of the country with the hightest male/female ratio.**

```sql
SELECT l.language
FROM language l NATURAL JOIN population p1
WHERE l.percentage > 50 AND p1.sex_ratio = (SELECT MAX(p2.sex_ratio) FROM population p2)
```
