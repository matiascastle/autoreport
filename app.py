"""
AutoReport - Generador Automático de Reportes
App interna para crear dashboards y enviar reportes profesionales a clientes.
"""

import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
import os
from datetime import datetime
from dotenv import load_dotenv

from utils.data_analyzer import DataAnalyzer
from utils.pdf_generator import PDFReportGenerator
from utils.client_manager import ClientManager, EmailSender

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="AutoReport - Dashboard Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'client_manager' not in st.session_state:
    st.session_state.client_manager = ClientManager()
if 'email_sender' not in st.session_state:
    st.session_state.email_sender = EmailSender()

# Header
st.markdown('<div class="main-header">📊 AutoReport</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Generador Automático de Reportes Profesionales</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1f77b4/ffffff?text=AutoReport", use_column_width=True)
    st.markdown("---")
    
    st.markdown("### 🎯 Workflow")
    st.markdown("""
    1. **Upload** - Sube CSV/Excel
    2. **Preview** - Revisa dashboard
    3. **Generate** - Crea PDF
    4. **Send** - Envía al cliente
    """)
    
    st.markdown("---")
    
    # Stats
    total_clients = len(st.session_state.client_manager.get_all_clients())
    st.metric("Total Clientes", total_clients)
    
    if st.session_state.df is not None:
        st.metric("Registros Cargados", len(st.session_state.df))

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📁 Upload Data", "📊 Preview Dashboard", "👥 Clientes", "⚙️ Settings"])

# ==================== TAB 1: Upload Data ====================
with tab1:
    st.header("Paso 1: Sube tus Datos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Formatos soportados:** CSV, Excel (XLSX)
        
        **Columnas detectadas automáticamente:**
        - 📅 Fechas (date, time, day, month, fecha)
        - 💰 Dinero (revenue, price, sales, cost, ingreso)
        - 📈 Cantidades (quantity, orders, count, pedidos)
        - 🏷️ Categorías (cualquier texto)
        """)
        
        uploaded_file = st.file_uploader(
            "Arrastra tu archivo o haz click para seleccionar",
            type=['csv', 'xlsx', 'xls'],
            help="El sistema detectará automáticamente las columnas y tipos de datos"
        )
        
        if uploaded_file is not None:
            try:
                # Load data
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state.df = df
                st.session_state.analyzer = DataAnalyzer(df)
                
                st.success(f"✅ Archivo cargado: {uploaded_file.name} ({len(df)} registros)")
                
                # Show preview
                with st.expander("👀 Ver datos (primeras 10 filas)"):
                    st.dataframe(df.head(10), use_container_width=True)
                
                # Show detected columns
                with st.expander("🔍 Columnas detectadas"):
                    detected = st.session_state.analyzer.detected_columns
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.markdown("**📅 Fechas:**")
                        if detected['dates']:
                            for col in detected['dates']:
                                st.markdown(f"- {col}")
                        else:
                            st.markdown("_Ninguna_")
                    
                    with col_b:
                        st.markdown("**💰 Numéricos:**")
                        if detected['numeric']:
                            for col in detected['numeric']:
                                col_type = detected['column_info'].get(col, 'number')
                                icon = "💰" if col_type == 'currency' else "📊"
                                st.markdown(f"{icon} {col}")
                        else:
                            st.markdown("_Ninguno_")
                    
                    with col_c:
                        st.markdown("**🏷️ Categorías:**")
                        if detected['categories']:
                            for col in detected['categories']:
                                st.markdown(f"- {col}")
                        else:
                            st.markdown("_Ninguna_")
                
            except Exception as e:
                st.error(f"❌ Error al cargar archivo: {e}")
    
    with col2:
        st.info("""
        **💡 Tips:**
        
        - Usa nombres descriptivos en columnas
        - Incluye fechas para ver tendencias
        - Revenue/Sales para métricas de dinero
        - Categorías para análisis de segmentos
        """)
        
        if st.session_state.df is not None:
            st.markdown("---")
            st.success("**Datos listos!**")
            st.markdown("Ve al tab **Preview Dashboard** →")

# ==================== TAB 2: Preview Dashboard ====================
with tab2:
    if st.session_state.df is None:
        st.warning("⚠️ Primero sube un archivo en el tab 'Upload Data'")
    else:
        st.header("Paso 2: Vista Previa del Dashboard")
        
        analyzer = st.session_state.analyzer
        metrics = analyzer.get_key_metrics()
        charts = analyzer.get_chart_data()
        insights = analyzer.get_insights()
        
        # Key Metrics
        st.subheader("📊 Métricas Clave")
        
        cols = st.columns(len(metrics))
        for i, (key, metric) in enumerate(metrics.items()):
            with cols[i]:
                value = metric['value']
                label = metric['label']
                format_type = metric.get('format', 'number')
                
                if format_type == 'currency':
                    display_value = f"${value:,.2f}"
                    delta_color = "normal"
                elif format_type == 'percentage':
                    display_value = f"{value:.1f}%"
                    delta_color = "inverse" if value < 0 else "normal"
                else:
                    display_value = f"{value:,.0f}"
                    delta_color = "normal"
                
                st.metric(
                    label=label,
                    value=display_value,
                    delta="↑ 12%" if i == 0 else None  # Simulated growth
                )
        
        st.markdown("---")
        
        # Charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("📈 Tendencia Temporal")
            
            if charts['line_chart']:
                line_data = charts['line_chart']
                
                option = {
                    "title": {"text": line_data['title'], "left": "center"},
                    "tooltip": {"trigger": "axis"},
                    "xAxis": {
                        "type": "category",
                        "data": line_data['x_data'],
                        "axisLabel": {"rotate": 45}
                    },
                    "yAxis": {"type": "value"},
                    "series": [{
                        "data": line_data['y_data'],
                        "type": "line",
                        "smooth": True,
                        "areaStyle": {"color": "rgba(31, 119, 180, 0.3)"},
                        "itemStyle": {"color": "#1f77b4"},
                        "lineStyle": {"width": 3}
                    }],
                    "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True}
                }
                
                st_echarts(options=option, height="400px")
            else:
                st.info("No hay datos de fecha disponibles para gráfico temporal")
        
        with chart_col2:
            st.subheader("🥧 Distribución por Categoría")
            
            if charts['pie_chart']:
                pie_data = charts['pie_chart']
                
                pie_chart_data = [
                    {"value": val, "name": label} 
                    for label, val in zip(pie_data['labels'][:10], pie_data['values'][:10])
                ]
                
                option = {
                    "title": {"text": pie_data['title'], "left": "center"},
                    "tooltip": {"trigger": "item", "formatter": "{b}: ${c} ({d}%)"},
                    "legend": {
                        "orient": "vertical",
                        "left": "left",
                        "top": "middle"
                    },
                    "series": [{
                        "type": "pie",
                        "radius": "60%",
                        "data": pie_chart_data,
                        "emphasis": {
                            "itemStyle": {
                                "shadowBlur": 10,
                                "shadowOffsetX": 0,
                                "shadowColor": "rgba(0, 0, 0, 0.5)"
                            }
                        }
                    }]
                }
                
                st_echarts(options=option, height="400px")
            else:
                st.info("No hay categorías disponibles para gráfico circular")
        
        st.markdown("---")
        
        # Bar Chart (if available)
        if charts['bar_chart']:
            st.subheader("📊 Top 10 Rendimiento")
            
            bar_data = charts['bar_chart']
            
            option = {
                "title": {"text": bar_data['title'], "left": "center"},
                "tooltip": {"trigger": "axis"},
                "xAxis": {
                    "type": "category",
                    "data": bar_data['x_data'],
                    "axisLabel": {"rotate": 45, "interval": 0}
                },
                "yAxis": {"type": "value"},
                "series": [{
                    "data": bar_data['y_data'],
                    "type": "bar",
                    "itemStyle": {
                        "color": {
                            "type": "linear",
                            "x": 0, "y": 0, "x2": 0, "y2": 1,
                            "colorStops": [
                                {"offset": 0, "color": "#667eea"},
                                {"offset": 1, "color": "#764ba2"}
                            ]
                        }
                    }
                }],
                "grid": {"left": "3%", "right": "4%", "bottom": "20%", "containLabel": True}
            }
            
            st_echarts(options=option, height="400px")
        
        st.markdown("---")
        
        # Insights
        st.subheader("💡 Insights Automáticos")
        
        insight_cols = st.columns(2)
        for i, insight in enumerate(insights):
            with insight_cols[i % 2]:
                st.info(insight)
        
        st.markdown("---")
        
        # Actions
        st.subheader("🚀 Acciones")
        
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            # Select client
            clients = st.session_state.client_manager.get_all_clients()
            
            if clients:
                client_options = {f"{c['name']} ({c['email']})": c['id'] for c in clients}
                selected_client_name = st.selectbox(
                    "Selecciona Cliente",
                    options=[""] + list(client_options.keys())
                )
                
                if selected_client_name:
                    selected_client_id = client_options[selected_client_name]
                    st.session_state.selected_client_id = selected_client_id
            else:
                st.warning("No hay clientes. Añade uno en el tab 'Clientes'")
                st.session_state.selected_client_id = None
        
        with action_col2:
            if st.button("📥 Generar PDF", type="primary", use_container_width=True):
                with st.spinner("Generando PDF profesional..."):
                    try:
                        # Get client name
                        client_name = "Demo Client"
                        if hasattr(st.session_state, 'selected_client_id') and st.session_state.selected_client_id:
                            client = st.session_state.client_manager.get_client(st.session_state.selected_client_id)
                            if client:
                                client_name = client['name']
                        
                        # Prepare data for PDF
                        pdf_data = {
                            'metrics': metrics,
                            'charts': charts,
                            'insights': insights
                        }
                        
                        # Generate PDF
                        output_path = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        generator = PDFReportGenerator(
                            client_name=client_name,
                            data=pdf_data,
                            output_path=output_path
                        )
                        
                        pdf_path = generator.generate()
                        
                        st.success(f"✅ PDF generado: {pdf_path}")
                        
                        # Download button
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button(
                                label="⬇️ Descargar PDF",
                                data=pdf_file,
                                file_name=output_path,
                                mime="application/pdf",
                                use_container_width=True
                            )
                        
                        # Save to client history
                        if hasattr(st.session_state, 'selected_client_id') and st.session_state.selected_client_id:
                            st.session_state.client_manager.add_report_to_client(
                                st.session_state.selected_client_id,
                                {'metrics': metrics, 'pdf_path': pdf_path}
                            )
                        
                    except Exception as e:
                        st.error(f"❌ Error generando PDF: {e}")
        
        with action_col3:
            if st.button("📧 Enviar por Email", type="secondary", use_container_width=True):
                if not hasattr(st.session_state, 'selected_client_id') or not st.session_state.selected_client_id:
                    st.error("❌ Selecciona un cliente primero")
                else:
                    with st.spinner("Enviando email..."):
                        try:
                            client = st.session_state.client_manager.get_client(st.session_state.selected_client_id)
                            
                            # Generate PDF first
                            pdf_data = {
                                'metrics': metrics,
                                'charts': charts,
                                'insights': insights
                            }
                            
                            output_path = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                            generator = PDFReportGenerator(
                                client_name=client['name'],
                                data=pdf_data,
                                output_path=output_path
                            )
                            
                            pdf_path = generator.generate()
                            
                            # Send email
                            success = st.session_state.email_sender.send_report(
                                to_email=client['email'],
                                client_name=client['name'],
                                pdf_path=pdf_path
                            )
                            
                            if success:
                                st.success(f"✅ Email enviado a {client['email']}")
                                
                                # Save to history
                                st.session_state.client_manager.add_report_to_client(
                                    st.session_state.selected_client_id,
                                    {'metrics': metrics, 'pdf_path': pdf_path}
                                )
                            else:
                                st.warning("⚠️ Email no configurado. Verifica SENDGRID_API_KEY en Settings")
                        
                        except Exception as e:
                            st.error(f"❌ Error enviando email: {e}")

# ==================== TAB 3: Clientes ====================
with tab3:
    st.header("Gestión de Clientes")
    
    # Add new client
    with st.expander("➕ Añadir Nuevo Cliente", expanded=False):
        with st.form("add_client_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Nombre *", placeholder="John Doe")
                new_email = st.text_input("Email *", placeholder="john@company.com")
            
            with col2:
                new_company = st.text_input("Empresa", placeholder="Acme Corp")
                new_color = st.color_picker("Color de marca", "#1f77b4")
            
            submitted = st.form_submit_button("Añadir Cliente", use_container_width=True)
            
            if submitted:
                if new_name and new_email:
                    client = st.session_state.client_manager.add_client(
                        name=new_name,
                        email=new_email,
                        company=new_company,
                        brand_color=new_color
                    )
                    st.success(f"✅ Cliente añadido: {new_name}")
                    st.rerun()
                else:
                    st.error("❌ Nombre y email son obligatorios")
    
    st.markdown("---")
    
    # List clients
    clients = st.session_state.client_manager.get_all_clients()
    
    if not clients:
        st.info("📭 No hay clientes aún. Añade uno arriba.")
    else:
        st.subheader(f"👥 Clientes ({len(clients)})")
        
        for client in clients:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.markdown(f"### {client['name']}")
                    st.markdown(f"📧 {client['email']}")
                
                with col2:
                    if client.get('company'):
                        st.markdown(f"🏢 {client['company']}")
                    
                    reports_count = len(client.get('reports', []))
                    st.markdown(f"📊 {reports_count} reportes enviados")
                
                with col3:
                    if st.button("📋 Histórico", key=f"hist_{client['id']}"):
                        st.session_state.show_history = client['id']
                
                with col4:
                    if st.button("🗑️", key=f"del_{client['id']}", help="Eliminar cliente"):
                        st.session_state.client_manager.delete_client(client['id'])
                        st.rerun()
                
                # Show history if selected
                if hasattr(st.session_state, 'show_history') and st.session_state.show_history == client['id']:
                    reports = client.get('reports', [])
                    
                    if reports:
                        st.markdown("**Histórico de Reportes:**")
                        for i, report in enumerate(reversed(reports[-5:])):  # Last 5
                            date = datetime.fromisoformat(report['date']).strftime("%Y-%m-%d %H:%M")
                            st.markdown(f"- {date}")
                    else:
                        st.info("Sin reportes aún")
                
                st.markdown("---")

# ==================== TAB 4: Settings ====================
with tab4:
    st.header("⚙️ Configuración")
    
    st.subheader("📧 Email Settings (SendGrid)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        api_key = st.text_input(
            "SendGrid API Key",
            value=os.getenv('SENDGRID_API_KEY', ''),
            type="password",
            help="Obtén tu API key en sendgrid.com"
        )
        
        from_email = st.text_input(
            "From Email",
            value=os.getenv('SENDGRID_FROM_EMAIL', 'reports@autoreport.io'),
            help="Email desde el que se enviarán los reportes"
        )
        
        if st.button("💾 Guardar Configuración"):
            # Save to .env file
            with open('.env', 'w') as f:
                f.write(f"SENDGRID_API_KEY={api_key}\n")
                f.write(f"SENDGRID_FROM_EMAIL={from_email}\n")
            
            st.success("✅ Configuración guardada")
            st.session_state.email_sender = EmailSender(api_key, from_email)
    
    with col2:
        st.markdown("**💡 Cómo configurar SendGrid:**")
        st.markdown("""
        1. Crea cuenta en [sendgrid.com](https://sendgrid.com)
        2. Ve a Settings → API Keys
        3. Crea nuevo API Key (Full Access)
        4. Copia y pega aquí
        5. Verifica tu dominio/email
        """)
        
        test_email = st.text_input("Email de prueba", placeholder="tu@email.com")
        
        if st.button("📨 Enviar Email de Prueba"):
            if test_email:
                success = st.session_state.email_sender.send_test_email(test_email)
                if success:
                    st.success(f"✅ Email de prueba enviado a {test_email}")
                else:
                    st.error("❌ Error. Verifica tu configuración.")
            else:
                st.warning("⚠️ Ingresa un email de prueba")
    
    st.markdown("---")
    
    st.subheader("📊 Estadísticas de Uso")
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        total_clients = len(st.session_state.client_manager.get_all_clients())
        st.metric("Total Clientes", total_clients)
    
    with stat_col2:
        total_reports = sum(
            len(c.get('reports', [])) 
            for c in st.session_state.client_manager.get_all_clients()
        )
        st.metric("Total Reportes Enviados", total_reports)
    
    with stat_col3:
        if st.session_state.df is not None:
            st.metric("Datos Cargados", "✅ Sí")
        else:
            st.metric("Datos Cargados", "❌ No")
    
    st.markdown("---")
    
    st.subheader("📚 Información")
    
    st.markdown("""
    **AutoReport v1.0**
    
    Generador automático de reportes profesionales con:
    - ✅ Detección automática de datos
    - ✅ Dashboards interactivos con ECharts
    - ✅ PDFs profesionales de 4 páginas
    - ✅ Envío automático por email
    - ✅ Gestión de clientes
    - ✅ Histórico de reportes
    
    ---
    
    **Tech Stack:**
    - Frontend: Streamlit
    - Charts: Apache ECharts
    - PDF: ReportLab
    - Email: SendGrid
    
    ---
    
    Made with ❤️ for efficient reporting
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'>"
    "AutoReport v1.0 | Made with Streamlit | © 2025"
    "</div>",
    unsafe_allow_html=True
)

