import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, time
import numpy as np

# Configuración de página mejorada
st.set_page_config(
    page_title="⚡ BKT - Monitoreo Eléctrico",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función de autenticación
def check_authentication():
    """Verifica si el usuario está autenticado"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated

def login_screen():
    """Pantalla de login"""
    # Crear columnas para centrar el formulario
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        
        
        st.markdown("### 🔐 **Acceso Autorizado**")
        st.markdown("---")
        
        # Formulario de login
        with st.form("login_form"):
            usuario = st.text_input("👤 Usuario:", placeholder="Ingresa tu usuario")
            password = st.text_input("🔑 Contraseña:", type="password", placeholder="Ingresa tu contraseña")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                submit_button = st.form_submit_button("🚀 Ingresar", use_container_width=True)
        
        if submit_button:
            if usuario == "admin" and password == "12345678":
                st.session_state.authenticated = True
                st.success("✅ ¡Acceso autorizado! Redirigiendo...")
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
                st.warning("⚠️ Contacta al administrador si tienes problemas de acceso")
        
        st.markdown("</div>", unsafe_allow_html=True)

def logout():
    """Función para cerrar sesión"""
    st.session_state.authenticated = False
    st.rerun()

# Verificar autenticación al inicio
if not check_authentication():
    login_screen()
    st.stop()

# CSS personalizado para una apariencia profesional
st.markdown("""
<style>
    /* --- THEME VARIABLES --- */
    :root {
        --primary-color: #2563eb; /* Blue 600 */
        --primary-color-darker: #1d4ed8; /* Blue 700 */
        --sidebar-bg: #0f172a; /* Slate 900 */
        --app-bg: #f1f5f9; /* Slate 100 */
        --widget-bg: #ffffff; /* White */
        --text-main: #0f172a; /* Slate 900 */
        --text-light: #f1f5f9; /* Slate 100 */
        --text-secondary: #475569; /* Slate 600 */
        --border-color: #cbd5e1; /* Slate 300 */
    }

    /* --- GENERAL APP STYLING --- */
    .stApp {
        background-color: var(--app-bg);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: var(--text-main);
    }
    
    /* --- HEADER --- */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-color-darker) 100%);
        padding: 2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: var(--text-light);
        text-align: center;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.2);
    }
    .main-header h1 {
        margin: 0 0 0.5rem 0;
        font-size: 2.2rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color);
    }
    [data-testid="stSidebar"] h3 {
        color: var(--text-light) !important;
        font-weight: 600;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: var(--text-light) !important;
        opacity: 0.8;
    }
    [data-testid="stFileUploader"] {
        border-color: var(--primary-color);
    }
    
    /* --- CUSTOM HTML METRIC CONTAINERS --- */
    .metric-container {
        background-color: var(--widget-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease-in-out;
        border-left: 5px solid var(--primary-color);
        margin: 1rem 0;
    }
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        border-color: var(--primary-color);
    }
    .metric-container h4 {
        color: var(--primary-color);
        margin-top: 0;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .metric-container p {
        margin: 0.5rem 0;
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 0.95rem;
    }
    .metric-container p strong {
        color: var(--text-main);
    }

    /* --- STREAMLIT METRIC CONTAINERS (st.metric) --- */
    [data-testid="metric-container"] {
        background-color: var(--widget-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease-in-out;
        border-left: 5px solid var(--primary-color);
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        border-color: var(--primary-color);
    }
    [data-testid="metric-container"] label {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--text-main) !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    [data-testid="metric-container"] [data-testid="metric-delta"] {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }

    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 2px solid var(--border-color);
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: var(--text-secondary);
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        border: none;
        padding: 0.75rem 1.25rem;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e2e8f0; /* Slate 200 */
        color: var(--text-main);
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: var(--primary-color) !important;
        border-bottom: 3px solid var(--primary-color) !important;
        box-shadow: none;
    }

    /* --- HEADINGS & TEXT --- */
    .stMarkdown h2 {
        color: var(--text-main);
        font-weight: 600;
        border-bottom: 2px solid var(--border-color);
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }

    /* --- ALERTS & INFO BOXES --- */
    .alert-success, .alert-warning, .alert-danger, .stInfo, .stSuccess, .stWarning {
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-weight: 500;
        border: 1px solid;
        border-left-width: 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .alert-success, .stSuccess {
        background-color: #f0fdf4 !important; /* Green 50 */
        color: #14532d !important; /* Green 900 */
        border-color: #4ade80 !important; /* Green 400 */
    }
    .alert-warning, .stWarning {
        background-color: #fffbeb !important; /* Yellow 50 */
        color: #78350f !important; /* Yellow 900 */
        border-color: #facc15 !important; /* Yellow 400 */
    }
    .alert-danger {
        background-color: #fef2f2 !important; /* Red 50 */
        color: #7f1d1d !important; /* Red 900 */
        border-color: #f87171 !important; /* Red 400 */
    }
    .stInfo {
        background-color: #eff6ff !important; /* Blue 50 */
        color: #1e3a8a !important; /* Blue 900 */
        border-color: #60a5fa !important; /* Blue 400 */
    }

    /* --- WIDGETS --- */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-color-darker) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.3);
    }
      /* --- HIDE STREAMLIT DEFAULTS --- */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Oculta botón inferior derecho de Streamlit Cloud */
    .viewerBadge_container__1QSob {display: none !important;}
    
    /* Oculta botón de menú superior derecho (tres puntos) */
    .st-emotion-cache-1avcm0n.ezrtsby0 {display: none !important;}
    
    /* --- SPACING --- */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Cargar y procesar datos
