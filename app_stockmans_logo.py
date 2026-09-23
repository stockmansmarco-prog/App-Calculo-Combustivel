import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="Calculadora de Economia | Stockmans",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Consumos conforme planilha-base
CONSUMO_DIESEL = 3.7   # L/h - GTS30D
CONSUMO_GLP = 2.2      # kg/h - GTS30L
PESO_P20 = 20.0        # kg
CONSUMO_ELETRICA = 3.8 # kWh/h - L30XE

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #071526 0%, #0b1f35 100%);
    }
    [data-testid="stHeader"] {background: transparent;}
    #MainMenu, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    display: none !important;
}

    .block-container {
        max-width: 760px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, p, label, .stMarkdown {
        font-family: Arial, sans-serif;
    }

    .brand {
        text-align:center;
        margin-bottom: 1.4rem;
    }
    .brand-name {
        color:#ffffff;
        font-size:2.25rem;
        font-weight:900;
        letter-spacing:.04em;
        margin:0;
    }
    .brand-line {
        width:72px;
        height:5px;
        background:#bed600;
        border-radius:10px;
        margin:10px auto 18px auto;
    }
    .brand-title {
        color:#ffffff;
        font-size:1.55rem;
        font-weight:800;
        margin:0;
    }
    .brand-subtitle {
        color:#b9c6d3;
        font-size:.98rem;
        margin-top:.45rem;
    }

    div[data-testid="stNumberInput"] label {
        color:#eaf0f5 !important;
        font-weight:700;
    }

    div[data-testid="stNumberInput"] input {
        font-size:1.05rem;
    }

    div.stButton > button {
        width:100%;
        background:#bed600;
        color:#071526;
        border:none;
        border-radius:10px;
        font-weight:900;
        font-size:1.08rem;
        min-height:3.25rem;
    }
    div.stButton > button:hover {
        background:#d0e91a;
        color:#071526;
        border:none;
    }

    .section-title {
        color:#ffffff;
        font-size:1.12rem;
        font-weight:800;
        margin:1.4rem 0 .8rem 0;
    }

    .cost-card {
        background:#102942;
        border:1px solid #27445e;
        border-radius:14px;
        padding:16px 18px;
        margin-bottom:10px;
    }
    .cost-model {
        color:#ffffff;
        font-weight:800;
        font-size:1rem;
    }
    .cost-type {
        color:#9fb1c2;
        font-size:.85rem;
    }
    .cost-value {
        color:#ffffff;
        font-weight:900;
        font-size:1.35rem;
        margin-top:5px;
    }

    .saving-card {
        background:#bed600;
        border-radius:16px;
        padding:20px;
        margin:10px 0;
        color:#071526;
    }
    .saving-label {
        font-size:.92rem;
        font-weight:800;
    }
    .saving-value {
        font-size:1.85rem;
        font-weight:950;
        margin:3px 0;
    }
    .saving-detail {
        font-size:.84rem;
        font-weight:650;
    }

    .note {
        color:#8fa1b2;
        font-size:.78rem;
        text-align:center;
        margin-top:1.4rem;
    }

    hr {border-color:#294158 !important;}
</style>
""", unsafe_allow_html=True)

def brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

logo_path = Path(__file__).with_name("logo_stockmans.png")
LOGO_BASE64 = base64.b64encode(logo_path.read_bytes()).decode() if logo_path.exists() else ""

header_html = """
<div class="brand">
    <div style="text-align:center;">
    <img src="data:image/png;base64,{LOGO_BASE64}" style="width:260px;max-width:65%;height:auto;">
    </div>
    <div class="brand-line"></div>
    <div class="brand-title">Calculadora de Economia</div>
    <div class="brand-subtitle">Compare o custo de energia das empilhadeiras CLARK</div>
</div>
"""
header_html = header_html.replace("{LOGO_BASE64}", LOGO_BASE64)
st.markdown(header_html, unsafe_allow_html=True)

st.markdown('<div class="section-title">1. Informe os custos atuais</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    diesel = st.number_input(
        "Diesel — R$/litro",
        min_value=0.0, value=0.0, step=0.01, format="%.2f"
    )
with c2:
    glp_p20 = st.number_input(
        "Recarga GLP P20 — R$",
        min_value=0.0, value=0.0, step=1.0, format="%.2f"
    )

energia = st.number_input(
    "Energia elétrica — R$/kWh",
    min_value=0.0, value=0.0, step=0.01, format="%.2f"
)

st.markdown('<div class="section-title">2. Jornada de utilização</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    horas_dia = st.number_input(
        "Horas trabalhadas por dia",
        min_value=0.0, value=8.0, step=0.5
    )
with c4:
    dias_mes = st.number_input(
        "Dias trabalhados por mês",
        min_value=0, value=22, step=1
    )

calcular = st.button("CALCULAR ECONOMIA", use_container_width=True)

if calcular:
    if diesel <= 0 or glp_p20 <= 0 or energia <= 0:
        st.warning("Informe o preço do diesel, da recarga P20 e da energia elétrica.")
    elif horas_dia <= 0 or dias_mes <= 0:
        st.warning("Informe uma jornada de utilização maior que zero.")
    else:
        custo_diesel_h = diesel * CONSUMO_DIESEL
        custo_glp_h = (glp_p20 / PESO_P20) * CONSUMO_GLP
        custo_eletrica_h = energia * CONSUMO_ELETRICA

        horas_mes = horas_dia * dias_mes
        horas_ano = horas_mes * 12

        econ_diesel_h = custo_diesel_h - custo_eletrica_h
        econ_glp_h = custo_glp_h - custo_eletrica_h

        econ_diesel_mes = econ_diesel_h * horas_mes
        econ_glp_mes = econ_glp_h * horas_mes
        econ_diesel_ano = econ_diesel_h * horas_ano
        econ_glp_ano = econ_glp_h * horas_ano
        
        st.markdown('<div id="resultado-economia"></div>', unsafe_allow_html=True)

st.components.v1.html(
    """
    <script>
        setTimeout(function() {
            const alvo = window.parent.document.getElementById("resultado-economia");
            if (alvo) {
                alvo.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }
        }, 400);
    </script>
    """,
    height=0
)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Custo de energia por hora</div>', unsafe_allow_html=True)

        a, b, c = st.columns(3)
        with a:
            st.markdown(f"""
            <div class="cost-card">
                <div class="cost-model">GTS30D</div>
                <div class="cost-type">Diesel</div>
                <div class="cost-value">{brl(custo_diesel_h)}/h</div>
            </div>""", unsafe_allow_html=True)
        with b:
            st.markdown(f"""
            <div class="cost-card">
                <div class="cost-model">GTS30L</div>
                <div class="cost-type">GLP</div>
                <div class="cost-value">{brl(custo_glp_h)}/h</div>
            </div>""", unsafe_allow_html=True)
        with c:
            st.markdown(f"""
            <div class="cost-card">
                <div class="cost-model">L30XE</div>
                <div class="cost-type">Elétrica</div>
                <div class="cost-value">{brl(custo_eletrica_h)}/h</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-title">Economia estimada com a L30XE elétrica</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="saving-card">
            <div class="saving-label">L30XE × GTS30D DIESEL</div>
            <div class="saving-value">{brl(econ_diesel_mes)} / mês</div>
            <div class="saving-detail">
                {brl(econ_diesel_h)}/h • {brl(econ_diesel_ano)}/ano
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="saving-card">
            <div class="saving-label">L30XE × GTS30L GLP</div>
            <div class="saving-value">{brl(econ_glp_mes)} / mês</div>
            <div class="saving-detail">
                {brl(econ_glp_h)}/h • {brl(econ_glp_ano)}/ano
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.caption(
            f"Simulação considerando {horas_dia:g} h/dia, {dias_mes} dias/mês "
            f"({horas_mes:g} h/mês). Valores estimados exclusivamente a partir "
            "dos consumos médios informados na planilha-base."
        )

st.markdown("""
<div class="note">
    Simulador comercial • Os resultados podem variar conforme aplicação,
    operação, carga, ambiente e condições do equipamento.
</div>
""", unsafe_allow_html=True)
