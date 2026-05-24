# ⚡ QUICK REFERENCE - RESUMEN PARA REFERENCIA RÁPIDA

## 🎯 OBJETIVO DEL PROYECTO
Construir una **plataforma IAM real** (como Microsoft Entra ID, Okta, Auth0) que demuestre:
- Autenticación segura (OAuth2, OIDC, SAML)
- Multifactor (TOTP, WebAuthn)
- Autorización basada en roles (RBAC)
- Auditoría de seguridad

---

## 📊 COMPARATIVA: Conceptos clave

### OAuth2 vs OIDC vs SAML

```
┌─────────────────────────────────────────────────────────┐
│ OAUTH2: "¿Me dejas acceder a tus datos?"               │
│ • Autorización (permisos)                              │
│ • Acceso a APIs, recursos                              │
│ • Ejemplo: "Permiso para leer tu email"                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ OIDC: "¿Eres realmente tú?"                            │
│ • Autenticación (identidad)                            │
│ • Layer on top of OAuth2                               │
│ • Devuelve: ID Token + userData (claims)               │
│ • Ejemplo: Login con Google                            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ SAML: "Certifico que eres empleado de EMPRESA_A"       │
│ • Federación empresarial (legacy)                      │
│ • XML-based (más pesado)                               │
│ • Para grandes corporaciones                           │
│ • Ejemplo: Single Sign-On en gobierno, banca           │
└─────────────────────────────────────────────────────────┘
```

### MFA: TOTP vs WebAuthn

```
┌─────────────────────────────────────────────────────────┐
│ TOTP: Time-based One-Time Password                     │
│ • Algoritmo HMAC-SHA1 + Timestamp                      │
│ • 6 dígitos cada 30 segundos                           │
│ • Requiere: Google Authenticator, Authy                │
│ • Vulnerable: Phishing sigue siendo posible            │
│ • Setup: QR code con secreto                           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ WebAuthn/FIDO2: No hay secreto                         │
│ • Criptografía asimétrica (pública/privada)            │
│ • Privada NUNCA sale del dispositivo                   │
│ • Biometría o hardware key                             │
│ • RESISTENTE a phishing (verificaría dominio)          │
│ • Future: Passkeys (sin contraseña)                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 FLUJOS RESUMIDOS

### 1️⃣ OAuth2 Authorization Code Flow (BASE)

```
Usuario → "Login" → Backend /authorize → IdP
                    ↓ (usuario ingresa credenciales)
IdP → Backend /callback?code=xxx
Backend (secreto) → IdP /token (+ client_secret) → access_token
Backend → Frontend: "Cookie segura"
Frontend → Backend /protected: "Cookie" → "Acceso OK"
```

### 2️⃣ OIDC (SSO - Single Sign-On)

```
OAuth2 + ID Token + Claims (email, groups, roles)

Diferencia vs OAuth2:
- Response type: "code id_token" (vs solo "code")
- ID Token: JWT con datos del usuario
- Claims: Grupos, roles, permisos dentro del token
```

### 3️⃣ SAML 2.0 (Federación)

```
Usuario → "Login con SAML" → Backend /saml/login
Backend → Genera AuthnRequest (XML) → Redirige a IdP
Usuario → IdP (credenciales)
IdP → Backend /saml/acs (POST con SAML Response XML)
Backend → Valida firma XML → Extrae claims → Sesión local
```

### 4️⃣ TOTP (MFA)

```
Enroll:
1. Usuario: "Habilitar TOTP"
2. Backend: Genera secreto → QR code
3. Usuario: Escanea QR en Authenticator
4. Usuario: Verifica introduciendo código 6-dígitos
5. Backend: Confirma, guarda secreto encriptado

Login (con TOTP habilitado):
1. Usuario: Email + password
2. Backend: OK, pedir TOTP
3. Usuario: Abre Authenticator → introduce código
4. Backend: Valida HMAC-SHA1(secreto + timestamp)
5. Backend: Token de sesión
```

### 5️⃣ WebAuthn (MFA sin secreto)

```
Register:
1. Backend: Genera Challenge (bytes random)
2. Frontend: navigator.credentials.create() → Security Key/Biometría
3. Key: Genera clave pública/privada, firma challenge
4. Frontend: Envía public key + firma al backend
5. Backend: Verifica firma, guarda public key