@st.cache_data
def cargar_datos(uploaded_file):
    """Carga y procesa los datos del CSV subido por el usuario"""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, skiprows=1)
        df.rename(columns={"Date  hh:mm:ss": "datetime_str"}, inplace=True)
        df["datetime"] = pd.to_datetime(df["datetime_str"])
        # Agregar columnas calculadas
        df["hora"] = df["datetime"].dt.hour
        df["minuto"] = df["datetime"].dt.minute
        
        # Clasificar períodos del día laboral (9:00-18:00 con comida 14:00-15:00)
        def clasificar_periodo(row):
            hora = row["hora"]
            if 9 <= hora < 14:
                return "🌅 Mañana (9:00-14:00)"
            elif hora == 14:
                return "🍽️ Hora de Comida (14:00-15:00)"
            elif 15 <= hora < 18:
                return "🌆 Tarde (15:00-18:00)"
            else:
                return "⏰ Fuera de Horario"
        
        df["periodo"] = df.apply(clasificar_periodo, axis=1)
        
        return df
    return None

# Configuración de máquinas
maquinas_config = {
    "BRN01": {
        "nombre": "Dobladora Hidráulica",
        "icono": "🔧",
        "color": "#FF6B6B",
        "potencia_col": "BRN01 W TOT-AVG",
        "energia_col": "BRN01 kWh+ SUM TOT"
    },
    "BRN02": {
        "nombre": "CNC Plasma",
        "icono": "⚙️",
        "color": "#4ECDC4",
        "potencia_col": "BRN02 W TOT-AVG",
        "energia_col": "BRN02 kWh+ SUM TOT"
    },
    "BRN03": {
        "nombre": "Soldadoras",
        "icono": "⚡",
        "color": "#45B7D1",
        "potencia_col": "BRN03 W TOT-AVG",
        "energia_col": "BRN03 kWh+ SUM TOT"
    }
}

# Header principal mejorado
st.markdown("""
<div class="main-header">
    <h1>⚡ BKT MOBILIARIO - DASHBOARD ELÉCTRICO</h1>
    <p>Monitoreo en tiempo real del consumo energético de equipos industriales</p>
</div>
""", unsafe_allow_html=True)

# Sidebar mejorado
st.sidebar.markdown("### 👤 **Usuario Autenticado**")
st.sidebar.success("🟢 admin")

