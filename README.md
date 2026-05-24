# Enterprise Identity Platform Demo

Quick start (local, requires Docker):

```bash
docker compose up --build
```

Backend health: http://localhost:8000/health

Demo auth (junior-level):
- Demo user: `demo` / `demo`
- Register a new user:

```bash
curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d '{"username":"demo","password":"demo"}'
```

Login to get JWT:

```bash
curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"demo","password":"demo"}'
```

The returned `access_token` is a demo JWT (HS256). Do NOT use this secret in production.
