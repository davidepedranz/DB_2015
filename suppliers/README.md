**1. Find the names of suppliers who supply some red part**
``` sql
SELECT DISTINCT s.sname
FROM parts p NATURAL JOIN catalog c NATURAL JOIN suppliers s
WHERE p.color = 'red'
```

**2. Find the sids of suppliers who supply some red or green part**
``` sql
SELECT DISTINCT s.sid
FROM parts p NATURAL JOIN catalog c
WHERE p.color = 'red' OR p.color = 'green'
```

**3. Find the sids of suppliers who supply some red part or at Address X**
```sql
SELECT DISTINCT s.sid
FROM parts p NATURAL JOIN catalog c NATURAL JOIN suppliers s
WHERE p.color = 'red' OR s.adress = 'Address X', 
```

**4. Find the sids of suppliers who supply some red part and some green part**
  * Using INTERSECT
  ``` sql
  SELECT c.sid
  FROM parts p NATURAL JOIN catalog c
  WHERE p.color = 'red'
  
  INTERSECT
  
  SELECT c.sid
  FROM parts p NATURAL JOIN catalog c
  WHERE p.color = 'green'
  ```
  
  * Using nested queries
  ``` sql
  SELECT DISTINCT c.sid
  FROM parts p NATURAL JOIN catalog c
  WHERE p.color = 'red' AND c.sid IN (SELECT c.sid
                                      FROM parts p NATURAL JOIN catalog c
                                      WHERE p.color = 'green')
  ```
