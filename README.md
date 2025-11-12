# 📊 AutoReport - Generador Automático de Reportes

Aplicación interna para crear dashboards profesionales y enviar reportes automáticos a clientes.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache ECharts](https://img.shields.io/badge/Apache%20ECharts-AA344D?style=for-the-badge&logo=apache-echarts&logoColor=white)

## 🚀 Características

- ✅ **Detección Automática de Datos** - Interpreta CSV/Excel de cualquier empresa
- ✅ **Dashboards Interactivos** - Visualizaciones hermosas con Apache ECharts
- ✅ **PDFs Profesionales** - Reportes de 4 páginas listos para clientes
- ✅ **Envío Automático** - Email con PDF adjunto vía SendGrid
- ✅ **Gestión de Clientes** - CRM básico con histórico de reportes
- ✅ **100% Automático** - Sin configuración manual de gráficos

## 📦 Instalación Rápida

### Opción 1: Local (5 minutos)

```bash
# 1. Clona el repositorio
git clone <tu-repo>
cd reportsauto

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Corre la app
streamlit run app.py
```

Abre: http://localhost:8501

### Opción 2: Deploy en Streamlit Cloud (10 minutos)

1. **Push a GitHub**
```bash
git add .
git commit -m "AutoReport app"
git push
```

2. **Deploy en Streamlit Cloud**
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Selecciona tu repositorio
   - Main file: `app.py`
   - Click "Deploy"

3. **Listo!** Tu app estará en: `https://tu-username-autoreport.streamlit.app`

## 🎯 Cómo Usar

### Workflow Simple

```
1. Upload → Sube CSV/Excel
2. Preview → Revisa dashboard interactivo
3. Generate → Crea PDF profesional
4. Send → Envía al cliente por email
```

### Paso a Paso

#### 1️⃣ Upload Data

- Ve al tab **"Upload Data"**
- Arrastra tu CSV o Excel
- El sistema detecta automáticamente:
  - 📅 Fechas (date, time, month)
  - 💰 Revenue (revenue, sales, price)
  - 📊 Cantidades (orders, quantity)
  - 🏷️ Categorías (cualquier texto)

#### 2️⃣ Preview Dashboard

- Ve al tab **"Preview Dashboard"**
- Verás:
  - **Métricas clave** (Revenue, Orders, AOV, Growth)
  - **Gráfico de línea** (Tendencia temporal)
  - **Gráfico circular** (Distribución por categoría)
  - **Gráfico de barras** (Top 10 rendimiento)
  - **Insights automáticos**

#### 3️⃣ Generar PDF

- Selecciona un cliente del dropdown
- Click **"Generar PDF"**
- PDF de 4 páginas se genera automáticamente:
  1. **Executive Summary** - Métricas clave
  2. **Performance Deep Dive** - Análisis detallado
  3. **Trends & Insights** - Tendencias identificadas
  4. **Action Items** - Recomendaciones

#### 4️⃣ Enviar Email

- Click **"Enviar por Email"**
- Email profesional con PDF adjunto se envía al cliente
- Se guarda en histórico automáticamente

## 👥 Gestión de Clientes

### Añadir Cliente

1. Ve al tab **"Clientes"**
2. Click "➕ Añadir Nuevo Cliente"
3. Llena formulario:
   - Nombre (obligatorio)
   - Email (obligatorio)
   - Empresa (opcional)
   - Color de marca (opcional)
4. Click "Añadir Cliente"

### Ver Histórico

- Click "📋 Histórico" en cualquier cliente
- Ver últimos 5 reportes enviados
- Fechas y métricas guardadas

## ⚙️ Configuración Email (SendGrid)

### Setup Inicial

1. **Crea cuenta en SendGrid**
   - Ve a [sendgrid.com](https://sendgrid.com)
   - Sign up (plan gratuito: 100 emails/día)

2. **Obtén API Key**
   - Settings → API Keys
   - Create API Key (Full Access)
   - Copia el API key

3. **Configura en la App**
   - Ve al tab **"Settings"**
   - Pega tu API Key
   - Ingresa tu email (from)
   - Click "Guardar Configuración"

4. **Verifica Email**
   - SendGrid te enviará email de verificación
   - Click en link para verificar

5. **Test**
   - En Settings, ingresa email de prueba
   - Click "Enviar Email de Prueba"
   - Verifica que llegó

### Variables de Entorno (Opcional)

Crea archivo `.env`:

```bash
SENDGRID_API_KEY=tu_api_key_aqui
SENDGRID_FROM_EMAIL=reports@tudominio.com
```

## 📊 Ejemplos de Datos

Incluidos en carpeta `examples/`:

### 1. E-commerce (`ecommerce_example.csv`)

```csv
date,revenue,orders,product,category,customer
2025-01-01,1500.50,45,Laptop Pro,Electronics,John Doe
2025-01-02,2000.75,60,Smartphone X,Electronics,Jane Smith
...
```

**Detecta automáticamente:**
- Revenue total
- Órdenes
- AOV (Average Order Value)
- Tendencia por fecha
- Top categorías

### 2. SaaS (`saas_example.csv`)

```csv
month,mrr,churn_rate,new_customers,plan_type
2024-01,5000.00,0.05,10,Basic
2024-02,6500.00,0.03,15,Pro
...
```

**Detecta automáticamente:**
- MRR (Monthly Recurring Revenue)
- Churn rate
- New customers
- Growth trends
- Plan distribution

### 3. Retail (`retail_example.csv`)

```csv
date,store_name,total_sales,transactions,region
2025-01-01,Downtown Store,12500.50,145,North
2025-01-02,Mall Location,15200.75,180,South
...
```

**Detecta automáticamente:**
- Total sales
- Transactions
- Average ticket
- Top stores
- Regional performance

## 🎨 Personalización

### Cambiar Colores

En `app.py`, modifica el CSS:

```python
st.markdown("""
<style>
    .main-header {
        color: #TU_COLOR_AQUI;
    }
</style>
""", unsafe_allow_html=True)
```

### Personalizar PDF

En `utils/pdf_generator.py`, modifica:

- Colores: `colors.HexColor('#TU_COLOR')`
- Estilos de texto
- Layout de tablas
- Contenido de páginas

## 🛠️ Tech Stack

| Categoría | Tecnología | Propósito |
|-----------|------------|-----------|
| **Framework** | Streamlit | Interface web |
| **Charts** | Apache ECharts | Visualizaciones interactivas |
| **PDF** | ReportLab | Generación de PDFs |
| **Email** | SendGrid | Envío de emails |
| **Data** | Pandas | Procesamiento de datos |
| **Storage** | JSON | Almacenamiento simple de clientes |

## 📁 Estructura del Proyecto

```
reportsauto/
├── app.py                      # App principal de Streamlit
├── requirements.txt            # Dependencias Python
├── .streamlit/
│   └── config.toml            # Configuración de Streamlit
├── utils/
│   ├── __init__.py
│   ├── data_analyzer.py       # Detección automática de datos
│   ├── pdf_generator.py       # Generación de PDFs
│   └── client_manager.py      # Gestión de clientes y emails
├── examples/
│   ├── ecommerce_example.csv  # Ejemplo e-commerce
│   ├── saas_example.csv       # Ejemplo SaaS
│   └── retail_example.csv     # Ejemplo retail
├── clients_data.json          # Base de datos de clientes (auto-creado)
└── README.md                  # Este archivo
```

## 🚀 Deploy en Producción

### Streamlit Cloud (Recomendado)

**Ventajas:**
- ✅ Gratis
- ✅ Deploy en 5 minutos
- ✅ HTTPS automático
- ✅ Actualización automática con git push

**Pasos:**

1. Push a GitHub
2. Conecta en [share.streamlit.io](https://share.streamlit.io)
3. Añade secrets (Settings → Secrets):

```toml
SENDGRID_API_KEY = "tu_api_key"
SENDGRID_FROM_EMAIL = "reports@tudominio.com"
```

4. Deploy!

### Alternativas

#### Heroku

```bash
# Crea Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku create autoreport
git push heroku main
```

#### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD streamlit run app.py --server.port=8501
```

## 🔒 Seguridad

- ✅ API Keys en variables de entorno
- ✅ No hardcodear credenciales
- ✅ `.gitignore` configurado
- ⚠️ Para producción: añadir autenticación (Streamlit Auth)

## 📈 Roadmap

### v1.0 (Actual)
- ✅ Upload CSV/Excel
- ✅ Detección automática
- ✅ Dashboards ECharts
- ✅ PDFs de 4 páginas
- ✅ Email con SendGrid
- ✅ Gestión de clientes

### v1.1 (Próximo)
- ⏳ Autenticación (login/password)
- ⏳ Múltiples usuarios
- ⏳ Templates de PDF personalizables
- ⏳ Scheduler (reportes automáticos semanales)
- ⏳ Base de datos SQL (PostgreSQL)

### v2.0 (Futuro)
- ⏳ Integración con APIs (Shopify, Stripe, GA)
- ⏳ Dashboard público para clientes
- ⏳ Multi-tenant
- ⏳ Payments (Stripe)

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError"

```bash
pip install -r requirements.txt
```

### Email no se envía

1. Verifica API Key de SendGrid
2. Verifica email está verificado en SendGrid
3. Revisa límite de emails (100/día plan gratuito)
4. Checa spam folder

### PDF no se genera

1. Verifica permisos de escritura
2. Instala reportlab: `pip install reportlab`
3. Verifica datos están cargados

### CSV no se detecta

- Asegúrate columnas tienen nombres descriptivos
- Usa nombres en inglés (date, revenue, sales, etc.)
- O español (fecha, ingreso, ventas, etc.)

## 💡 Tips

### Mejores Prácticas

1. **Nombres de columnas descriptivos**
   - ✅ `revenue`, `sales_total`, `order_count`
   - ❌ `col1`, `data`, `x`

2. **Fechas en formato estándar**
   - ✅ `2025-01-01`, `01/01/2025`
   - ❌ `Jan 1`, `01-Ene`

3. **Categorías consistentes**
   - ✅ `Electronics`, `Furniture`
   - ❌ `electronics`, `FURNITURE`, `Furn`

4. **Números sin formato**
   - ✅ `1500.50` (el sistema añade $)
   - ❌ `$1,500.50`

## 🤝 Contribuir

1. Fork el repositorio
2. Crea branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m "Añade nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre Pull Request

## 📝 Licencia

MIT License - Usa libremente para proyectos personales o comerciales.

## 📞 Soporte

- 🐛 Reporta bugs en GitHub Issues
- 💬 Preguntas en Discussions
- 📧 Email: support@autoreport.io

---

## ⚡ Quick Start (TL;DR)

```bash
# 1. Instala
pip install -r requirements.txt

# 2. Corre
streamlit run app.py

# 3. Usa
# - Sube CSV en tab "Upload Data"
# - Ve dashboard en tab "Preview"
# - Añade cliente en tab "Clientes"
# - Configura email en tab "Settings"
# - Genera y envía PDF!
```

**Deploy en la nube:**

```bash
git push
# Ve a share.streamlit.io → Deploy
```

---

Made with ❤️ for efficient reporting | © 2025 AutoReport