# Botón de cerrar sesión
if st.sidebar.button("🚪 Cerrar Sesión", type="secondary", use_container_width=True):
    logout()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📁 **Cargar Datos**")
st.sidebar.markdown("---")

# File uploader
uploaded_file = st.sidebar.file_uploader(
    "📄 Sube tu archivo CSV",
    type=['csv'],
    help="Selecciona el archivo CSV exportado por el equipo Lovato DMG9000"
)

# Cargar datos
df = cargar_datos(uploaded_file)

if df is not None:
    st.sidebar.success("✅ Archivo cargado correctamente")
    
    # Mostrar información básica del archivo
    st.sidebar.markdown("### 📊 **Información del Archivo**")
    st.sidebar.info(f"""
    - **Registros:** {len(df):,}
    - **Período:** {df['datetime'].min().strftime('%Y-%m-%d %H:%M')} 
      hasta {df['datetime'].max().strftime('%Y-%m-%d %H:%M')}
    - **Días:** {df['datetime'].dt.date.nunique()}
    """)
    
    st.sidebar.markdown("### 📅 **Configuración**")
    st.sidebar.markdown("---")

    # Filtros de fecha
    fechas_unicas = sorted(df["datetime"].dt.date.unique())
    fecha_seleccionada = st.sidebar.selectbox(
        "📅 Selecciona una fecha:", 
        fechas_unicas, 
        index=len(fechas_unicas) - 1,
        help="Elige la fecha para visualizar los datos"
    )

    df_filtrado = df[df["datetime"].dt.date == fecha_seleccionada]

    # Configuración de tarifa
    st.sidebar.markdown("### 💰 **Configuración de Costos**")
    costo_kwh = st.sidebar.number_input(
        "💲 Tarifa por kWh (MXN):",
        min_value=0.1,
        max_value=10.0,
        value=2.5,
        step=0.1,
        help="Tarifa eléctrica en pesos mexicanos por kWh"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ **Información**")
    st.sidebar.info(
        "💡 **Tip:** Utiliza los filtros para analizar períodos específicos y optimizar el consumo energético."
    )
else:
    st.info("👆 **Por favor, sube un archivo CSV para comenzar el análisis**")
    st.markdown("""
    ### 📋 **Instrucciones:**
    1. Usa el selector de archivos en la barra lateral
    2. Sube el archivo CSV exportado por tu equipo Lovato DMG9000
    3. El dashboard se actualizará automáticamente con tus datos
    
    ### 📄 **Formato esperado:**
    - Archivo CSV con datos de potencia y energía
    - Columnas de tiempo en formato "Date hh:mm:ss"
    - Datos de las máquinas BRN01, BRN02, BRN03
    """)
    st.stop()

# Función para crear gráficos mejorados
def crear_grafico_potencia(df_data, maquina_id, config):
    """Crea un gráfico de potencia mejorado para una máquina"""
    fig = go.Figure()
    
    # Agregar línea principal
    fig.add_trace(go.Scatter(
        x=df_data["datetime"],
        y=df_data[config["potencia_col"]],
        mode='lines+markers',
        name=f'{config["icono"]} {config["nombre"]}',
        line=dict(color=config["color"], width=3),
        marker=dict(size=4),
        hovertemplate='<b>%{fullData.name}</b><br>' +
                     'Fecha: %{x}<br>' +
                     'Potencia: %{y:.1f} W<br>' +
                     '<extra></extra>'
    ))
    
    # Agregar línea de promedio
    promedio = df_data[config["potencia_col"]].mean()
    fig.add_hline(
        y=promedio, 
        line_dash="dash", 
        line_color="gray",
        annotation_text=f"Promedio: {promedio:.1f}W"
    )
    
    # Definir el rango completo del día laboral (9:00-18:00)
    fecha_base = df_data["datetime"].dt.date.iloc[0]
    hora_inicio = pd.Timestamp.combine(fecha_base, pd.Timestamp("09:00:00").time())
    hora_fin = pd.Timestamp.combine(fecha_base, pd.Timestamp("18:00:00").time())
    
    # Configurar layout
    fig.update_layout(
        title=dict(
            text=f'{config["icono"]} <b>{config["nombre"]}</b>',
            font=dict(size=16, color="darkblue"),
            x=0.1
        ),
        xaxis_title="Hora",
        yaxis_title="Potencia (W)",
        hovermode='x unified',
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            gridcolor='lightgray',
            gridwidth=1,
            title_font=dict(size=12),
            range=[hora_inicio, hora_fin],  # Mostrar todo el día laboral
            dtick=3600000,  # Marcas cada hora (en milisegundos)
            tickformat='%H:%M'  # Formato de hora
        ),
        yaxis=dict(
            gridcolor='lightgray',
            gridwidth=1,
            title_font=dict(size=12)
        )
    )
    
    return fig

