# ⚡ AutoReport - Quick Start (5 minutos)

Guía ultra-rápida para empezar a usar AutoReport.

---

## 🚀 Instalación (2 minutos)

```bash
# 1. Clona
git clone <tu-repo>
cd reportsauto

# 2. Instala
pip install -r requirements.txt

# 3. Corre
streamlit run app.py
```

**Abre**: http://localhost:8501

---

## 📊 Uso Básico (3 minutos)

### Paso 1: Upload Datos (30 segundos)

1. Tab **"Upload Data"**
2. Arrastra `examples/ecommerce_example.csv`
3. ✅ Datos cargados

### Paso 2: Ver Dashboard (1 minuto)

1. Tab **"Preview Dashboard"**
2. Verás automáticamente:
   - 📊 Métricas (Revenue, Orders, AOV, Growth)
   - 📈 Gráfico de tendencia temporal
   - 🥧 Gráfico por categorías
   - 💡 Insights automáticos

### Paso 3: Añadir Cliente (30 segundos)

1. Tab **"Clientes"**
2. Click **"➕ Añadir Nuevo Cliente"**
3. Llena:
   - Nombre: `Test Client`
   - Email: `tu@email.com`
4. Click **"Añadir Cliente"**

### Paso 4: Generar PDF (30 segundos)

1. Tab **"Preview Dashboard"**
2. Dropdown: Selecciona `Test Client`
3. Click **"📥 Generar PDF"**
4. Click **"⬇️ Descargar PDF"**
5. Abre el PDF → Verás reporte de 4 páginas profesional ✅

---

## 🎯 Resultado

En 3 minutos tienes:

- ✅ Dashboard interactivo
- ✅ PDF profesional de 4 páginas
- ✅ Cliente creado
- ✅ Sistema funcionando

---

## 📧 Bonus: Enviar Email (opcional)

Si quieres probar envío de emails:

### Setup SendGrid (2 minutos)

1. **Crear cuenta**: [sendgrid.com](https://sendgrid.com) (gratis)
2. **Obtener API Key**:
   - Settings → API Keys → Create API Key
   - Copiar el key
3. **Configurar en app**:
   - Tab "Settings"
   - Pegar API Key
   - Email: `reports@autoreport.io`
   - Click "Guardar"
4. **Test**:
   - Ingresa tu email
   - Click "Enviar Email de Prueba"
   - Checa inbox ✅

### Enviar Reporte

1. Tab "Preview Dashboard"
2. Selecciona cliente
3. Click **"📧 Enviar por Email"**
4. Cliente recibe email con PDF adjunto ✅

---

## 🎉 ¡Listo!

Ya sabes usar AutoReport. 

**Next Step**: Sube tus propios datos CSV y genera reportes reales.

---

## 💡 Tips Rápidos

### Mejores CSVs

```csv
date,revenue,orders,category
2025-01-01,1500,45,Electronics
2025-01-02,2000,60,Clothing
```

**Columnas que detecta automáticamente:**
- `date`, `time`, `month` → Fechas
- `revenue`, `sales`, `price` → Dinero
- `orders`, `quantity`, `count` → Cantidades
- Cualquier texto → Categorías

### Ejemplos Incluidos

```bash
examples/ecommerce_example.csv  # E-commerce
examples/saas_example.csv       # SaaS metrics
examples/retail_example.csv     # Retail stores
```

Prueba con estos para ver capacidades.

---

## 🐛 Problemas Comunes

**Error: Module not found**
```bash
pip install -r requirements.txt
```

**App no abre**
```bash
streamlit run app.py
# Abre manualmente: http://localhost:8501
```

**CSV no sube**
- Verifica que tenga headers (primera fila con nombres)
- Máximo 200MB

---

## 📚 Más Info

- **README.md** - Documentación completa
- **DEPLOY.md** - Deploy en la nube
- **examples/** - CSVs de ejemplo

---

**¿Preguntas?** Abre issue en GitHub.

Made with ❤️ | © 2025

