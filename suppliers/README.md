**1. Find the names of suppliers who supply some red part**

``` sql
SELECT DISTINCT  S.sname
FROM parts p NATURAL JOIN catalog c NATURAL JOIN suppliers s
WHERE p.color = 'red'
```

**2. Find the sids of suppliers who supply some red or green part**

``` sql
SELECT DISTINCT C.sid
FROM parts p NATURAL JOIN catalog c
WHERE p.color = 'red' OR p.color = 'green'
```