def calcular_metricas_maquina(df_data, config):
    """Calcula métricas para una máquina"""
    if df_data.empty:
        return {
            "potencia_actual": 0,
            "potencia_max": 0,
            "potencia_promedio": 0,
            "energia_consumida": 0,
            "estado": "Sin datos"
        }
    
    potencia_actual = df_data[config["potencia_col"]].iloc[-1]
    potencia_max = df_data[config["potencia_col"]].max()
    potencia_promedio = df_data[config["potencia_col"]].mean()
    
    # Calcular energía consumida en el período
    energia_inicial = df_data[config["energia_col"]].iloc[0]
    energia_final = df_data[config["energia_col"]].iloc[-1]
    energia_consumida = energia_final - energia_inicial
    
    # Determinar estado de la máquina
    if potencia_actual < 100:
        estado = "🟢 Inactiva"
    elif potencia_actual < potencia_promedio * 0.5:
        estado = "🟡 Baja carga"
    elif potencia_actual < potencia_promedio * 1.5:
        estado = "🟠 Carga normal"
    else:
        estado = "🔴 Alta carga"
    
    return {
        "potencia_actual": potencia_actual,
        "potencia_max": potencia_max,
        "potencia_promedio": potencia_promedio,
        "energia_consumida": energia_consumida,
        "estado": estado
    }

# Resumen ejecutivo con KPIs
st.markdown("## 📊 **Resumen Ejecutivo**")

if not df_filtrado.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    # Calcular métricas generales
    total_energia = 0
    potencia_total_actual = 0
    
    for maquina_id, config in maquinas_config.items():
        metricas = calcular_metricas_maquina(df_filtrado, config)
        total_energia += metricas["energia_consumida"]
        potencia_total_actual += metricas["potencia_actual"]
    
    total_costo = total_energia * costo_kwh
    
    with col1:
        st.metric(
            label="⚡ Potencia Total Actual",
            value=f"{potencia_total_actual:.0f} W",
            delta=f"{potencia_total_actual/1000:.2f} kW"
        )
    
    with col2:
        st.metric(
            label="🔋 Energía Consumida",
            value=f"{total_energia:.2f} kWh",
            delta="Período seleccionado"
        )
    
    with col3:
        st.metric(
            label="💰 Costo Estimado",
            value=f"${total_costo:.2f} MXN",
            delta=f"Tarifa: ${costo_kwh}/kWh"
        )
    
    with col4:
        # Calcular eficiencia (placeholder)
        eficiencia = min(100, (total_energia / (potencia_total_actual * 8 / 1000)) * 100) if potencia_total_actual > 0 else 0
        st.metric(
            label="⚙️ Eficiencia Estimada",
            value=f"{eficiencia:.1f}%",
            delta="vs. capacidad máxima"
        )
else:
    st.warning("⚠️ No hay datos disponibles para la fecha seleccionada.")

# Sección de análisis por máquina
st.markdown("---")
st.markdown("## 🏭 **Análisis por Máquina**")

# Crear tabs para cada máquina
tabs = st.tabs([f'{config["icono"]} {config["nombre"]}' for config in maquinas_config.values()])

