# 🗺️ ROADMAP DETALLADO - PASO A PASO

## 📋 TABLA DE CONTENIDOS

1. **FASE 1: Setup Inicial** (Pasos 1-5)
2. **FASE 2: OAuth2 Basic** (Pasos 6-10)
3. **FASE 3: OIDC/SSO** (Pasos 11-15)
4. **FASE 4: SAML** (Pasos 16-20)
5. **FASE 5: MFA** (Pasos 21-30)
6. **FASE 6: RBAC** (Pasos 31-35)
7. **FASE 7: Observabilidad** (Pasos 36-40)
8. **FASE 8: Producción** (Pasos 41-45)

---

# FASE 1: SETUP INICIAL 🏗️

## PASO 1: Estructura de carpetas y Git

### QUÉ hacemos:
Crear la estructura de directorios base del proyecto

### POR QUÉ:
- Separación de código (backend, frontend, infra, docs)
- Fácil navegación para otros developers
- Estándar industrial

### CÓMO:
```
/enterprise-iam-demo
├── backend/              ← FastAPI
├── frontend/             ← React
├── infra/                ← Docker, Nginx, SQL
├── docs/                 ← Documentación
├── .github/              ← GitHub workflows (CI/CD)
├── .gitignore
├── README.md
├── LICENSE
└── docker-compose.yml    ← Orquestación de servicios
```

### RESULTADO ESPERADO:
```bash
$ ls -la
drwxr-xr-x backend/
drwxr-xr-x frontend/
drwxr-xr-x infra/
drwxr-xr-x docs/
-rw-r--r-- docker-compose.yml
-rw-r--r-- README.md
```

---

## PASO 2: Backend - FastAPI Inicial

### QUÉ hacemos:
Configurar FastAPI con estructura base

### POR QUÉ:
- FastAPI = velocidad + type safety
- Pydantic = validación automática
- Documentación automática (Swagger)

### ESTRUCTURA:
```
backend/
├── main.py                  ← Punto de entrada
├── requirements.txt         ← Dependencias
├── .env.example             ← Variables de configuración
├── config.py                ← Configuración centralizada
├── auth/                    ← Módulo de autenticación
│   ├── __init__.py
│   └── dependencies.py      ← Validadores reutilizables
├── models/
│   ├── __init__.py
│   ├── user.py              ← User SQLAlchemy model
│   └── session.py           ← Session model
├── routes/
│   ├── __init__.py
│   ├── health.py            ← /health endpoint
│   └── protected.py         ← /api/protected (requiere auth)
├── utils/
│   ├── __init__.py
│   └── logger.py            ← Logging configurado
└── database.py              ← Conexión a PostgreSQL
```

### CÓDIGO EJEMPLO - main.py:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

app = FastAPI(
    title="Enterprise IAM Platform",
    version="1.0.0",
    docs_url="/docs"
)

# CORS para permitir frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check (simple)
@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### RESULTADO ESPERADO:
```bash
$ uvicorn main:app --reload
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000

# En navegador:
http://localhost:8000/docs → Swagger UI funcional
http://localhost:8000/health → {"status": "ok"}
```

---

## PASO 3: Frontend - React Inicial

### QUÉ hacemos:
Setup de React + estructura base

### POR QUÉ:
- React = componentes reutilizables
- Axios = HTTP client
- Protected routes = seguridad

### ESTRUCTURA:
```
frontend/
├── package.json
├── .env.example
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── index.js
│   ├── App.jsx
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   └── Protected.jsx
│   ├── components/
│   │   ├── Nav.jsx
│   │   └── ProtectedRoute.jsx
│   ├── services/
│   │   ├── api.js           ← Axios client
│   │   └── auth.js          ← Auth logic
│   ├── context/
│   │   └── AuthContext.jsx  ← Estado compartido
│   └── styles/
│       └── index.css
```

### CÓDIGO EJEMPLO - src/App.jsx:
```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Verificar si hay sesión activa
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/me');
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      setIsAuthenticated(false);
    }
  };

  return (
    <div className="App">
      <h1>Enterprise IAM Platform</h1>
      {isAuthenticated ? (
        <div>
          <p>Bienvenido, {user?.email}</p>
          <button onClick={() => window.location.href = '/logout'}>
            Logout
          </button>
        </div>
      ) : (
        <button onClick={() => window.location.href = 'http://localhost:8000/auth/login'}>
          Sign In
        </button>
      )}
    </div>
  );
}

export default App;
```

### RESULTADO ESPERADO:
```bash
$ npm start
Compiled successfully!
http://localhost:3000 → App visible
Botón "Sign In" funcional
```

---

## PASO 4: PostgreSQL + Docker Compose

### QUÉ hacemos:
Configurar base de datos y orquestación de contenedores

### POR QUÉ:
- PostgreSQL = ACID transactions (seguridad crítica en IAM)
- Docker Compose = mismo ambiente local = prod
- Facilita desarrollo en equipo

### ESTRUCTURA:
```
infra/
├── docker-compose.yml
├── postgres-init.sql        ← Tablas iniciales
└── nginx.conf               ← (aún no usamos)
```

### CÓDIGO - infra/docker-compose.yml:
```yaml
version: '3.9'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: iam-db
    environment:
      POSTGRES_USER: iam_user
      POSTGRES_PASSWORD: SecurePassword123!
      POSTGRES_DB: iam_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres-init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - iam-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U iam_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend FastAPI
  backend:
    build:
      context: ../backend
      dockerfile: Dockerfile
    container_name: iam-api
    environment:
      DATABASE_URL: postgresql://iam_user:SecurePassword123!@postgres:5432/iam_db
      OKTA_DOMAIN: ${OKTA_DOMAIN}
      OKTA_CLIENT_ID: ${OKTA_CLIENT_ID}
      OKTA_CLIENT_SECRET: ${OKTA_CLIENT_SECRET}
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - iam-network
    volumes:
      - ../backend:/app

  # Frontend React
  frontend:
    build:
      context: ../frontend
      dockerfile: Dockerfile
    container_name: iam-ui
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000
    networks:
      - iam-network
    volumes:
      - ../frontend:/app

volumes:
  postgres_data:

networks:
  iam-network:
    driver: bridge
```