Authenticate:
1. Backend: Genera Challenge
2. Frontend: navigator.credentials.get() → Toca key/fingerprint
3. Key: Firma challenge con private key
4. Backend: Verifica firma con public key guardada
5. ✅ Autenticado (sin contraseña)
```

---

## 📁 ESTRUCTURA FINAL (después de FASE 1)

```
enterprise-iam-demo/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── config.py
│   ├── database.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── oidc_flow.py
│   │   ├── oauth2_flow.py
│   │   ├── saml_flow.py
│   │   ├── mfa_totp.py
│   │   ├── mfa_webauthn.py
│   │   └── token_exchange.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── session.py
│   │   └── mfa.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── auth.py
│   │   └── protected.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── logs/
│   ├── Dockerfile
│   └── .dockerignore
│
├── frontend/
│   ├── package.json
│   ├── .env.example
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── index.js
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── MFA.jsx
│   │   │   └── Protected.jsx
│   │   ├── components/
│   │   │   ├── Nav.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   └── MFASetup.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── auth.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   └── styles/
│   │       └── index.css
│   ├── Dockerfile
│   └── .dockerignore
│
├── infra/
│   ├── docker-compose.yml
│   ├── nginx.conf
│   └── postgres-init.sql
│
├── docs/
│   ├── architecture.md
│   ├── sso_flows.md
│   ├── saml_setup.md
│   ├── mfa_design.md
│   └── troubleshooting.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── .env.example
├── README.md
├── docker-compose.yml
└── LICENSE
```

---

## 🔄 CICLO DE DESARROLLO TÍPICO

```
1. PLANIFICAR: ¿Qué haremos hoy?
   ↓
2. IMPLEMENTAR: Escribir código
   ↓
3. VERIFICAR: Checkpoints + testing local
   ↓
4. DOCUMENTAR: Explicar en docs/
   ↓
5. COMMIT: Git commit con mensaje claro
   ↓
6. SIGUIENTE: Próxima funcionalidad
```

---

## 🛡️ SEGURIDAD: Checklist

- [ ] Tokens en httpOnly cookies (no localStorage)
- [ ] CSRF tokens en formularios
- [ ] Rate limiting (anti-brute-force)
- [ ] HTTPS en producción
- [ ] Secretos en .env (nunca en código)
- [ ] Logs de auditoría (todos los eventos de auth)
- [ ] Validación de entrada (SQL injection, XSS)
- [ ] Refresh token rotation (token nuevo cada uso)
- [ ] CORS restringido (solo dominios permitidos)
- [ ] WebAuthn verification (resistente a phishing)

---

## 📚 TABLA DE REFERENCIA RÁPIDA

### Backend Endpoints (que crearemos)

| Endpoint | Método | Propósito | Auth requerida |
|----------|--------|-----------|----------------|
| `/health` | GET | Health check | ❌ |
| `/auth/login` | GET | Redirige a IdP | ❌ |
| `/auth/callback` | GET | IdP devuelve código | ❌ |
| `/auth/token` | POST | Intercambia código por token | ❌ |
| `/auth/logout` | POST | Limpia sesión | ✅ |
| `/auth/me` | GET | Datos del usuario actual | ✅ |
| `/api/protected` | GET | Ruta protegida (requiere RBAC) | ✅ |
| `/mfa/totp/enroll` | POST | Iniciar TOTP | ✅ |
| `/mfa/totp/verify` | POST | Verificar código TOTP | ✅ |
| `/mfa/webauthn/register/options` | GET | Opciones para registrar WebAuthn | ✅ |
| `/mfa/webauthn/register` | POST | Registrar WebAuthn | ✅ |
| `/audit/logs` | GET | Ver logs de auditoría | ✅ (admin) |

### Base de Datos

| Tabla | Propósito | Campos importantes |
|-------|----------|-------------------|
| `users` | Usuarios | id, email, okta_id, picture_url |
| `sessions` | Sesiones activas | id, user_id, access_token, refresh_token |
| `mfa_totp` | TOTP habilitado | user_id, secret |
| `mfa_webauthn` | WebAuthn registrado | user_id, credential_id, public_key |
| `audit_logs` | Auditoría | user_id, action, ip, status, details, timestamp |

---

## 🚀 TIMELINE ESTIMADO

| Fase | Pasos | Duración | Skills |
|------|-------|----------|--------|
| Setup | 1-5 | 1-2h | Docker, Git, Config |
| OAuth2 | 6-10 | 3-4h | OAuth2, JWT, FastAPI |
| OIDC | 11-15 | 2-3h | OIDC, Claims, Token validation |
| SAML | 16-20 | 3-4h | SAML, XML, Signatures |
| MFA | 21-30 | 4-5h | TOTP, WebAuthn, Cryptography |
| RBAC | 31-35 | 2-3h | Authorization, Groups |
| Observability | 36-40 | 2h | Logging, Auditing |
| Production | 41-45 | 2h | Hardening, CI/CD |

**TOTAL: ~25-30 horas de contenido práctico**

---

## 🎓 SKILLS QUE DESARROLLARÁS

```
CORE IAM:
✅ OAuth2/OIDC (authorization code flow)
✅ SAML 2.0 (XML, signatures)
✅ JWT (creation, validation, refresh)
✅ MFA (TOTP, WebAuthn/FIDO2)
✅ Cryptography (hashing, signing, encryption)