for i, (maquina_id, config) in enumerate(maquinas_config.items()):
    with tabs[i]:
        if not df_filtrado.empty:
            metricas = calcular_metricas_maquina(df_filtrado, config)
            
            # KPIs específicos de la máquina
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="🔌 Potencia Actual",
                    value=f"{metricas['potencia_actual']:.0f} W"
                )
            
            with col2:
                st.metric(
                    label="📈 Potencia Máxima",
                    value=f"{metricas['potencia_max']:.0f} W"
                )
            
            with col3:
                st.metric(
                    label="📊 Potencia Promedio",
                    value=f"{metricas['potencia_promedio']:.0f} W"
                )
            
            with col4:
                st.metric(
                    label="⚙️ Estado",
                    value=metricas['estado']
                )
            
            # Gráfico de potencia
            st.markdown("### 📈 **Consumo de Potencia en el Tiempo**")
            fig = crear_grafico_potencia(df_filtrado, maquina_id, config)
            st.plotly_chart(fig, use_container_width=True)
            
            # Análisis adicional
            col_left, col_right = st.columns(2)
            
            with col_left:
                # Distribución de potencia
                st.markdown("### 📊 **Distribución de Potencia**")
                fig_hist = px.histogram(
                    df_filtrado, 
                    x=config["potencia_col"],
                    nbins=20,
                    title="Frecuencia de niveles de potencia",
                    color_discrete_sequence=[config["color"]]
                )
                fig_hist.update_layout(
                    xaxis_title="Potencia (W)",
                    yaxis_title="Frecuencia",
                    showlegend=False,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col_right:                # Información de la máquina
                st.markdown("### ℹ️ **Información de la Máquina**")
                
                energia_consumida = metricas['energia_consumida']
                costo_maquina = energia_consumida * costo_kwh
                
                info_container = st.container()
                with info_container:
                    st.markdown(f"""
                    <div style="background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); 
                         padding: 25px; border-radius: 12px; border-left: 4px solid #3b82f6;
                         margin: 20px 0; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                         color: #1e293b;">
                        <h4 style="color: #3b82f6; margin-top: 0; margin-bottom: 15px; 
                                font-size: 1.2rem; font-weight: 600;">
                            {config["icono"]} {config["nombre"]}
                        </h4>
                        <p style="margin: 10px 0; line-height: 1.6; font-size: 0.95rem;">
                            <strong>⚡ Energía consumida:</strong> {energia_consumida:.2f} kWh
                        </p>
                        <p style="margin: 10px 0; line-height: 1.6; font-size: 0.95rem;">
                            <strong>💰 Costo estimado:</strong> ${costo_maquina:.2f} MXN
                        </p>
                        <p style="margin: 10px 0; line-height: 1.6; font-size: 0.95rem;">
                            <strong>⏱️ Período:</strong> Todo el día (9:00-18:00)
                        </p>
                        <p style="margin: 10px 0; line-height: 1.6; font-size: 0.95rem;">
                            <strong>📊 Estado actual:</strong> {metricas['estado']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                  # Recomendaciones
                if metricas['potencia_actual'] > metricas['potencia_promedio'] * 1.8:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #fef9e7 0%, #fcf3cf 100%);
                         border: 2px solid #f4d03f; color: #b7950b; padding: 18px;
                         border-radius: 10px; margin: 20px 0; font-weight: 500;
                         box-shadow: 0 4px 15px rgba(244, 208, 63, 0.2);">
                        <strong>⚠️ Atención:</strong> La máquina está operando con alta carga. 
                        Considere revisar el proceso para optimizar el consumo.
                    </div>
                    """, unsafe_allow_html=True)
                elif metricas['potencia_actual'] < 100:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #d1f2eb 0%, #a3e4d7 100%);
                         border: 2px solid #58d68d; color: #0e6b47; padding: 18px;
                         border-radius: 10px; margin: 20px 0; font-weight: 500;
                         box-shadow: 0 4px 15px rgba(88, 214, 141, 0.2);">
                        <strong>✅ Estado normal:</strong> La máquina está inactiva o en standby.
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No hay datos disponibles para esta máquina en el período seleccionado.")

# Gráfico comparativo general
st.markdown("---")
st.markdown("## 📈 **Comparativo General de Potencia**")

if not df_filtrado.empty:
    fig_comparativo = go.Figure()
    
    for maquina_id, config in maquinas_config.items():
        fig_comparativo.add_trace(go.Scatter(
            x=df_filtrado["datetime"],
            y=df_filtrado[config["potencia_col"]],
            mode='lines',
            name=f'{config["icono"]} {config["nombre"]}',
            line=dict(color=config["color"], width=2),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Fecha: %{x}<br>' +
                         'Potencia: %{y:.1f} W<br>' +
                         '<extra></extra>'
        ))
    
    # Definir el rango completo del día laboral (9:00-18:00)
    fecha_base = df_filtrado["datetime"].dt.date.iloc[0]
    hora_inicio = pd.Timestamp.combine(fecha_base, pd.Timestamp("09:00:00").time())
    hora_fin = pd.Timestamp.combine(fecha_base, pd.Timestamp("18:00:00").time())
    
    fig_comparativo.update_layout(
        title="🏭 Consumo de Potencia - Todas las Máquinas",
        xaxis_title="Hora",
        yaxis_title="Potencia (W)",
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=60, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            gridcolor='lightgray',
            gridwidth=1,
            title_font=dict(size=12),
            range=[hora_inicio, hora_fin],  # Mostrar todo el día laboral
            dtick=3600000,  # Marcas cada hora (en milisegundos)
            tickformat='%H:%M'  # Formato de hora
        ),
        yaxis=dict(
            gridcolor='lightgray',
            gridwidth=1,
            title_font=dict(size=12)
        )
    )
    
    st.plotly_chart(fig_comparativo, use_container_width=True)
