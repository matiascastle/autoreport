# 🚀 Guía de Deploy - AutoReport

Guía paso a paso para deployar AutoReport en la nube SIN Docker ni localhost.

## 🎯 Opción Más Fácil: Streamlit Cloud (RECOMENDADO)

### ⏱️ Tiempo: 10 minutos
### 💰 Costo: GRATIS

---

## Paso 1: Preparar el Repositorio

### 1.1 Inicializar Git (si no está hecho)

```bash
cd /Users/matias/reportsauto

# Inicializar git
git init

# Añadir todos los archivos
git add .

# Primer commit
git commit -m "Initial commit - AutoReport app"
```

### 1.2 Crear Repositorio en GitHub

**Opción A: Desde la terminal (con GitHub CLI)**

```bash
# Instalar GitHub CLI (si no lo tienes)
brew install gh

# Login
gh auth login

# Crear repo
gh repo create autoreport --public --source=. --remote=origin --push
```

**Opción B: Manual**

1. Ve a [github.com/new](https://github.com/new)
2. Nombre: `autoreport`
3. Public
4. NO inicializar con README (ya lo tienes)
5. Click "Create repository"
6. Conecta tu repo local:

```bash
git remote add origin https://github.com/TU_USERNAME/autoreport.git
git branch -M main
git push -u origin main
```

---

## Paso 2: Deploy en Streamlit Cloud

### 2.1 Crear Cuenta en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign up"** (o "Continue with GitHub")
3. Autoriza Streamlit a acceder a GitHub
4. Acepta términos

### 2.2 Deploy la App

1. Click **"New app"** (botón azul)
2. Completa el formulario:
   - **Repository**: `TU_USERNAME/autoreport`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (custom): `autoreport` (o lo que quieras)
3. Click **"Deploy!"**

### 2.3 Esperar Deploy

- Toma 2-5 minutos la primera vez
- Verás logs de instalación
- Cuando termine: ✅ "Your app is live!"

### 2.4 Tu URL

```
https://TU_USERNAME-autoreport.streamlit.app
```

O si elegiste custom URL:

```
https://autoreport.streamlit.app
```

---

## Paso 3: Configurar Secrets (Email)

### 3.1 En Streamlit Cloud

1. En tu app deployada, click **"⚙️ Settings"** (arriba derecha)
2. Click **"Secrets"** (menú lateral)
3. Añade tus secrets:

```toml
SENDGRID_API_KEY = "SG.xxxxxxxxxxxx"
SENDGRID_FROM_EMAIL = "reports@tudominio.com"
```

4. Click **"Save"**
5. La app se reiniciará automáticamente

### 3.2 Obtener SendGrid API Key

1. **Crear cuenta en SendGrid**
   - Ve a [sendgrid.com/pricing](https://sendgrid.com/pricing)
   - Click "Try for Free"
   - Plan gratuito: 100 emails/día (suficiente para empezar)

2. **Verificar email**
   - SendGrid enviará email de verificación
   - Click en link

3. **Crear Sender Identity**
   - Settings → Sender Authentication
   - Verify Single Sender
   - Completa formulario con tu email
   - Verifica email nuevamente

4. **Obtener API Key**
   - Settings → API Keys
   - Click "Create API Key"
   - Name: `AutoReport Production`
   - Permission: **Full Access**
   - Click "Create & View"
   - **COPIA EL API KEY** (solo se muestra una vez)
   - Pega en Streamlit Secrets

5. **Test**
   - Ve a tu app
   - Tab "Settings"
   - "Enviar Email de Prueba"
   - Verifica inbox

---

## Paso 4: Actualizar la App

Cada vez que hagas cambios:

```bash
# 1. Haz tus cambios en el código

# 2. Commit
git add .
git commit -m "Descripción de cambios"

# 3. Push
git push

# 4. La app se actualiza AUTOMÁTICAMENTE en 1-2 minutos
```

**No necesitas hacer nada más.** Streamlit Cloud detecta el push y redeploya automáticamente.

---

## 🎉 ¡Listo!

Tu app está en la nube, accesible desde cualquier lugar:

```
https://TU_USERNAME-autoreport.streamlit.app
```

### Workflow Final

```
1. Abre la URL de tu app en el navegador
2. Upload CSV
3. Preview dashboard
4. Genera PDF
5. Envía a cliente por email
6. ¡Hecho! Sin localhost, sin Docker, sin complicaciones
```

---

## 🔒 Seguridad

### Contraseña Básica (Opcional)

Si quieres proteger la app con contraseña simple:

**1. Añade en secrets:**

```toml
PASSWORD = "tu_password_seguro_123"
```

**2. Añade al inicio de `app.py`:**

```python
import streamlit as st
import os

# Simple password protection
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        if password == os.getenv("PASSWORD"):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Password incorrecto")
    st.stop()

# Tu app continúa aquí...
```

**3. Push:**

```bash
git add app.py
git commit -m "Añade autenticación"
git push
```

---

## 🛠️ Troubleshooting

### App no inicia

**Error común**: Module not found

**Solución**: Verifica que `requirements.txt` esté en la raíz del proyecto

```bash
ls requirements.txt  # Debe existir
```

### Email no funciona

1. Verifica API Key en Secrets
2. Verifica email verificado en SendGrid
3. Revisa que no estés en límite (100 emails/día free)

### CSV no sube

- Límite de upload: 200MB (configurable en `.streamlit/config.toml`)
- Si necesitas más: actualiza `maxUploadSize`

### Cambios no se reflejan

- Espera 1-2 minutos
- Force refresh: Ctrl+Shift+R (Windows) o Cmd+Shift+R (Mac)
- Revisa logs en Streamlit Cloud → Manage app → Logs

---

## 📊 Monitoreo

### Ver Logs en Tiempo Real

1. Streamlit Cloud → Tu app → **"Manage app"**
2. Click **"Logs"**
3. Ver logs en tiempo real

### Métricas de Uso

- Streamlit Cloud muestra:
  - Viewers activos
  - CPU usage
  - Memory usage
  - Requests

---

## 💰 Costos

### Plan Gratuito (Actual)

- ✅ Hosting: **GRATIS**
- ✅ HTTPS: **GRATIS**
- ✅ Recursos: 1 GB RAM (suficiente)
- ✅ Emails: **100/día GRATIS** (SendGrid)

### Cuando Crezcas

#### Streamlit Cloud Pro ($20/mes)

- 3 apps privadas
- Más recursos
- Priority support

#### SendGrid Essentials ($15/mes)

- 50,000 emails/mes
- Email validation
- Analytics

**Total: $35/mes para escalar**

Pero con plan gratuito puedes manejar fácilmente:

- 10-20 clientes
- 100 reportes/mes
- Sin costo

---

## 🚀 Alternativas de Deploy (Más avanzado)

### Opción 2: Heroku

```bash
# 1. Instalar Heroku CLI
brew install heroku/brew/heroku

# 2. Login
heroku login

# 3. Crear Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# 4. Crear app
heroku create autoreport-app

# 5. Deploy
git push heroku main

# 6. Añadir secrets
heroku config:set SENDGRID_API_KEY=tu_api_key
heroku config:set SENDGRID_FROM_EMAIL=tu_email

# 7. Abrir
heroku open
```

**Costo**: $7/mes (Eco Dyno)

### Opción 3: Railway

1. [railway.app](https://railway.app) → New Project
2. Deploy from GitHub repo
3. Añade variables de entorno
4. Listo

**Costo**: $5/mes

---

## 📝 Checklist Final

Antes de compartir tu app con clientes:

- [ ] App deployada y accesible públicamente
- [ ] SendGrid configurado y emails funcionando
- [ ] Probado con CSV de ejemplo
- [ ] PDF se genera correctamente
- [ ] Email llega a cliente
- [ ] Clientes añadidos
- [ ] Opcional: Password protection activado
- [ ] URL personalizada (si quieres)

---

## 🎯 Next Steps

Una vez deployado:

1. **Añade tus primeros clientes** en el tab Clientes
2. **Sube datos reales** y prueba el workflow completo
3. **Envía tu primer reporte** a un cliente test
4. **Comparte la URL** (si la usas para interno, no compartas)
5. **Itera**: mejora basado en feedback

---

Made with ❤️ for easy deployment | © 2025

