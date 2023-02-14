# Lottery
- Lottery CTF challenge
- Exploit lack of input validation for cache keys

## Build/Run Steps

- Creates three docker containers: 
	- Backend API
	- Frontend service
	- Redis cache
```
docker-compose build && docker-compose up  
```