### CÓDIGO - infra/postgres-init.sql:
```sql
-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    picture_url TEXT,
    okta_id VARCHAR(255) UNIQUE,  -- ID del usuario en Okta
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de sesiones
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de auditoría
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,  -- login, logout, mfa_verified, etc.
    ip_address VARCHAR(45),
    user_agent TEXT,
    status VARCHAR(50),            -- success, failed, etc.
    details JSONB,                 -- Datos adicionales en JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de MFA (TOTP)
CREATE TABLE mfa_totp (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    secret VARCHAR(255) NOT NULL,  -- Secreto TOTP encriptado
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de WebAuthn
CREATE TABLE mfa_webauthn (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    credential_id VARCHAR(255) NOT NULL UNIQUE,
    public_key TEXT NOT NULL,      -- Clave pública de WebAuthn
    sign_count INTEGER DEFAULT 0,
    transports TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_okta_id ON users(okta_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

### RESULTADO ESPERADO:
```bash
$ docker-compose up -d
Creating iam-db ... done
Creating iam-api ... done
Creating iam-ui ... done

# Verificar:
$ docker ps
CONTAINER ID   IMAGE          STATUS
abc123         postgres:15    Up 2 minutes (healthy)
def456         iam-api        Up 2 minutes
ghi789         iam-ui         Up 2 minutes

# Conectar a DB:
$ psql -U iam_user -h localhost -d iam_db
iam_db=# \dt
        List of relations
 users | table | iam_user
 sessions | table | iam_user
 audit_logs | table | iam_user
 ...
```

---

## PASO 5: .env y configuración centralizada

### QUÉ hacemos:
Centralizar variables de configuración (API keys, URLs, etc.)

### POR QUÉ:
- Seguridad: secrets NO en Git
- Flexibilidad: cambiar config sin editar código
- Reproducibilidad: mismas variables en local, dev, prod

### ESTRUCTURA:
```
.env.example          ← Plantilla (en Git)
.env                  ← Real (NO en Git)
.gitignore            ← Excluye .env
```

### CÓDIGO - .env.example:
```bash
# Backend
DATABASE_URL=postgresql://iam_user:password@localhost:5432/iam_db
JWT_SECRET=your-super-secret-key-change-in-production
API_HOST=http://localhost:8000
DEBUG=True

# Okta (SSO Provider)
OKTA_DOMAIN=https://your-okta-domain.okta.com
OKTA_CLIENT_ID=your_client_id
OKTA_CLIENT_SECRET=your_client_secret
OKTA_AUTH_SERVER_ID=default

# Auth0 (Alternative)
AUTH0_DOMAIN=your-auth0-domain.auth0.com
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_client_secret

# SAML
SAML_CERT_PATH=./certs/saml_cert.pem
SAML_KEY_PATH=./certs/saml_key.pem

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_ANALYTICS_ID=
```

### CÓDIGO - .gitignore:
```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Dependencies
node_modules/
__pycache__/
*.pyc
venv/

# IDE
.vscode/
.idea/
*.swp

# Logs
logs/
*.log

# Certificates
certs/*.pem
certs/*.key
!certs/.gitkeep

# OS
.DS_Store
Thumbs.db
```

### CÓMO USAR EN CÓDIGO:

**Backend (Python):**
```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
OKTA_DOMAIN = os.getenv("OKTA_DOMAIN")
```

**Frontend (React):**
```jsx
const API_URL = process.env.REACT_APP_API_URL;
```

### RESULTADO ESPERADO:
```bash
$ cat .env
DATABASE_URL=postgresql://...
JWT_SECRET=...
OKTA_DOMAIN=...

$ git status
.env (no listado porque está en .gitignore) ✓
```

---

## CONCLUSIÓN FASE 1

Al terminar **PASO 5**, tenemos:
- ✅ Estructura de carpetas clara
- ✅ Backend FastAPI funcional
- ✅ Frontend React funcional
- ✅ PostgreSQL en Docker
- ✅ Variables de configuración centralizadas
- ✅ Docker Compose orquestando todo

**Tiempo estimado:** 1-2 horas

**Siguiente:** FASE 2 - OAuth2 Basic

---

# FASE 2: OAUTH2 BÁSICO 🔐

*(Este es el siguiente, te lo explico en el siguiente documento)*

---

## NOTAS IMPORTANTES

### Testing del Setup:
```bash
# Terminal 1: Backend
$ cd backend && uvicorn main:app --reload

# Terminal 2: Frontend
$ cd frontend && npm start

# Terminal 3: Verificar BD
$ docker-compose exec postgres psql -U iam_user -d iam_db -c "\dt"

# Browser:
http://localhost:3000     ← Frontend
http://localhost:8000     ← Backend
http://localhost:8000/docs ← Swagger
```

### Troubleshooting:
| Problema | Solución |
|----------|----------|
| Puerto 5432 ocupado | `lsof -i :5432` + kill proceso |
| Módulo Python no encontrado | `pip install -r requirements.txt` |
| CORS error | Verificar `allow_origins` en FastAPI |
| React no compila | `npm install` + limpiar node_modules |

### Próximo paso:
Cuando termines los 5 pasos iniciales, avísame y pasamos a **FASE 2: OAuth2 Authorization Code Flow**

---

