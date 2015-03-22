##Schema
 * Suppliers (**sid: integer**, sname: string, address: string)
 * Parts (**pid: integer**, pname: string, color: string)
 * Catalog (**sid: integer, pid: integer**, cost: real)

```sql
CREATE TABLE suppliers(
	sid INTEGER,
	sname VARCHAR(80),
	address VARCHAR(80), 
	PRIMARY KEY(sid)
);

CREATE TABLE parts (
	pid INTEGER, 
	pname VARCHAR(80), 
	color VARCHAR(80), 
	PRIMARY KEY (pid)
);

CREATE TABLE catalog (
	sid INTEGER, 
	pid INTEGER, 
	cost FLOAT, 
	PRIMARY KEY (sid, pid), 
	FOREIGN KEY(sid) REFERENCES suppliers (sid), 
	FOREIGN KEY(pid) REFERENCES parts (pid)
);
```

## Questions

**1. Find the names of suppliers who supply some red part**
``` sql
SELECT DISTINCT s.sname
FROM parts p NATURAL JOIN catalog c NATURAL JOIN suppliers s
WHERE p.color = 'red';
```

**2. Find the sids of suppliers who supply some red or green part**
``` sql
SELECT DISTINCT c.sid
FROM parts p NATURAL JOIN catalog c
WHERE p.color = 'red' OR p.color = 'green';
```

**3. Find the sids of suppliers who supply some red part or at Address X**
```sql
SELECT DISTINCT s.sid
FROM parts p NATURAL JOIN catalog c NATURAL JOIN suppliers s
WHERE p.color = 'red' OR s.address = 'Address X';
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
  WHERE p.color = 'green';
  ```
  
  * Using nested queries
  ``` sql
  SELECT DISTINCT c.sid
  FROM parts p NATURAL JOIN catalog c
  WHERE p.color = 'red' AND c.sid IN (SELECT c.sid
                                      FROM parts p NATURAL JOIN catalog c
                                      WHERE p.color = 'green');
  ```

**5. Find the sids of suppliers who supply every part**
```sql
SELECT DISTINCT c.sid
FROM catalog c
WHERE NOT EXISTS ( SELECT *
                   FROM parts p
                   WHERE NOT EXISTS ( SELECT *
                                      FROM catalog c1
                                      WHERE C1.sid = C.sid AND C1.pid = p.pid ));
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
                                    WHERE c.sid = c1.sid AND p.pid = c1.pid ))
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
                                    WHERE c.sid = c1.sid AND p.pid = c1.pid ));
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
                                    WHERE c.sid = c1.sid AND p.pid = c1.pid ));
OR NOT EXISTS ( SELECT *
                FROM parts p
                WHERE p.color = 'green'
                AND NOT EXISTS ( SELECT *
                                 FROM catalog c1
                                 WHERE c.sid = c1.sid AND p.pid = c1.pid ));
```
**9. Find pairs of sids such that the supplier with the first sid charges more for some part than the supplier with the second sid**
```sql
SELECT c1.sid AS sid1, c1.sid AS sid2
FROM catalog c1, catalog c1
WHERE c1.cost > c2.cost;
```

**10. Find the pids of parts supplied by at least two different suppliers**
```sql
SELECT DISTINCT c1.pid
FROM catalog c1
WHERE 2 <= ( SELECT COUNT(*)
             FROM catalog c2
             WHERE c2.pid = c1.pid );
```

**11. Find the pids of the most expensive parts supplied by suppliers named Yosemite Sham**
```sql
SELECT DISTINCT c.pid
FROM catalog c NATURAL JOIN suppliers s
WHERE s.sname='All red' AND c.cost = (SELECT MAX(c1.cost) FROM catalog c1);
```

**12. Find all fields of parts supplied by every supplier**
``` sql
SELECT *
FROM parts p
WHERE NOT EXISTS ( SELECT *
                   FROM suppliers s
                   WHERE NOT EXISTS ( SELECT *
                                      FROM catalog c
                                      WHERE c.pid = p.pid AND c.sid = s.sid ));
```

**13. Find the pids of parts supplied by every supplier at less then 100. (If any supplier either does not supply the part or charges more than 100 for it, the part is not selected.)**
``` sql
SELECT p.pid
FROM parts p
WHERE NOT EXISTS ( SELECT *
                   FROM suppliers s
                   WHERE NOT EXISTS ( SELECT *
                                      FROM catalog c
                                      WHERE c.pid = p.pid AND c.sid = s.sid AND c.cost < 100));
```