else:
    st.warning("⚠️ No hay datos disponibles para mostrar el comparativo.")

# Análisis por períodos del día
st.markdown("---")
st.markdown("## ⏰ **Análisis por Períodos del Día**")

if not df_filtrado.empty:
    # Agrupar datos por período
    periodos_stats = df_filtrado.groupby('periodo').agg({
        'BRN01 W TOT-AVG': ['mean', 'max', 'count'],
        'BRN02 W TOT-AVG': ['mean', 'max', 'count'],
        'BRN03 W TOT-AVG': ['mean', 'max', 'count']
    }).round(2)
    
    # Crear gráfico de consumo por períodos
    fig_periodos = go.Figure()
    
    # Datos para el gráfico
    periodos_data = []
    for periodo in ["🌅 Mañana (9:00-14:00)", "🍽️ Hora de Comida (14:00-15:00)", "🌆 Tarde (15:00-18:00)"]:
        periodo_df = df_filtrado[df_filtrado['periodo'] == periodo]
        if not periodo_df.empty:
            total_periodo = 0
            for maquina_id, config in maquinas_config.items():
                potencia_promedio = periodo_df[config["potencia_col"]].mean()
                total_periodo += potencia_promedio
            
            periodos_data.append({
                'periodo': periodo.split(' ')[0],
                'periodo_completo': periodo,
                'potencia_total': total_periodo
            })
    
    if periodos_data:
        # Crear gráfico de barras
        periodos_nombres = [p['periodo'] for p in periodos_data]
        periodos_potencia = [p['potencia_total'] for p in periodos_data]
        
        fig_periodos.add_trace(go.Bar(
            x=periodos_nombres,
            y=periodos_potencia,
            text=[f"{p:.0f}W" for p in periodos_potencia],
            textposition='auto',
            marker_color=['#FF6B6B', '#FFA500', '#4ECDC4'],
            name='Potencia Promedio'
        ))
        
        fig_periodos.update_layout(
            title="📊 Consumo Promedio por Período del Día",
            xaxis_title="Período",
            yaxis_title="Potencia Promedio (W)",
            showlegend=False,
            margin=dict(l=0, r=0, t=60, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_periodos, use_container_width=True)
    
    # Mostrar estadísticas detalladas por período
    col1, col2, col3 = st.columns(3)
    
    periodos_info = [
        {"periodo": "🌅 Mañana (9:00-14:00)", "icono": "🌅", "col": col1},
        {"periodo": "🍽️ Hora de Comida (14:00-15:00)", "icono": "🍽️", "col": col2},
        {"periodo": "🌆 Tarde (15:00-18:00)", "icono": "🌆", "col": col3}
    ]
    
    for periodo_info in periodos_info:
        periodo_nombre = periodo_info["periodo"]
        with periodo_info["col"]:
            st.markdown(f"### {periodo_info['icono']} **{periodo_nombre.split(' ')[1]} {periodo_nombre.split(' ')[2]}**")
            periodo_data = df_filtrado[df_filtrado['periodo'] == periodo_nombre]
            if not periodo_data.empty:
                total_periodo = 0
                for maquina_id, config in maquinas_config.items():
                    if not periodo_data.empty:
                        energia_inicial = periodo_data[config["energia_col"]].iloc[0]
                        energia_final = periodo_data[config["energia_col"]].iloc[-1]
                        energia_periodo = energia_final - energia_inicial
                        total_periodo += energia_periodo
                
                costo_periodo = total_periodo * costo_kwh
                potencia_promedio_periodo = sum([periodo_data[config["potencia_col"]].mean() for config in maquinas_config.values()])
                
                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); 
                     padding: 25px; border-radius: 12px; border-left: 4px solid #3b82f6;
                     margin: 20px 0; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                     color: #1e293b;">
                    <p style="margin: 10px 0; line-height: 1.6; font-size: 0.95rem;">
                        <strong>⚡ Energía:</strong> {total_periodo:.2f} kWh
                    </p>
                    <p style="margin: 10px 0; line-height: 1.6; font-size: 0.95rem;">
                        <strong>💰 Costo:</strong> ${costo_periodo:.2f} MXN
                    </p>
                    <p style="margin: 10px 0; line-height: 1.6; font-size: 0.95rem;">
                        <strong>📊 Potencia Promedio:</strong> {potencia_promedio_periodo:.0f} W
                    </p>
                    <p style="margin: 10px 0; line-height: 1.6; font-size: 0.95rem;">
                        <strong>⏱️ Registros:</strong> {len(periodo_data)} mediciones
                    </p>                </div>
                """, unsafe_allow_html=True)
                
                # Destacar la hora de comida
                if "Comida" in periodo_nombre:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #d1f2eb 0%, #a3e4d7 100%);
                         border: 2px solid #58d68d; color: #0e6b47; padding: 18px;
                         border-radius: 10px; margin: 20px 0; font-weight: 500;
                         box-shadow: 0 4px 15px rgba(88, 214, 141, 0.2);">
                        <strong>🍽️ Hora de Comida:</strong> Se puede observar la reducción natural del consumo 
                        durante este período, lo cual es esperado y beneficioso para la eficiencia energética.
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Sin datos para este período")
else:
    st.info("💡 No hay datos disponibles para mostrar el análisis por períodos.")

# Footer informativo
st.markdown("---")
st.markdown("## 📚 **Información del Sistema**")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("""
    ### 🔧 **Especificaciones Técnicas**
    - **Equipo de medición:** Lovato DMG9000
    - **Máquinas monitoreadas:** 3 equipos industriales
    - **Frecuencia de muestreo:** Datos cada minuto
    - **Parámetros medidos:** Potencia (W), Energía acumulada (kWh)
    """)

with col_info2:
    st.markdown("""
    ### 💡 **Interpretación de Estados**
    - 🟢 **Inactiva:** < 100W (Standby/Apagada)
    - 🟡 **Baja carga:** < 50% del promedio
    - 🟠 **Carga normal:** 50-150% del promedio  
    - 🔴 **Alta carga:** > 150% del promedio
    """)

