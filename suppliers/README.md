#Schema
 * Suppliers (**sid: integer**, sname: string, address: string)
 * Parts (**pid: integer**, pname: string, color: string)
 * Catalog (**sid: integer, pid: integer**, cost: real)

# Questions

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

**5. Find the sids of suppliers who supply every part**
```sql
SELECT DISTINCT c.sid
FROM catalog c
WHERE NOT EXISTS ( SELECT *
                   FROM parts p
                   WHERE NOT EXISTS ( SELECT *
                                      FROM catalog c1
                                      WHERE C1.sid = C.sid AND C1.pid = p.pid ))
```

**6. Find the sids of suppliers who supply every red part**
```sql
SELECT DISTINCT c.sid
FROM catalog c
WHERE NOT EXISTS ( SELECT *
                   FROM parts p
                   WHERE p.color = 'red'
                   AND NOT EXISTS ( SELECT *
                                    FROM catalog c1
                                    WHERE C1.sid = C.sid AND C1.pid = p.pid ))
```

**7. Find the sids of suppliers who supply every red and every green part**
```sql
SELECT DISTINCT c.sid
FROM catalog c
WHERE NOT EXISTS ( SELECT *
                   FROM parts p
                   WHERE (p.color = 'red' OR p.color = 'green')
                   AND NOT EXISTS ( SELECT *
                                    FROM catalog c1
                                    WHERE C1.sid = C.sid AND C1.pid = p.pid ))
```

**8. Find the sids of suppliers who supply every red or supply every green part**
```sql
SELECT DISTINCT c.sid
FROM catalog c
WHERE NOT EXISTS ( SELECT *
                   FROM parts p
                   WHERE p.color = 'red'
                   AND NOT EXISTS ( SELECT *
                                    FROM catalog c1
                                    WHERE C1.sid = C.sid AND C1.pid = p.pid ))
OR NOT EXISTS ( SELECT *
                FROM parts p
                WHERE p.color = 'green'
                AND NOT EXISTS ( SELECT *
                                 FROM catalog c1
                                 WHERE C1.sid = C.sid AND C1.pid = p.pid ))
```
**9. Find pairs of sids such that the supplier with the first sid charges more for some part than the supplier with the second sid**
```sql
SELECT C1.sid AS sid1, C2.sid AS sid2
FROM catalog C1, catalog C2
WHERE C1.cost > C2.cost
```

**10. Find the pids of parts supplied by at least two different suppliers**
```sql
SELECT DISTINCT c.pid
FROM catalog c1
WHERE 2 <= ( SELECT COUNT(*)
             FROM catalog c2
             WHERE c2.pid = c1.pid )
```