BACKEND:
✅ FastAPI (async, middleware)
✅ SQLAlchemy (ORM, migrations)
✅ Database design (audit logs, security)
✅ API security (CORS, CSRF, rate limiting)

FRONTEND:
✅ React (auth flows, protected routes)
✅ WebAuthn API (navigator.credentials)
✅ Secure storage (httpOnly cookies)
✅ QR code generation

INFRASTRUCTURE:
✅ Docker/Compose (containerization)
✅ PostgreSQL (ACID, JSON)
✅ Nginx (reverse proxy, SSL)
✅ CI/CD (GitHub Actions)

SECURITY:
✅ Threat modeling (OWASP Top 10)
✅ Auditing (compliance logging)
✅ Penetration testing mindset
✅ Key rotation, secret management
```

---

## ❓ FAQ RÁPIDO

**P: ¿Por qué FastAPI y no Django?**
R: FastAPI es más rápido (async nativo), menos boilerplate, ideal para OAuth2/OIDC.

**P: ¿Por qué separar TOTP y WebAuthn?**
R: Defensa en profundidad. Algunos usuarios pueden tener ambos, o elegir uno.

**P: ¿Por qué SAML si tenemos OAuth2/OIDC?**
R: SAML es requisito en grandes corporaciones (cumple normas antiguas).

**P: ¿Qué pasa si el IdP está caído?**
R: En este demo usamos tokens locales. En prod, usar refresh tokens + cache.

**P: ¿Cómo se manejan los refresh tokens?**
R: Token expira → Frontend solicita nuevo usando refresh_token → Backend valida y emite nuevo access_token.

**P: ¿Es seguro httpOnly cookies?**
R: Más seguro que localStorage (XSS no puede robar cookies con httpOnly).

---

## 🔗 RECURSOS RECOMENDADOS (después)

- RFC 6749 (OAuth 2.0): https://tools.ietf.org/html/rfc6749
- OIDC Spec: https://openid.net/specs/openid-connect-core-1_0.html
- SAML 2.0: https://oasis-open.org/
- WebAuthn: https://www.w3.org/TR/webauthn-2/
- OWASP Top 10: https://owasp.org/www-project-top-ten/

---

## 📍 ESTAMOS AQUÍ

```
Hoy: ANÁLISIS ← 🟢 TÚ ESTÁS AQUÍ
│
Mañana: PASO 1 (Setup)
│
Después: PASO 2 (OAuth2)
│
...
│
Semana 2-3: Proyecto completamente funcional
```

---

**Próximo paso:** Dime cuándo estés listo para PASO 1 ✅

