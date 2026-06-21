import streamlit as st
import mysql.connector
import pandas as pd
import time
import datetime
import altair as alt

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN & TEMA ROHIS BLUE ELEGANT
# ---------------------------------------------------------
st.set_page_config(page_title="ROHIS-MATCH", page_icon="🕌", layout="wide")

st.markdown("""
<style>
    /* =====================================================
       ROHIS-MATCH BLUE ELEGANT THEME
       Put global Streamlit theme in .streamlit/config.toml.
       CSS below only polishes layout, cards, tables, sidebar,
       and Islamic geometric identity.
       ===================================================== */

    :root {
        --rm-bg: #F7FBFF;
        --rm-sidebar: #DCEBFF;
        --rm-sidebar-soft: #EFF6FF;
        --rm-card: #FFFFFF;
        --rm-card-soft: #F0F7FF;
        --rm-primary: #2563EB;
        --rm-primary-dark: #1E3A8A;
        --rm-primary-soft: #DBEAFE;
        --rm-sky: #0EA5E9;
        --rm-gold: #D97706;
        --rm-text: #102A43;
        --rm-muted: #64748B;
        --rm-border: #BFDBFE;
        --rm-border-strong: #93C5FD;
        --rm-danger: #EF4444;
    }

    /* ===== GLOBAL RESET & BASE ===== */
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top right, rgba(37,99,235,0.10), transparent 28%),
            linear-gradient(180deg, #F7FBFF 0%, #FFFFFF 55%, #F8FBFF 100%) !important;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #DCEBFF 0%, #EFF6FF 45%, #FFFFFF 100%) !important;
        border-right: 1px solid var(--rm-border) !important;
        box-shadow: 10px 0 32px rgba(30,58,138,0.06) !important;
    }

    html, body, p, label, button, input, textarea, select, [data-testid="stMarkdownContainer"] {
        color: var(--rm-text) !important;
        font-family: 'Segoe UI', 'Inter', Arial, sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--rm-primary-dark) !important;
        letter-spacing: -0.02em !important;
    }

    /* FIX: tombol tutup/buka sidebar Streamlit memakai font ikon Material.
       Jangan sampai berubah menjadi tulisan seperti keyboard_double_arrow. */
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons,
    span[class*="material-symbols"],
    span[class*="Material"],
    [data-testid="collapsedControl"] span,
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapsedControl"] span,
    button[aria-label*="sidebar"] span,
    button[title*="sidebar"] span {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 22px !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: 'liga' !important;
        -webkit-font-smoothing: antialiased !important;
        font-feature-settings: 'liga' !important;
        color: var(--rm-primary) !important;
    }

    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {
        color: var(--rm-primary) !important;
        max-width: 44px !important;
        overflow: hidden !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #EFF6FF; }
    ::-webkit-scrollbar-thumb { background: #93C5FD; border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: #60A5FA; }

    /* Main container spacing */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
    }

    /* Hide deploy button */
    .stDeployButton {display:none;}

    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    div[data-testid="stDecoration"] {
        visibility: hidden !important;
    }

    /* ===== SIDEBAR STYLING ===== */
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
    }
    div[data-testid="stSidebarUserContent"] {
        padding-top: 0 !important;
    }
    div[data-testid="stSidebarUserContent"] label,
    div[data-testid="stSidebarUserContent"] p {
        color: #475569 !important;
        font-size: 13px !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        min-height: 42px !important;
        justify-content: flex-start !important;
        text-align: left !important;
        padding: 9px 12px !important;
        margin: 3px 0 !important;
        border-radius: 12px !important;
        font-size: 13px !important;
        transition: all .18s ease !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.48) !important;
        color: #1E3A8A !important;
        border: 1px solid transparent !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        background: #FFFFFF !important;
        color: var(--rm-primary) !important;
        border: 1px solid var(--rm-border-strong) !important;
        transform: translateX(2px);
    }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--rm-primary), var(--rm-primary-dark)) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--rm-primary) !important;
        border-left: 4px solid var(--rm-sky) !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 22px rgba(37,99,235,0.20) !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1D4ED8, #172554) !important;
        color: #FFFFFF !important;
        border-color: var(--rm-primary-dark) !important;
        border-left-color: var(--rm-gold) !important;
    }

    /* Fallback radio */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 12px !important;
        padding: 9px 12px !important;
        margin: 4px 0 !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #FFFFFF !important;
        border-color: var(--rm-border) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: #FFFFFF !important;
        border-color: var(--rm-primary) !important;
        border-left: 4px solid var(--rm-primary) !important;
        color: var(--rm-primary) !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    /* ===== BUTTONS ===== */
    button[kind="primary"] {
        background: linear-gradient(135deg, var(--rm-primary), var(--rm-primary-dark)) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--rm-primary) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        min-height: 44px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 8px 20px rgba(37,99,235,0.16) !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1D4ED8, #172554) !important;
        color: #FFFFFF !important;
        border-color: #172554 !important;
        transform: translateY(-1px);
    }

    button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: var(--rm-primary) !important;
        border: 1px solid var(--rm-border) !important;
        border-radius: 10px !important;
        min-height: 44px !important;
    }
    button[kind="secondary"]:hover {
        background-color: #EFF6FF !important;
        color: var(--rm-primary-dark) !important;
        border-color: var(--rm-primary) !important;
    }

    /* ===== INPUT, SELECT, TEXTAREA ===== */
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] div {
        background-color: #FFFFFF !important;
        border-color: var(--rm-border) !important;
        color: var(--rm-text) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"]:focus-within,
    div[data-baseweb="textarea"]:focus-within {
        border-color: var(--rm-primary) !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.10) !important;
    }
    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
        border: 1px solid var(--rm-border) !important;
        color: var(--rm-text) !important;
        box-shadow: 0 14px 30px rgba(15,23,42,0.12) !important;
    }
    li[role="option"]:hover {
        background-color: #EFF6FF !important;
    }

    /* ===== METRICS ===== */
    div[data-testid="stMetricValue"] {
        color: var(--rm-primary-dark) !important;
        font-size: 28px !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-size: 12px !important;
    }
    div[data-testid="stMetricDelta"] {
        color: var(--rm-primary) !important;
    }
    [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid var(--rm-border) !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        box-shadow: 0 8px 24px rgba(30,58,138,0.08) !important;
    }

    /* ===== TABS ===== */
    button[data-baseweb="tab"] {
        background: transparent !important;
        color: #64748B !important;
        border-bottom: 2px solid transparent !important;
        font-size: 13px !important;
    }
    button[aria-selected="true"][data-baseweb="tab"] {
        color: var(--rm-primary) !important;
        border-bottom-color: var(--rm-primary) !important;
        font-weight: 700 !important;
        background: transparent !important;
    }
    div[data-testid="stTabs"] {
        border-bottom: 1px solid var(--rm-border) !important;
    }

    /* ===== DATAFRAME / TABLE ===== */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--rm-border) !important;
        border-radius: 14px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 28px rgba(30,58,138,0.08) !important;
    }
    th {
        background-color: #EAF3FF !important;
        color: #1E3A8A !important;
        font-weight: 700 !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.4px !important;
        border-bottom: 1px solid var(--rm-border) !important;
    }
    td {
        background-color: #FFFFFF !important;
        color: #102A43 !important;
        border-bottom: 1px solid #E2E8F0 !important;
        font-size: 13px !important;
    }
    tr:hover td {
        background-color: #F0F7FF !important;
    }
    [data-testid="stDataFrameResizable"] {
        background: #FFFFFF !important;
    }

    /* ===== ALERTS & NOTIFICATIONS ===== */
    div[data-testid="stNotification"],
    div[data-testid="stAlert"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border-color: var(--rm-border) !important;
        color: var(--rm-text) !important;
    }
    div[data-testid="stAlert"][data-baseweb="notification"] {
        border-left: 4px solid var(--rm-primary) !important;
    }

    /* ===== EXPANDER & FORMS ===== */
    details,
    [data-testid="stForm"] {
        background: #FFFFFF !important;
        border: 1px solid var(--rm-border) !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 24px rgba(30,58,138,0.06) !important;
    }
    [data-testid="stForm"] {
        padding: 20px !important;
    }
    summary {
        color: var(--rm-primary-dark) !important;
        font-weight: 700 !important;
    }

    /* ===== DIALOG / MODAL ===== */
    div[role="dialog"] {
        background: #FFFFFF !important;
        border: 1px solid var(--rm-border) !important;
        border-radius: 16px !important;
        color: var(--rm-text) !important;
    }

    /* ===== DOWNLOAD BUTTON ===== */
    a[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, var(--rm-primary), var(--rm-primary-dark)) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--rm-primary) !important;
    }

    /* ===== BOLD TEXT ===== */
    strong, b {
        color: var(--rm-primary-dark) !important;
        font-weight: 800 !important;
    }

    small, [data-testid="stCaptionContainer"] {
        color: #64748B !important;
    }

    hr {
        border-color: var(--rm-border) !important;
    }

    div[data-testid="stSpinner"] {
        color: var(--rm-primary) !important;
    }

    ul[data-testid="stSelectboxVirtualDropdown"] li {
        background: #FFFFFF !important;
        color: #102A43 !important;
    }
    ul[data-testid="stSelectboxVirtualDropdown"] li:hover {
        background: #EFF6FF !important;
        color: var(--rm-primary) !important;
    }

    [data-testid="stVegaLiteChart"] {
        background: #FFFFFF !important;
        border-radius: 14px !important;
        padding: 8px !important;
        border: 1px solid var(--rm-border) !important;
        box-shadow: 0 8px 24px rgba(30,58,138,0.06) !important;
    }

    /* Utility */
    .rm-card {
        background: #FFFFFF;
        border: 1px solid var(--rm-border);
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(30,58,138,0.08);
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
    /* =====================================================
       FINAL OVERRIDE: BLUE SIDEBAR + SOFT BLUE-WHITE CANVAS
       ===================================================== */
    :root {
        --rm-bg-soft: #EAF3FF;
        --rm-bg-soft-2: #F4F9FF;
        --rm-sidebar-blue: #1E40AF;
        --rm-sidebar-blue-2: #2563EB;
        --rm-sidebar-blue-3: #0F2F74;
        --rm-white: #FFFFFF;
        --rm-text-dark: #102A43;
        --rm-muted-dark: #475569;
        --rm-border-blue: #BFDBFE;
        --rm-gold: #F59E0B;
    }

    /* Background utama tidak full putih, tapi putih kebiruan */
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 85% 5%, rgba(37,99,235,0.16), transparent 30%),
            linear-gradient(135deg, #EAF3FF 0%, #F4F9FF 42%, #E9F2FF 100%) !important;
    }

    /* Sidebar dibuat biru tebal/elegan */
    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #1E40AF 0%, #1D4ED8 48%, #0F2F74 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.25) !important;
        box-shadow: 12px 0 30px rgba(30,64,175,0.22) !important;
    }

    /* Tombol sidebar: teks harus kontras */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"],
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] *,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] p {
        color: #1E40AF !important;
        font-weight: 800 !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.10) !important;
        color: #EAF3FF !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] *,
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] p {
        color: #EAF3FF !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        background: rgba(255,255,255,0.20) !important;
        color: #FFFFFF !important;
        border-color: rgba(255,255,255,0.42) !important;
        transform: translateX(2px);
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: rgba(255,255,255,0.96) !important;
        border: 1px solid rgba(255,255,255,0.88) !important;
        border-left: 5px solid #F59E0B !important;
        box-shadow: 0 12px 24px rgba(15,47,116,0.25) !important;
    }

    /* Tombol utama di area konten: kalau background biru, teks putih */
    main button[kind="primary"],
    main button[kind="primary"] *,
    main button[kind="primary"] p,
    div[data-testid="stAppViewContainer"] main .stButton > button[kind="primary"] *,
    div[data-testid="stAppViewContainer"] main .stButton > button[kind="primary"] p {
        color: #FFFFFF !important;
    }

    /* Kartu dan komponen konten tetap putih lembut, tidak silau */
    [data-testid="stMetric"],
    [data-testid="stForm"],
    details,
    [data-testid="stDataFrame"],
    [data-testid="stVegaLiteChart"] {
        background: rgba(255,255,255,0.86) !important;
        backdrop-filter: blur(8px);
    }

    .rm-card {
        background: rgba(255,255,255,0.88) !important;
    }

    /* Tombol login/logout sudah dipindah ke sidebar, jadi konten aman dari toolbar Streamlit */
    .block-container {
        padding-top: 2.4rem !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.24) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. HELPER: KOMPONEN UI ISLAMI
# ---------------------------------------------------------
def render_page_header(icon: str, title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid #BFDBFE;
        border-left: 4px solid #2563EB;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 14px;
    ">
        <div style="
            width: 46px; height: 46px;
            background: #DBEAFE;
            border: 1.5px solid #3B82F6;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px;
            position: relative;
            flex-shrink: 0;
        ">
            {icon}
            <div style="position:absolute;top:-2px;left:-2px;width:6px;height:6px;border:1px solid #2563EB;border-radius:1px;"></div>
            <div style="position:absolute;top:-2px;right:-2px;width:6px;height:6px;border:1px solid #2563EB;border-radius:1px;"></div>
            <div style="position:absolute;bottom:-2px;left:-2px;width:6px;height:6px;border:1px solid #2563EB;border-radius:1px;"></div>
            <div style="position:absolute;bottom:-2px;right:-2px;width:6px;height:6px;border:1px solid #2563EB;border-radius:1px;"></div>
        </div>
        <div>
            <div style="font-size:17px;font-weight:600;color:#102A43;margin-bottom:3px;">{title}</div>
            <div style="font-size:12px;color:#64748B;">{subtitle}</div>
        </div>
        <div style="margin-left:auto;font-size:24px;color:#D97706;opacity:0.4;letter-spacing:6px;">❋ ✦ ❋</div>
    </div>
    """, unsafe_allow_html=True)


def render_divider_arabic():
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin:8px 0 16px;">
        <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,#3B82F6,transparent);"></div>
        <span style="color:#D97706;opacity:0.5;font-size:14px;">✦</span>
        <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,#3B82F6,transparent);"></div>
    </div>
    """, unsafe_allow_html=True)


def render_card_start(title: str = "", icon: str = ""):
    header = ""
    if title:
        header = f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
            <span style="font-size:15px;">{icon}</span>
            <span style="font-size:13px;font-weight:500;color:#1E293B;">{title}</span>
            <div style="margin-left:auto;width:6px;height:6px;border-radius:50%;background:#2563EB;"></div>
        </div>
        """
    st.markdown(f"""
    <div style="
        background:#FFFFFF;
        border:1px solid #BFDBFE;
        border-radius:10px;
        padding:16px;
        margin-bottom:12px;
    ">
        {header}
    """, unsafe_allow_html=True)


def render_card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def render_geo_badge(label: str, color: str = "#2563EB"):
    st.markdown(f"""
    <span style="
        font-size:11px;
        background:{color}18;
        color:{color};
        border:1px solid {color}40;
        border-radius:20px;
        padding:3px 10px;
        font-weight:500;
    ">{label}</span>
    """, unsafe_allow_html=True)


def render_sidebar_logo():
    st.markdown("""
    <div style="
        padding: 20px 16px 16px;
        border-bottom: 1px solid rgba(255,255,255,0.24);
        margin-bottom: 10px;
    ">
        <div style="font-size:11px;color:#DBEAFE;letter-spacing:2px;margin-bottom:8px;font-weight:700;">
            بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ
        </div>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <div style="
                width:34px;height:34px;border-radius:12px;
                background:rgba(255,255,255,0.14);
                border:1px solid rgba(255,255,255,0.34);
                display:flex;align-items:center;justify-content:center;
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.08);
            ">
                <svg width="21" height="21" viewBox="0 0 20 20" fill="none">
                    <polygon points="10,1 12,7 18,7 13,11 15,17 10,13 5,17 7,11 2,7 8,7"
                        fill="none" stroke="#FFFFFF" stroke-width="1.3"/>
                    <circle cx="10" cy="10" r="2.4" fill="#F59E0B" opacity="0.95"/>
                </svg>
            </div>
            <div>
                <div style="font-size:19px;font-weight:800;color:#FFFFFF;letter-spacing:1px;line-height:1;">
                    ROHIS-MATCH
                </div>
                <div style="font-size:11px;color:#FCD34D;font-weight:800;margin-top:5px;">
                    SMPN 87 Jakarta
                </div>
            </div>
        </div>
        <div style="
            height:4px;
            background: repeating-linear-gradient(
                90deg,
                #FFFFFF 0px, #FFFFFF 18px,
                #93C5FD 18px, #93C5FD 34px,
                #F59E0B 34px, #F59E0B 46px
            );
            opacity:0.90;
            border-radius:99px;
            margin-top:14px;
        "></div>
    </div>
    """, unsafe_allow_html=True)




def render_sidebar_menu(menu_items, key_prefix="menu"):
    """Render menu sidebar dalam bentuk kotak tombol, bukan radio bullet."""
    active_menu = st.session_state.get('menu_aktif') or menu_items[0]
    if active_menu not in menu_items:
        active_menu = menu_items[0]
        st.session_state['menu_aktif'] = active_menu

    for idx, item in enumerate(menu_items):
        is_active = active_menu == item
        button_type = "primary" if is_active else "secondary"
        safe_key = f"{key_prefix}_{idx}_{item.replace(' ', '_').replace('⭐','star').replace('🏠','home').replace('👥','people').replace('📝','input').replace('⚙️','settings')}"
        if st.button(item, key=safe_key, type=button_type, use_container_width=True):
            if st.session_state.get('menu_aktif') != item:
                catat_log(f"Membuka halaman {item}")
            st.session_state['menu_aktif'] = item
            st.rerun()


def render_sidebar_access_note(mode="public"):
    if mode == "login":
        title = "Portal Login Khusus"
        desc = "Halaman ini hanya digunakan oleh Pembina dan Pengurus untuk mengelola data, input penilaian, dan melihat hasil rekomendasi."
        icon = "🔐"
        border = "#F59E0B"
    else:
        title = "Akses Pengguna"
        desc = "Menu publik dapat dilihat tanpa akun. Login hanya untuk Pengurus dan Pembina Rohis."
        icon = "👥"
        border = "#F59E0B"
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.94);border:1px solid rgba(255,255,255,0.78);border-left:5px solid {border};border-radius:14px;padding:14px 15px;margin-top:14px;box-shadow:0 12px 25px rgba(15,47,116,0.18);">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">
            <span style="font-size:16px;">{icon}</span>
            <span style="font-size:12px;font-weight:800;color:#0F2F74;">{title}</span>
        </div>
        <div style="font-size:11px;color:#334155;line-height:1.75;">{desc}</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:11px;">
            <span style="font-size:10px;background:#DBEAFE;color:#1D4ED8;border:1px solid #93C5FD;border-radius:999px;padding:3px 8px;font-weight:700;">Pembina</span>
            <span style="font-size:10px;background:#FFF7ED;color:#D97706;border:1px solid #FDBA74;border-radius:999px;padding:3px 8px;font-weight:700;">Pengurus</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_user_card(username, role_aktif):
    inisial = username[0].upper() if username else "?"
    role_label = (role_aktif or "pengguna").upper()
    role_color = "#1D4ED8" if role_aktif == "pembina" else "#D97706"
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.94);border:1px solid rgba(255,255,255,0.78);border-radius:14px;padding:14px;margin-top:12px;box-shadow:0 12px 25px rgba(15,47,116,0.18);">
        <div style="font-size:10px;color:#64748B;text-transform:uppercase;letter-spacing:1.4px;margin-bottom:10px;font-weight:800;">Akun Aktif</div>
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="
                width:40px;height:40px;border-radius:13px;
                background:#DBEAFE;border:1.5px solid {role_color};
                display:flex;align-items:center;justify-content:center;
                font-size:14px;color:{role_color};font-weight:900;flex-shrink:0;
            ">{inisial}</div>
            <div style="min-width:0;">
                <div style="font-size:12px;color:#0F172A;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{username}</div>
                <div style="font-size:10px;color:{role_color};font-weight:900;text-transform:uppercase;margin-top:2px;">{role_label}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_topbar(menu_name: str):
    # Aman untuk halaman publik: saat belum login, role/username bernilai None.
    role = (st.session_state.get('role') or 'PUBLIK').upper()
    username = st.session_state.get('username') or 'Tamu'
    role_color = "#2563EB" if role == "PEMBINA" else "#D97706"
    tahun_ajaran = get_tahun_ajaran()

    st.markdown(f"""
    <div style="
        background:rgba(255,255,255,0.88);
        border:1px solid #BFDBFE;
        border-left:4px solid #2563EB;
        border-radius:16px;
        padding:13px 16px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:18px;
        box-shadow:0 10px 28px rgba(30,64,175,0.09);
        backdrop-filter: blur(8px);
    ">
        <div style="display:flex;align-items:center;gap:9px;">
            <span style="font-size:16px;font-weight:800;color:#0F2F74;">{menu_name}</span>
            <span style="font-size:12px;color:#3B82F6;">· Tahun Ajaran {tahun_ajaran}</span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="
                font-size:11px;
                background:{role_color}14;
                color:{role_color};
                border:1px solid {role_color}45;
                border-radius:999px;
                padding:5px 12px;
                font-weight:800;
            ">🔐 {role} — {username}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card_custom(label: str, value: str, sub: str = "", accent: str = "#2563EB", icon: str = "📊"):
    st.markdown(f"""
    <div style="
        background:#FFFFFF;
        border:1px solid #BFDBFE;
        border-radius:10px;
        padding:16px 18px;
        position:relative;
        overflow:hidden;
        min-height:136px;
    ">
        <div style="position:absolute;top:0;left:0;right:0;height:2.5px;background:{accent};border-radius:2px 2px 0 0;"></div>
        <div style="font-size:11px;color:#1E293B;margin-bottom:10px;display:flex;align-items:center;gap:6px;font-weight:500;">
            <span style="font-size:13px;">{icon}</span> {label}
        </div>
        <div style="font-size:26px;font-weight:700;color:#D97706;line-height:1.2;max-width:78%;word-wrap:break-word;">{value}</div>
        <div style="font-size:11px;color:#475569;margin-top:8px;max-width:80%;line-height:1.5;">{sub}</div>
        <div style="
            position:absolute;right:16px;top:50%;transform:translateY(-50%);
            width:52px;height:52px;border-radius:14px;
            display:flex;align-items:center;justify-content:center;
            background:{accent}1f;border:1px solid {accent}55;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
            font-size:24px;
        ">{icon}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. KONEKSI DATABASE (MULTI-USER ISOLATION)
# ---------------------------------------------------------
                                                                                                                                                                                                                                                                                                                                                                                                                                              
def create_new_connection():                                                                                                                                                                                                                                                                                                                                                                         
    return mysql.connector.connect(                                                                                                                                                                                                                                                                                                                                               
        host=st.secrets["DB_HOST"],                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        port=int(st.secrets["DB_PORT"]),                                                                                                                                                                                                                                                         
        user=st.secrets["DB_USER"],                                                                                                                                                                                                                                                                                                                                                                                                                                              
        password=st.secrets["DB_PASS"],                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        database=st.secrets["DB_NAME"],                                                                                                                            
        use_pure=True,                                                                                                                                   
        autocommit=True # Wajib agar data langsung tersimpan                                                                                                                             
    )                                                                                                                                                                                                                                                                

# 1. Simpan koneksi secara eksklusif untuk masing-masing user (Private Session)
if 'db_conn' not in st.session_state:
    st.session_state['db_conn'] = create_new_connection()

conn = st.session_state['db_conn']

# 2. Fitur Auto-Reconnect: Cek denyut nadi koneksi sebelum ngapa-ngapain
try:
    conn.ping(reconnect=True, attempts=3, delay=1)
except Exception:
    # Kalau terowongan diputus karena user kelamaan AFK, otomatis bikin baru!
    st.session_state['db_conn'] = create_new_connection()
    conn = st.session_state['db_conn']

# 3. Bikin kursor khusus untuk eksekusi query
cursor = conn.cursor(dictionary=True)                                                                                                                                                                                                                  

# ---------------------------------------------------------
# 4. SESSION STATE & LOGGING
# ---------------------------------------------------------
defaults = {
    'logged_in': False,
    'username': None,
    'role': None,
    'menu_aktif': "🏠 Dashboard",
    'menu_pilihan_key': "🏠 Dashboard",
    'login_attempts': 0,
    'lockout_until': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def catat_log(aksi):
    role_saat_ini = st.session_state['role'] if st.session_state['logged_in'] else 'anggota'
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute(
            "INSERT INTO log_aktivitas (waktu, role, aksi) VALUES (%s, %s, %s)",
            (waktu, role_saat_ini, aksi)
        )
        conn.commit()
    except Exception:
        pass



def get_tahun_ajaran():
    """Menghasilkan tahun ajaran otomatis berdasarkan tanggal saat aplikasi dibuka.
    Logika umum Indonesia: tahun ajaran baru dimulai sekitar Juli.
    Contoh:
    - Januari 2026 -> 2025/2026
    - Juli 2026 -> 2026/2027
    """
    today = datetime.date.today()
    start_year = today.year if today.month >= 7 else today.year - 1
    return f"{start_year}/{start_year + 1}"

def proses_logout():
    catat_log("Keluar (logout) dari sistem")
    for k in ['logged_in', 'username', 'role']:
        st.session_state[k] = False if k == 'logged_in' else None
    st.session_state['menu_aktif'] = "🏠 Dashboard"
    st.session_state['menu_pilihan_key'] = "🏠 Dashboard"
    st.rerun()


@st.dialog("⚠️ Konfirmasi Logout")
def dialog_konfirmasi_logout():
    st.markdown("""
    <div style="text-align:center;padding:10px 0;">
        <div style="font-size:36px;margin-bottom:10px;">🚪</div>
        <p style="color:#475569;">Apakah Anda yakin ingin keluar dari sistem?</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Ya, Keluar", type="primary", use_container_width=True):
            proses_logout()
    with c2:
        if st.button("Batal", use_container_width=True):
            st.rerun()


# ---------------------------------------------------------
# 5. HALAMAN LOGIN
# ---------------------------------------------------------
def halaman_login():
    st.markdown("""
    <div style="text-align:center;margin:20px 0 10px;">
        <div style="font-size:48px;margin-bottom:10px;">🕌</div>
        <h2 style="color:#2563EB;font-size:22px;font-weight:600;margin-bottom:4px;">Portal Login ROHIS-MATCH</h2>
        <p style="color:#64748B;font-size:13px;">Sistem Pendukung Keputusan Divisi Rohis SMPN 87 Jakarta</p>
    </div>
    """, unsafe_allow_html=True)

    render_divider_arabic()

    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown("""
        <div style="
            background:#FFFFFF;
            border:1px solid #93C5FD;
            border-top:3px solid #2563EB;
            border-radius:12px;
            padding:24px;
        ">
            <div style="font-size:15px;font-weight:600;color:#2563EB;margin-bottom:16px;text-align:center;">
                👤 Masuk ke Sistem
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_login"):
            input_user = st.text_input("Username", placeholder="Masukkan username...")
            input_pass = st.text_input("Password", type="password", placeholder="Masukkan password...")
            btn_login = st.form_submit_button("🔐 Login", type="primary", use_container_width=True)

            if btn_login:
                if time.time() < st.session_state['lockout_until']:
                    sisa = int(st.session_state['lockout_until'] - time.time())
                    st.error(f"🛑 Sistem terkunci! Coba lagi dalam **{sisa} detik**.")
                    catat_log("Mencoba login saat masa penalti")
                else:
                    if not input_user or not input_pass:
                        st.warning("⚠️ Username dan Password tidak boleh kosong!")
                    else:
                        cursor.execute(
                            "SELECT * FROM user WHERE username = %s AND password = %s",
                            (input_user, input_pass)
                        )
                        user_data = cursor.fetchone()

                        if user_data:
                            st.session_state.update({
                                'login_attempts': 0,
                                'lockout_until': 0,
                                'logged_in': True,
                                'username': user_data['username'],
                                'role': user_data['role'],
                                'menu_aktif': "🏠 Dashboard",
                                'menu_pilihan_key': "🏠 Dashboard",
                            })
                            catat_log(f"Login berhasil: {user_data['username']}")
                            st.success("✅ Login berhasil! Memuat sistem...")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.session_state['login_attempts'] += 1
                            catat_log(f"Gagal login ke-{st.session_state['login_attempts']}: {input_user}")
                            if st.session_state['login_attempts'] >= 3:
                                st.session_state['lockout_until'] = time.time() + 30
                                st.error("⚠️ Terlalu banyak percobaan gagal! Sistem terkunci 30 detik.")
                            else:
                                sisa = 3 - st.session_state['login_attempts']
                                st.error(f"❌ Username atau Password salah! (Sisa kesempatan: **{sisa}**)")


# ---------------------------------------------------------
# 6. STATISTIK
# ---------------------------------------------------------
def get_statistik():
    cursor.execute("SELECT COUNT(kd_siswa) AS total FROM siswa")
    total_siswa = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(id_divisi) AS total FROM divisi")
    total_divisi = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(id_kriteria) AS total FROM kriteria")
    total_kriteria = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(DISTINCT kd_siswa) AS total FROM hasil_ranking")
    total_ranked = cursor.fetchone()['total']
    return total_siswa, total_divisi, total_kriteria, total_ranked


# ---------------------------------------------------------
# 7. HALAMAN DASHBOARD
# ---------------------------------------------------------
def halaman_dashboard():
    if st.session_state['logged_in']:
        render_topbar("🏠 Dashboard")

        role = st.session_state['role'].lower()
        nama = st.session_state['username']

        if role == 'pembina':
            greeting = f"Assalamu'alaikum, Bapak/Ibu {nama}"
            sub = "Selamat datang kembali di Sistem Pendukung Keputusan Divisi Rohis"
        else:
            greeting = f"Assalamu'alaikum, Kak {nama}"
            sub = "Selamat datang, Pengurus Rohis SMPN 87 Jakarta"

        render_page_header("🕌", greeting, sub)
    else:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 10px;">
            <div style="font-size:40px;margin-bottom:8px;">🕌</div>
            <h1 style="color:#2563EB;font-size:24px;font-weight:600;">ROHIS-MATCH</h1>
            <p style="color:#64748B;font-size:13px;">Sistem Pendukung Keputusan Penempatan Divisi</p>
        </div>
        """, unsafe_allow_html=True)

    render_divider_arabic()

    st.markdown("##### 📊 Ringkasan Data", unsafe_allow_html=True)
    total_siswa, total_divisi, total_kriteria, total_ranked = get_statistik()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card_custom("Total Anggota", f"{total_siswa}", "Siswa terdaftar", "#D97706", "👥")
    with c2:
        render_metric_card_custom("Total Divisi", f"{total_divisi}", "Divisi tersedia", "#D97706", "🏷️")
    with c3:
        render_metric_card_custom("Kriteria Penilaian", f"{total_kriteria}", "Aspek penilaian", "#D97706", "📋")
    with c4:
        pct = f"{(total_ranked/total_siswa*100):.0f}%" if total_siswa else "0%"
        render_metric_card_custom("Sudah Diranking", f"{total_ranked}", f"dari {total_siswa} siswa ({pct})", "#D97706", "⭐")

    render_divider_arabic()

    col_chart, col_rank = st.columns([2, 1])

    with col_chart:
        st.markdown("""
        <div style="
            background:#FFFFFF;border:1px solid #BFDBFE;
            border-radius:10px;padding:16px;margin-bottom:12px;
        ">
            <div style="font-size:13px;font-weight:500;color:#1E293B;margin-bottom:10px;">
                📈 Sebaran Anggota per Divisi
            </div>
        </div>
        """, unsafe_allow_html=True)

        cursor.execute("""
            SELECT d.nama_divisi, COUNT(h.id_ranking) as jumlah
            FROM divisi d
            LEFT JOIN hasil_ranking h ON d.id_divisi = h.id_divisi
            GROUP BY d.id_divisi
        """)
        data_sebaran = cursor.fetchall()
        
        if data_sebaran:
            df_sebaran = pd.DataFrame(data_sebaran)
            df_sebaran = df_sebaran.rename(columns={'nama_divisi': 'Divisi', 'jumlah': 'Jumlah Siswa'})
            
            # Modern UI: Vertical Bar Chart dengan ujung atas melengkung (Rounded Pill)
            chart = alt.Chart(df_sebaran).mark_bar(
                color='#2563EB',
                cornerRadiusTopLeft=8,
                cornerRadiusTopRight=8,
                size=38  # Ketebalan bar biar terlihat padat dan modern
            ).encode(
                x=alt.X('Divisi:N', sort='-y', axis=alt.Axis(labelAngle=-40, title=None, labelColor='#1E293B', labelFontSize=11)),
                y=alt.Y('Jumlah Siswa:Q', axis=alt.Axis(grid=True, gridColor='#93C5FD', title=None, labelColor='#1E293B', tickMinStep=1)),
                tooltip=[alt.Tooltip('Divisi:N', title='Nama Divisi'), alt.Tooltip('Jumlah Siswa:Q', title='Total Anggota')]
            ).properties(
                height=320
            ).configure_view(
                strokeWidth=0 # Menghilangkan garis tepi luar kotak chart agar menyatu dengan background
            )
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Belum ada data penempatan divisi.")

    with col_rank:
        st.markdown("""
        <div style="
            background:#FFFFFF;border:1px solid #BFDBFE;
            border-radius:10px;padding:16px;
        ">
            <div style="font-size:13px;font-weight:500;color:#1E293B;margin-bottom:12px;">
                🏆 Top 5 Anggota dengan Nilai Keseluruhan Terbaik
            </div>
        """, unsafe_allow_html=True)

        # Kueri baru: Menghitung rata-rata mentah (1-100) dari nilai aktual siswa
        cursor.execute("""
            SELECT s.nama_siswa, s.kelas,
                   COALESCE((
                       SELECT GROUP_CONCAT(d.nama_divisi SEPARATOR ' / ') 
                       FROM hasil_ranking h 
                       JOIN divisi d ON h.id_divisi = d.id_divisi 
                       WHERE h.kd_siswa = s.kd_siswa
                   ), 'Belum Ditentukan') as nama_divisi,
                   AVG(n.nilai_aktual) * 20 as rata_rata_100
            FROM siswa s
            JOIN nilai_siswa n ON s.kd_siswa = n.kd_siswa
            WHERE s.kd_siswa IN (SELECT kd_siswa FROM hasil_ranking)
            GROUP BY s.kd_siswa, s.nama_siswa, s.kelas
            HAVING COUNT(DISTINCT n.id_kriteria) = 5
            ORDER BY rata_rata_100 DESC
            LIMIT 5
        """)
        top_list = cursor.fetchall()

        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        if top_list:
            for i, siswa in enumerate(top_list):
                inisial = "".join([n[0].upper() for n in siswa['nama_siswa'].split()[:2]])
                # Menggunakan skor rata-rata mentah murni skala 100
                skor_pct = float(siswa['rata_rata_100'])
                divisi = siswa['nama_divisi'].split(" / ")[0] if siswa['nama_divisi'] else "Belum Ditentukan"
                border_color = "#D97706" if i == 0 else "#93C5FD"
                text_color = "#D97706" if i == 0 else "#2563EB"
                st.markdown(f"""
                <div style="
                    display:flex;align-items:center;gap:8px;
                    background:#EFF6FF;border-radius:8px;
                    padding:8px 10px;margin-bottom:6px;
                    border:1px solid {border_color};
                ">
                    <span style="font-size:14px;width:20px;">{medals[i]}</span>
                    <div style="
                        width:28px;height:28px;border-radius:50%;
                        background:#DBEAFE;border:1.5px solid {border_color};
                        display:flex;align-items:center;justify-content:center;
                        font-size:10px;color:{text_color};font-weight:600;flex-shrink:0;
                    ">{inisial}</div>
                    <div style="flex:1;min-width:0;">
                        <div style="font-size:11px;color:#1E293B;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{siswa['nama_siswa']}</div>
                        <div style="font-size:10px;color:#64748B;">{divisi}</div>
                    </div>
                    <div style="font-size:12px;font-weight:700;color:{text_color};">{skor_pct:.1f}/100</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Belum ada data ranking.")

        st.markdown("</div>", unsafe_allow_html=True)

    # Log aktivitas terbaru (hanya jika login)
    if st.session_state['logged_in']:
        render_divider_arabic()
        st.markdown("##### 🕐 Aktivitas Terbaru", unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background:rgba(255,255,255,0.84);
            border:1px solid #B7D3FF;
            border-left:5px solid #2563EB;
            border-radius:14px;
            padding:14px 16px;
            margin:8px 0 12px;
            box-shadow:0 8px 22px rgba(30,64,175,0.07);
        ">
            <div style="font-size:13px;font-weight:800;color:#0F2F74;margin-bottom:4px;">
                👀 Pantau Aktivitas Sistem
            </div>
            <div style="font-size:12px;color:#475569;line-height:1.65;">
                Lihat riwayat aktivitas terbaru pengguna yang mengakses dan menggunakan web ROHIS-MATCH.
                Catatan ini membantu Pembina dan Pengurus memantau penggunaan sistem secara lebih transparan.
            </div>
        </div>
        """, unsafe_allow_html=True)

        try:
            cursor.execute("SELECT waktu, role, aksi FROM log_aktivitas ORDER BY waktu DESC LIMIT 6")
            logs = cursor.fetchall()
            if logs:
                for log in logs:
                    color = "#2563EB" if "berhasil" in log['aksi'].lower() else "#D97706" if "simpan" in log['aksi'].lower() or "input" in log['aksi'].lower() else "#64748B"
                    st.markdown(f"""
                    <div style="
                        display:flex;
                        gap:12px;
                        align-items:flex-start;
                        padding:10px 0;
                        border-bottom:1px solid rgba(148,163,184,0.35);
                    ">
                        <div style="width:9px;height:9px;border-radius:50%;background:{color};margin-top:5px;flex-shrink:0;"></div>
                        <div style="flex:1;">
                            <div style="font-size:12px;color:#334155;">{log['aksi']}</div>
                            <div style="font-size:10px;color:#3B82F6;margin-top:3px;font-weight:600;">{log['waktu']} · {log['role'].upper()}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Belum ada aktivitas terbaru yang tercatat.")
        except Exception:
            pass


# ---------------------------------------------------------
# 8. HALAMAN DATA SISWA (CRUD)
# ---------------------------------------------------------
def halaman_data_siswa():
    render_topbar("👥 Data Anggota")
    render_page_header("👥", "Manajemen Data Anggota", "Kelola data anggota Rohis yang akan diseleksi penempatan divisinya")

    list_kelas = ["7.1","7.2","7.3","7.4","7.5","7.6","8.1","8.2","8.3","8.4","8.5","8.6"]

    cursor.execute("SELECT kd_siswa, nama_siswa, kelas FROM siswa ORDER BY kd_siswa DESC")
    data_siswa = cursor.fetchall()

    st.markdown("""
    <div style="background:#FFFFFF;border:1px solid #BFDBFE;border-radius:10px;padding:16px;margin-bottom:12px;">
        <div style="font-size:13px;font-weight:500;color:#2563EB;margin-bottom:10px;">📋 Daftar Anggota Terdaftar</div>
    """, unsafe_allow_html=True)

    if data_siswa:
            df_siswa = pd.DataFrame(data_siswa)
            df_siswa.columns = ['ID Siswa', 'Nama Lengkap', 'Kelas']
        
            # Bikin salinan khusus untuk UI: Tambah kolom 'No.' berurutan & hilangkan 'ID Siswa'
            df_tampil = df_siswa.copy()
            df_tampil.insert(0, 'No.', range(1, len(df_tampil) + 1))
            df_tampil = df_tampil[['No.', 'Nama Lengkap', 'Kelas']]
        
            # Tampilkan df_tampil, tapi biarkan df_siswa utuh untuk fitur Edit & Hapus di bawahnya
            st.dataframe(df_tampil, use_container_width=True, hide_index=True)
    else:
            st.info("Belum ada data anggota yang terdaftar.")
            df_siswa = pd.DataFrame()

    st.markdown("</div>", unsafe_allow_html=True)

    render_divider_arabic()
    tab_tambah, tab_edit, tab_hapus = st.tabs(["➕ Tambah Data", "✏️ Edit Data", "🗑️ Hapus Data"])

    with tab_tambah:
        with st.form("form_tambah_siswa"):
            st.markdown("<div style='font-size:14px;font-weight:500;color:#2563EB;margin-bottom:10px;'>Masukkan Data Anggota Baru</div>", unsafe_allow_html=True)
            input_nama = st.text_input("Nama Lengkap Siswa", placeholder="Contoh: Ahmad Fauzan")
            input_kelas = st.selectbox("Kelas", list_kelas)
            btn = st.form_submit_button("💾 Simpan ke Database", type="primary")
            if btn:
                if not input_nama.strip():
                    st.error("❌ Nama siswa tidak boleh kosong!")
                else:
                    try:
                        cursor.execute("INSERT INTO siswa (nama_siswa, kelas) VALUES (%s, %s)", (input_nama, input_kelas))
                        conn.commit()
                        catat_log(f"Menambahkan data siswa: {input_nama} ({input_kelas})")
                        st.success(f"✅ Data **{input_nama}** berhasil ditambahkan!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    with tab_edit:
        if not df_siswa.empty:
            # Bikin kamus rahasia (ID -> Nama)
            map_siswa = dict(zip(df_siswa['ID Siswa'], df_siswa['Nama Lengkap']))
            
            # Jurus format_func biar ID gaib
            kd = st.selectbox(
                "Pilih Anggota yang akan diedit:", 
                options=list(map_siswa.keys()),
                format_func=lambda x: map_siswa[x]
            )
            
            cursor.execute("SELECT * FROM siswa WHERE kd_siswa = %s", (kd,))
            lama = cursor.fetchone()
            with st.form("form_edit_siswa"):
                edit_nama = st.text_input("Nama Lengkap", value=lama['nama_siswa'])
                try:
                    idx = list_kelas.index(lama['kelas'])
                except ValueError:
                    idx = 0
                edit_kelas = st.selectbox("Kelas", list_kelas, index=idx)
                if st.form_submit_button("✏️ Update Data", type="primary"):
                    if not edit_nama.strip():
                        st.error("❌ Nama tidak boleh kosong!")
                    else:
                        cursor.execute("UPDATE siswa SET nama_siswa=%s, kelas=%s WHERE kd_siswa=%s", (edit_nama, edit_kelas, kd))
                        conn.commit()
                        catat_log(f"Mengubah data siswa ID {kd} → {edit_nama} ({edit_kelas})")
                        st.success("✅ Data berhasil diperbarui!")
                        time.sleep(1)
                        st.rerun()
        else:
            st.warning("Tidak ada data yang bisa diedit.")

    with tab_hapus:
        if not df_siswa.empty:
            # Bikin kamus rahasia (ID -> Nama)
            map_siswa = dict(zip(df_siswa['ID Siswa'], df_siswa['Nama Lengkap']))
            
            # Jurus format_func biar ID gaib
            kd = st.selectbox(
                "Pilih Anggota yang akan dihapus:", 
                options=list(map_siswa.keys()),
                format_func=lambda x: map_siswa[x]
            )
            
            nama_hapus = map_siswa[kd] # Ambil nama langsung dari kamus
            
            st.markdown(f"""
            <div style="background:#FEF2F2;border:1px solid #FECACA;border-left:4px solid #EF4444;
                        border-radius:8px;padding:12px 16px;margin-bottom:12px;">
                <div style="font-size:13px;color:#B91C1C;font-weight:500;">⚠️ Peringatan</div>
                <div style="font-size:12px;color:#475569;margin-top:4px;">
                    Menghapus <strong style="color:#B91C1C;">{nama_hapus}</strong> juga akan menghapus seluruh data nilainya. Tindakan ini tidak dapat dibatalkan.
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.form("form_hapus_siswa"):
                if st.form_submit_button("🗑️ Ya, Hapus Permanen", type="primary"):
                    cursor.execute("DELETE FROM siswa WHERE kd_siswa = %s", (kd,))
                    conn.commit()
                    catat_log(f"Menghapus siswa: {nama_hapus}")
                    st.success("✅ Data berhasil dihapus.")
                    time.sleep(1)
                    st.rerun()
        else:
            st.warning("Tidak ada data yang bisa dihapus.")


# ---------------------------------------------------------
# 9. HALAMAN PENGATURAN AKUN
# ---------------------------------------------------------
def halaman_profil():
    render_topbar("⚙️ Pengaturan Akun")
    render_page_header("⚙️", "Pengaturan Akun", "Kelola kredensial akun Anda untuk menjaga keamanan sistem")

    uname = st.session_state['username']
    cursor.execute("SELECT * FROM user WHERE username = %s", (uname,))
    user_info = cursor.fetchone()

    if not user_info:
        st.error("Gagal memuat data akun dari database.")
        return

    tab_info, tab_user, tab_pass = st.tabs(["ℹ️ Info Akun", "✏️ Ubah Username", "🔒 Ubah Password"])

    with tab_info:
        st.markdown(f"""
        <div style="background:#FFFFFF;border:1px solid #BFDBFE;border-radius:10px;padding:20px;max-width:480px;">
            <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px;">
                <div style="
                    width:52px;height:52px;border-radius:50%;
                    background:#DBEAFE;border:2px solid #2563EB;
                    display:flex;align-items:center;justify-content:center;
                    font-size:20px;color:#2563EB;font-weight:700;
                ">{user_info['username'][0].upper()}</div>
                <div>
                    <div style="font-size:16px;font-weight:600;color:#102A43;">{user_info['username']}</div>
                    <div style="
                        font-size:11px;margin-top:4px;padding:2px 10px;
                        background:#DBEAFE;color:#2563EB;border:1px solid #3B82F6;
                        border-radius:20px;display:inline-block;font-weight:500;
                    ">{user_info['role'].upper()}</div>
                </div>
            </div>
            <div style="border-top:1px solid #BFDBFE;padding-top:14px;">
                <div style="font-size:12px;color:#64748B;margin-bottom:6px;">Hak akses Anda menentukan batasan manipulasi data kriteria dan perhitungan algoritma SPK.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_user:
        with st.form("form_ubah_username"):
            st.markdown("<div style='font-size:14px;font-weight:500;color:#2563EB;margin-bottom:10px;'>Ganti Username Akun</div>", unsafe_allow_html=True)
            new_user = st.text_input("Username Baru")
            if st.form_submit_button("🔄 Perbarui Username", type="primary"):
                if not new_user.strip():
                    st.error("❌ Username baru tidak boleh kosong!")
                elif new_user == uname:
                    st.warning("Username baru sama dengan yang sekarang.")
                else:
                    cursor.execute("SELECT * FROM user WHERE username = %s", (new_user,))
                    if cursor.fetchone():
                        st.error("🛑 Username sudah dipakai akun lain!")
                    else:
                        try:
                            cursor.execute("UPDATE user SET username=%s WHERE username=%s", (new_user, uname))
                            conn.commit()
                            catat_log(f"Mengubah username → {new_user}")
                            st.session_state['username'] = new_user
                            st.success("✅ Username berhasil diubah!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

    with tab_pass:
        with st.form("form_ubah_password"):
            st.markdown("<div style='font-size:14px;font-weight:500;color:#2563EB;margin-bottom:10px;'>Ganti Kata Sandi</div>", unsafe_allow_html=True)
            old_p = st.text_input("Password Lama", type="password")
            new_p = st.text_input("Password Baru", type="password")
            conf_p = st.text_input("Konfirmasi Password Baru", type="password")
            if st.form_submit_button("🔒 Perbarui Password", type="primary"):
                if old_p != user_info['password']:
                    st.error("❌ Password lama salah!")
                elif not new_p.strip():
                    st.error("❌ Password baru tidak boleh kosong!")
                elif new_p != conf_p:
                    st.error("❌ Konfirmasi password tidak cocok!")
                else:
                    try:
                        cursor.execute("UPDATE user SET password=%s WHERE username=%s", (new_p, uname))
                        conn.commit()
                        catat_log("Mengubah kata sandi akun")
                        st.success("🔒 Password berhasil diperbarui!")
                    except Exception as e:
                        st.error(f"Error: {e}")


# ---------------------------------------------------------
# 10. HALAMAN INPUT PENILAIAN
# ---------------------------------------------------------
def halaman_input_nilai():
    render_topbar("📝 Input Penilaian")
    render_page_header("📝", "Input Penilaian Aktual Siswa", "Modul Core Engine: Menginput nilai tes untuk diproses pada algoritma Profile Matching")

    cursor.execute("SELECT kd_siswa, nama_siswa FROM siswa ORDER BY nama_siswa ASC")
    data_siswa = cursor.fetchall()
    cursor.execute("SELECT id_kriteria, nama_kriteria FROM kriteria")
    data_kriteria = cursor.fetchall()

    if not data_siswa or not data_kriteria:
        st.warning("⚠️ Data Master belum lengkap. Lengkapi Data Anggota dan Kriteria terlebih dahulu.")
        return

    # Buat dictionary pemetaan ID ke Nama Siswa
    map_siswa = {s['kd_siswa']: s['nama_siswa'] for s in data_siswa}
    
    # Gunakan format_func untuk menyembunyikan ID di layar (tampil nama doang)
    kd_terpilih = st.selectbox(
        "🎓 Pilih Siswa yang Dinilai:", 
        options=list(map_siswa.keys()),
        format_func=lambda x: map_siswa[x]
    )

    pilihan_skala = [
        "1 - Sangat Kurang",
        "2 - Kurang",
        "3 - Cukup / Standar",
        "4 - Baik",
        "5 - Sangat Baik"
    ]

    # Tampilkan nilai lama jika ada
    cursor.execute("SELECT id_kriteria, nilai_aktual FROM nilai_siswa WHERE kd_siswa = %s", (kd_terpilih,))
    nilai_lama = {n['id_kriteria']: n['nilai_aktual'] for n in cursor.fetchall()}

    render_divider_arabic()
    st.markdown("""
    <div style="background:#FFFFFF;border:1px solid #BFDBFE;border-radius:10px;padding:16px;margin-bottom:12px;">
        <div style="font-size:13px;font-weight:500;color:#2563EB;margin-bottom:4px;">📊 Skala Penilaian</div>
        <div style="font-size:11px;color:#64748B;">1 = Sangat Kurang · 2 = Kurang · 3 = Cukup · 4 = Baik · 5 = Sangat Baik</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_input_nilai"):
        nilai_inputan = {}
        c1, c2 = st.columns(2)
        for i, k in enumerate(data_kriteria):
            default_idx = (nilai_lama.get(k['id_kriteria'], 3) - 1)
            with c1 if i % 2 == 0 else c2:
                nilai_inputan[k['id_kriteria']] = st.selectbox(
                    f"📌 {k['nama_kriteria']}",
                    options=pilihan_skala,
                    index=default_idx,
                )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("💾 Simpan Nilai ke Database", type="primary"):
            try:
                cursor.execute("DELETE FROM nilai_siswa WHERE kd_siswa = %s", (kd_terpilih,))
                for id_k, val_str in nilai_inputan.items():
                    angka = int(val_str.split(" - ")[0])
                    cursor.execute(
                        "INSERT INTO nilai_siswa (kd_siswa, id_kriteria, nilai_aktual) VALUES (%s, %s, %s)",
                        (kd_terpilih, id_k, angka)
                    )
                conn.commit()
                catat_log(f"Input/Update nilai siswa ID: {kd_terpilih}")
                st.success("✅ Nilai aktual siswa berhasil disimpan!")
            except Exception as e:
                st.error(f"Kesalahan: {e}")


# ---------------------------------------------------------
# 11. HALAMAN HASIL SPK (PROFILE MATCHING)
# ---------------------------------------------------------
def bobot_gap(gap):
    mapping = {
        0: 5.0, 1: 4.5, -1: 4.0, 2: 3.5, -2: 3.0,
        3: 2.5, -3: 2.0, 4: 1.5, -4: 1.0, 5: 0.5, -5: 0.0
    }
    return mapping.get(gap, 0.0)


def halaman_hasil_spk():
    render_topbar("⭐ Hasil Ranking")
    render_page_header("⭐", "Hasil Ranking Profile Matching", "Rekomendasi penempatan divisi berdasarkan algoritma Profile Matching")

    role_aktif = st.session_state['role'].lower() if st.session_state['logged_in'] else 'publik'

    st.markdown("""
    <div style="background:#FFFFFF;border:1px solid #BFDBFE;border-left:4px solid #D97706;border-radius:10px;padding:14px 16px;margin-bottom:14px;">
        <div style="font-size:13px;font-weight:600;color:#D97706;margin-bottom:6px;">📘 Cara Membaca Hasil Rekomendasi</div>
        <div style="font-size:12px;color:#475569;line-height:1.7;">
            Sistem mencocokkan nilai setiap siswa dengan kebutuhan ideal tiap divisi Rohis. Hasil dengan skor tertinggi
            menjadi rekomendasi utama. Istilah <strong>Nilai Kekuatan Utama (NCF)</strong> berarti nilai pada aspek yang paling penting,
            sedangkan <strong>Nilai Pendukung (NSF)</strong> adalah nilai pada aspek pendukung tambahan.
        </div>
    </div>
    """, unsafe_allow_html=True)

    TARGET_DIVISI = {
        "Syiar":              {"K1": 3, "K2": 3, "K3": 4, "K4": 3, "K5": 4},
        "Tilawah (Kesenian)": {"K1": 4, "K2": 4, "K3": 3, "K4": 3, "K5": 4},
        "Da'i (Kesenian)":    {"K1": 3, "K2": 4, "K3": 4, "K4": 3, "K5": 4},
        "Seni/Kaligrafi":     {"K1": 3, "K2": 3, "K3": 3, "K4": 4, "K5": 4},
        "PSDM":               {"K1": 4, "K2": 4, "K3": 4, "K4": 3, "K5": 4},
        "Sosial":             {"K1": 3, "K2": 3, "K3": 4, "K4": 3, "K5": 4},
        "Takmir Musholla":    {"K1": 4, "K2": 4, "K3": 4, "K4": 3, "K5": 4},
        "CCI (Kesenian)":     {"K1": 4, "K2": 4, "K3": 4, "K4": 3, "K5": 4},
        "Tahfidz (Kesenian)": {"K1": 4, "K2": 4, "K3": 3, "K4": 3, "K5": 4},
    }

    # Core Factor ditentukan berdasarkan validasi mitra, bukan berdasarkan angka target >= 4.
    CORE_FACTOR_DIVISI = {
        "Syiar":              ["K3", "K5"],
        "Tilawah (Kesenian)": ["K1", "K2", "K5"],
        "Da'i (Kesenian)":    ["K2", "K3", "K5"],
        "Seni/Kaligrafi":     ["K4", "K5"],
        "PSDM":               ["K3", "K5"],
        "Sosial":             ["K3", "K5"],
        "Takmir Musholla":    ["K1", "K2", "K5"],
        "CCI (Kesenian)":     ["K1", "K2", "K5"],
        "Tahfidz (Kesenian)": ["K1", "K2", "K5"],
    }

    K_LIST = ["K1", "K2", "K3", "K4", "K5"]

    DIVISI_IDS = {
        "Syiar": 1, "Tilawah (Kesenian)": 2, "Da'i (Kesenian)": 3,
        "Seni/Kaligrafi": 4, "PSDM": 5, "Sosial": 6,
        "Takmir Musholla": 7, "CCI (Kesenian)": 8, "Tahfidz (Kesenian)": 9
    }

    def hitung_detail_divisi(na, div_name):
        target = TARGET_DIVISI.get(div_name)
        core_list = CORE_FACTOR_DIVISI.get(div_name, [])

        if not target or not core_list:
            return {
                "Asli Keseluruhan": 0.0,
                "Asli Syarat Utama": 0.0,
                "NCF": 0.0,
                "NSF": 0.0,
                "Skor Akhir": 0.0,
                "Kecocokan Divisi": 0.0,
            }

        secondary_list = [k for k in K_LIST if k not in core_list]

        bobot = {}
        for k in K_LIST:
            gap = int(na[k]) - int(target[k])
            bobot[k] = bobot_gap(gap)

        ncf = sum(bobot[k] for k in core_list) / len(core_list)
        nsf = sum(bobot[k] for k in secondary_list) / len(secondary_list) if secondary_list else 0.0
        skor_akhir = (0.6 * ncf) + (0.4 * nsf)

        asli_keseluruhan = (sum(int(na[k]) for k in K_LIST) / 25.0) * 100
        asli_syarat_utama = (sum(int(na[k]) for k in core_list) / (len(core_list) * 5.0)) * 100

        return {
            "Asli Keseluruhan": asli_keseluruhan,
            "Asli Syarat Utama": asli_syarat_utama,
            "NCF": ncf,
            "NSF": nsf,
            "Skor Akhir": skor_akhir,
            "Kecocokan Divisi": (skor_akhir / 5.0) * 100,
        }

    def get_data_klasemen():
        cursor.execute("""
            SELECT h.kd_siswa, s.nama_siswa, s.kelas,
                   MAX(h.skor_akhir) AS skor_akhir,
                   GROUP_CONCAT(d.nama_divisi SEPARATOR ' / ') AS nama_divisi
            FROM hasil_ranking h
            JOIN siswa s ON h.kd_siswa = s.kd_siswa
            JOIN divisi d ON h.id_divisi = d.id_divisi
            GROUP BY h.kd_siswa, s.nama_siswa, s.kelas
        """)
        hasil_db = cursor.fetchall()

        if not hasil_db:
            return []

        data = []

        for row in hasil_db:
            cursor.execute("""
                SELECT id_kriteria, nilai_aktual
                FROM nilai_siswa
                WHERE kd_siswa = %s
            """, (row['kd_siswa'],))
            marks = cursor.fetchall()

            na = {f"K{m['id_kriteria']}": int(m['nilai_aktual']) for m in marks}

            if len(na) != 5:
                continue

            detail_semua_divisi = {}
            for div in TARGET_DIVISI.keys():
                detail_semua_divisi[div] = hitung_detail_divisi(na, div)

            rekomendasi_text = row['nama_divisi'] if row['nama_divisi'] else "Belum Ditentukan"
            divisi_utama = rekomendasi_text.split(" / ")[0]
            detail_utama = detail_semua_divisi.get(divisi_utama, {})

            skor_float = float(row['skor_akhir']) if row['skor_akhir'] is not None else detail_utama.get("Skor Akhir", 0.0)
            persen = (skor_float / 5.0) * 100

            data.append({
                "Kd Siswa": row['kd_siswa'],
                "Nama Siswa": row['nama_siswa'],
                "Kelas": row['kelas'],
                "Asli Keseluruhan": detail_utama.get("Asli Keseluruhan", 0.0),
                "Detail Divisi": detail_semua_divisi,
                "NCF": detail_utama.get("NCF", 0.0),
                "NSF": detail_utama.get("NSF", 0.0),
                "Skor (%)": persen,
                "Rekomendasi": rekomendasi_text,
            })

        data.sort(
            key=lambda x: (x["Skor (%)"], x["NCF"], x["Asli Keseluruhan"]),
            reverse=True
        )

        return data

    def render_tabel_klasemen():
        data_mentah = get_data_klasemen()
        if not data_mentah:
            st.info("Belum ada data hasil perankingan di database.")
            return

        tab_individu, tab_keseluruhan = st.tabs(["👤 Cek Hasil Individu", "📊 Data Keseluruhan"])

        with tab_individu:
            render_divider_arabic()
            st.markdown("<div style='font-size:13px;color:#475569;margin-bottom:10px;'>🔍 Cari namamu untuk melihat detail rekomendasi divisi yang paling cocok.</div>", unsafe_allow_html=True)

            opsi = [f"{d['Nama Siswa']} (Kelas {d['Kelas']})" for d in data_mentah]
            pilih = st.selectbox("Nama Siswa:", opsi, index=None, placeholder="Ketik atau pilih nama...")

            if pilih:
                d = next(x for x in data_mentah if f"{x['Nama Siswa']} (Kelas {x['Kelas']})" == pilih)
                divisi_utama = d['Rekomendasi'].split(" / ")[0]

                st.markdown(f"""
                <div style="
                    background:linear-gradient(135deg,#FFFFFF,#DBEAFE);
                    border:1px solid #93C5FD;border-top:3px solid #2563EB;
                    border-radius:12px;padding:20px;margin:12px 0;
                ">
                    <div style="font-size:20px;margin-bottom:4px;">🎉</div>
                    <div style="font-size:17px;font-weight:600;color:#2563EB;margin-bottom:4px;">
                        Selamat, {d['Nama Siswa']}!
                    </div>
                    <div style="font-size:12px;color:#64748B;">Kelas {d['Kelas']}</div>
                </div>
                """, unsafe_allow_html=True)

                c1, c2, c3 = st.columns(3)
                with c1:
                    render_metric_card_custom("Rekomendasi Divisi", divisi_utama, "", "#2563EB", "🏷️")
                with c2:
                    render_metric_card_custom("Tingkat Kecocokan", f"{d['Skor (%)']:.2f}%", "Seberapa cocok nilai siswa dengan kebutuhan divisi", "#D97706", "📊")
                with c3:
                    render_metric_card_custom("Kelayakan Karakter", f"{d['NCF']:.2f} / 5.0", "Kesesuaian sifat dengan kriteria wajib divisi ini", "#3B82F6", "⭐")

                st.markdown(f"""
                <div style="background:#FFFFFF;border:1px solid #BFDBFE;border-radius:10px;padding:16px;margin-top:12px;">
                    <div style="font-size:13px;font-weight:500;color:#2563EB;margin-bottom:8px;">💡 Alasan Rekomendasi</div>
                    <div style="font-size:12px;color:#475569;line-height:1.7;">
                        Sistem membandingkan nilai siswa dengan kebutuhan ideal setiap divisi. Hasil terbaikmu ada pada
                        divisi <strong style="color:#D97706">{divisi_utama}</strong> karena nilai yang kamu miliki paling mendekati
                        kebutuhan divisi tersebut. Tingkat kecocokanmu mencapai
                        <strong style="color:#2563EB">{d['Skor (%)']:.2f}%</strong>, artinya potensi dan kemampuanmu dinilai paling sesuai
                        untuk berkontribusi di divisi ini. Semakin kecil selisih nilai dengan kebutuhan divisi,
                        semakin tinggi rekomendasi yang diberikan sistem.
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab_keseluruhan:
            if 'filter_divisi' not in st.session_state:
                st.session_state['filter_divisi'] = "Semua Divisi"

            list_divisi = ["Semua Divisi","Syiar","Tilawah (Kesenian)","Da'i (Kesenian)",
                           "Seni/Kaligrafi","PSDM","Sosial","Takmir Musholla","CCI (Kesenian)","Tahfidz (Kesenian)"]

            st.markdown("<div style='font-size:13px;color:#475569;margin-bottom:8px;'>🔍 Filter Divisi:</div>", unsafe_allow_html=True)
            for i in range(0, len(list_divisi), 5):
                cols = st.columns(5)
                for j in range(5):
                    if i + j < len(list_divisi):
                        div = list_divisi[i + j]
                        with cols[j]:
                            btn_type = "primary" if st.session_state['filter_divisi'] == div else "secondary"
                            if st.button(div, type=btn_type, use_container_width=True, key=f"btn_f_{i+j}"):
                                st.session_state['filter_divisi'] = div
                                st.rerun()

            render_divider_arabic()

            filter_aktif = st.session_state['filter_divisi']
            
            if filter_aktif == "Semua Divisi":
                data_fil = data_mentah.copy()
                data_fil.sort(
                    key=lambda x: (x["Skor (%)"], x["NCF"], x["Asli Keseluruhan"]),
                    reverse=True
                )
            else:
                # JURUS SULAP: Filter dulu siswanya, buang yang rekomendasinya nggak cocok!
                data_fil = [d for d in data_mentah if filter_aktif in d['Rekomendasi']]
                
                # Setelah difilter, baru di-sort (urutkan) berdasarkan nilai tertingginya
                data_fil.sort(
                    key=lambda x: (
                        x["Detail Divisi"].get(filter_aktif, {}).get("Asli Syarat Utama", 0.0),
                        x["Detail Divisi"].get(filter_aktif, {}).get("NCF", 0.0),
                        x["Detail Divisi"].get(filter_aktif, {}).get("Kecocokan Divisi", 0.0),
                    ),
                    reverse=True
                )

            klasemen = []

            for idx, d in enumerate(data_fil):
                if filter_aktif == "Semua Divisi":
                    row_data = {
                        "Rank": idx + 1,
                        "Nama Siswa": d["Nama Siswa"],
                        "Kelas": d["Kelas"],
                        "Nilai Tes Keseluruhan (Max 100)": f"{d['Asli Keseluruhan']:.1f}",
                        "Kelayakan Karakter (Max 5.0)": f"{d['NCF']:.2f}",
                        "Persentase Kecocokan (Max 100%)": f"{d['Skor (%)']:.2f}%",
                        "Rekomendasi": d["Rekomendasi"],
                    }
                else:
                    detail_fokus = d["Detail Divisi"].get(filter_aktif, {})

                    row_data = {
                        "Rank": idx + 1,
                        "Nama Siswa": d["Nama Siswa"],
                        "Kelas": d["Kelas"],
                        "Nilai Tes Keseluruhan (Max 100)": f"{detail_fokus.get('Asli Keseluruhan', 0.0):.1f}",
                        "Nilai Tes Khusus Divisi Ini (Max 100)": f"{detail_fokus.get('Asli Syarat Utama', 0.0):.1f}",
                        "Kelayakan Karakter (Max 5.0)": f"{detail_fokus.get('NCF', 0.0):.2f}",
                        "Persentase Kecocokan (Max 100%)": f"{detail_fokus.get('Kecocokan Divisi', 0.0):.2f}%",
                        "Fokus Divisi": filter_aktif,
                        "Rekomendasi Utama": d["Rekomendasi"],
                    }

                klasemen.append(row_data)

            if klasemen:
                df_klas = pd.DataFrame(klasemen)
                
                # Cek apakah user sedang login (Pembina/Pengurus)
                if st.session_state.get('logged_in'):
                    c_head, c_pdf, c_xls = st.columns([2, 1, 1])
                    with c_head:
                        st.markdown("### 🏆 Tabel Rekomendasi", unsafe_allow_html=True)
                        
                        if st.session_state['filter_divisi'] == "Semua Divisi":
                            st.caption("Tabel menampilkan ranking rekomendasi utama berdasarkan hasil Profile Matching.")
                        else:
                            st.caption(f"Tabel menampilkan ranking talenta untuk divisi {st.session_state['filter_divisi']} berdasarkan nilai asli syarat utama, NCF, dan kecocokan divisi.")

                    import io
                    buf = io.BytesIO()
                    with pd.ExcelWriter(buf, engine='openpyxl') as w:
                        df_klas.to_excel(w, index=False, sheet_name='Klasemen ROHIS')
                    with c_xls:
                        st.download_button("📊 Download Excel", data=buf.getvalue(),
                                           file_name=f"Laporan_Rohis_{datetime.date.today()}.xlsx",
                                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                           use_container_width=True, type="primary")
                    try:
                        from fpdf import FPDF
                        import tempfile, os

                        class PDF(FPDF):
                            def header(self):
                                self.set_font('Arial','B',12)
                                self.cell(0,10,'Laporan Hasil Penempatan Divisi ROHIS SMPN 87 Jakarta',0,1,'C')
                                if st.session_state['filter_divisi'] != "Semua Divisi":
                                    self.set_font('Arial','I',10)
                                    self.cell(0,8,f"Kategori: {st.session_state['filter_divisi']}",0,1,'C')
                                self.ln(5)

                        # JURUS SULAP: Ubah kertas ke Landscape ('L')
                        pdf = PDF('L', 'mm', 'A4') 
                        pdf.add_page()
                        
                        filter_aktif = st.session_state['filter_divisi']
                        
                        if filter_aktif == "Semua Divisi":
                            # PDF Format 7 Kolom (Kertas Landscape luasnya ~277mm)
                            headers = ["Rank", "Nama Siswa", "Kls", "Tes Umum (100)", "Kelayakan (5)", "Kecocokan(%)", "Rekomendasi"]
                            widths  = [12, 55, 12, 30, 25, 25, 118] # Total Pas 277mm

                            pdf.set_font("Arial", 'B', 9) # Font bisa digedein lagi ke 9
                            for h, w in zip(headers, widths):
                                pdf.cell(w, 10, h, 1, 0, 'C')
                            pdf.ln()

                            pdf.set_font("Arial", size=9)
                            for _, row in df_klas.iterrows():
                                pdf.cell(widths[0], 8, str(row['Rank']), 1, 0, 'C')
                                pdf.cell(widths[1], 8, str(row['Nama Siswa'])[:30], 1, 0, 'L') # Nama bisa lebih panjang
                                pdf.cell(widths[2], 8, str(row['Kelas']), 1, 0, 'C')
                                pdf.cell(widths[3], 8, str(row['Nilai Tes Keseluruhan (Max 100)']), 1, 0, 'C')
                                pdf.cell(widths[4], 8, str(row['Kelayakan Karakter (Max 5.0)']), 1, 0, 'C')
                                pdf.cell(widths[5], 8, str(row['Persentase Kecocokan (Max 100%)']), 1, 0, 'C')

                                rek = str(row['Rekomendasi'])
                                if len(rek) > 75:
                                    rek = rek[:72] + "..." # Teks rekomendasi bisa panjang banget
                                pdf.cell(widths[6], 8, rek, 1, 0, 'L')
                                pdf.ln()

                        else:
                            # PDF Format 8 Kolom (Kertas Landscape ~277mm)
                            headers = ["Rank", "Nama Siswa", "Kls", "Umum(100)", "Khusus(100)", "Karakter(5)", "Cocok(%)", "Fokus Divisi"]
                            widths  = [10, 48, 10, 23, 23, 22, 22, 119] # Total Pas 277mm

                            pdf.set_font("Arial", 'B', 9) # Font dibalikin ke 9
                            for h, w in zip(headers, widths):
                                pdf.cell(w, 10, h, 1, 0, 'C')
                            pdf.ln()

                            pdf.set_font("Arial", size=9)
                            for _, row in df_klas.iterrows():
                                pdf.cell(widths[0], 8, str(row['Rank']), 1, 0, 'C')
                                pdf.cell(widths[1], 8, str(row['Nama Siswa'])[:25], 1, 0, 'L')
                                pdf.cell(widths[2], 8, str(row['Kelas']), 1, 0, 'C')
                                pdf.cell(widths[3], 8, str(row['Nilai Tes Keseluruhan (Max 100)']), 1, 0, 'C')
                                pdf.cell(widths[4], 8, str(row['Nilai Tes Khusus Divisi Ini (Max 100)']), 1, 0, 'C')
                                pdf.cell(widths[5], 8, str(row['Kelayakan Karakter (Max 5.0)']), 1, 0, 'C')
                                pdf.cell(widths[6], 8, str(row['Persentase Kecocokan (Max 100%)']), 1, 0, 'C')

                                fokus = str(row['Fokus Divisi'])
                                if len(fokus) > 70:
                                    fokus = fokus[:67] + "..." # Divisi bisa muat panjang
                                pdf.cell(widths[7], 8, fokus, 1, 0, 'L')
                                pdf.ln()
                       
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            pdf.output(tmp.name)
                            with open(tmp.name, "rb") as f:
                                pdf_bytes = f.read()
                        os.remove(tmp.name)

                        with c_pdf:
                            st.download_button("📄 Download PDF", data=pdf_bytes,
                                               file_name=f"Laporan_Rohis_{datetime.date.today()}.pdf",
                                               mime="application/pdf",
                                               use_container_width=True, type="primary")
                    except ImportError:
                        with c_pdf:
                            st.error("Install fpdf: pip install fpdf")
                else:
                    # Tampilan khusus Tamu Publik (Tanpa tombol Export)
                    st.markdown("### 🏆 Tabel Rekomendasi", unsafe_allow_html=True)
                    
                    if st.session_state['filter_divisi'] == "Semua Divisi":
                        st.caption("Tabel menampilkan ranking rekomendasi utama berdasarkan hasil Profile Matching.")
                    else:
                        st.caption(f"Tabel menampilkan ranking talenta untuk divisi {st.session_state['filter_divisi']} berdasarkan nilai asli syarat utama, NCF, dan kecocokan divisi.")

                st.dataframe(df_klas, hide_index=True, use_container_width=True)
            else:
                st.warning(f"Belum ada data untuk divisi: **{st.session_state['filter_divisi']}**")

    # === PEMBINA: ada tab kalkulasi ===
    if role_aktif == 'pembina':
        tab_kalkulasi, tab_klasemen = st.tabs(["🧮 Kalkulasi Nilai", "📊 Klasemen & Rekomendasi"])

        with tab_kalkulasi:
            df_target = pd.DataFrame([
                {"Divisi / Peminatan": divisi, **target}
                for divisi, target in TARGET_DIVISI.items()
            ])

            # Tambahkan ORDER BY nama_siswa ASC agar namanya urut dari A ke Z
            cursor.execute("SELECT kd_siswa, nama_siswa FROM siswa ORDER BY nama_siswa ASC")
            data_siswa = cursor.fetchall()

            if not data_siswa:
                st.warning("Belum ada data siswa di database.")
            else:
                # Buat dictionary pemetaan ID ke Nama Siswa
                map_siswa = {s['kd_siswa']: s['nama_siswa'] for s in data_siswa}
                
                # Gunakan format_func untuk menyembunyikan ID dari pandangan user
                kd_siswa = st.selectbox(
                    "Pilih siswa untuk melihat proses rekomendasinya:", 
                    options=list(map_siswa.keys()),
                    format_func=lambda x: map_siswa[x]
                )
                
                cursor.execute(
                    "SELECT id_kriteria, nilai_aktual FROM nilai_siswa WHERE kd_siswa = %s ORDER BY id_kriteria ASC",
                    (kd_siswa,)
                )
                data_nilai = cursor.fetchall()

                if len(data_nilai) < 5:
                    st.markdown("""
                    <div style="background:#FEF2F2;border:1px solid #FECACA;border-left:4px solid #EF4444;
                                border-radius:8px;padding:12px 16px;">
                        <div style="font-size:13px;color:#B91C1C;font-weight:500;">⚠️ Data Nilai Tidak Lengkap</div>
                        <div style="font-size:12px;color:#475569;margin-top:4px;">
                            Siswa ini belum memiliki data nilai pada 5 kriteria. Silakan input penilaian terlebih dahulu.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    nilai_aktual = {f"K{n['id_kriteria']}": n['nilai_aktual'] for n in data_nilai}

                    render_divider_arabic()
                    st.markdown(f"""
                    <div style="background:#FFFFFF;border:1px solid #BFDBFE;border-radius:8px;padding:12px 16px;margin-bottom:12px;">
                        <div style="font-size:12px;color:#64748B;margin-bottom:4px;">Nilai Aktual Terdaftar</div>
                        <div style="display:flex;gap:8px;flex-wrap:wrap;">
                            {"".join([f'<span style="background:#DBEAFE;color:#2563EB;border:1px solid #93C5FD;border-radius:6px;padding:4px 10px;font-size:12px;font-weight:600;">{k}: {v}</span>' for k, v in nilai_aktual.items()])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    df_gap = df_target.copy()
                    kriteria_list = ["K1","K2","K3","K4","K5"]
                    hasil_perh = []

                    for i, row in df_gap.iterrows():
                        ncf_t, ncf_c = 0, 0
                        nsf_t, nsf_c = 0, 0
                        
                        divisi_hitung = row['Divisi / Peminatan']
                        core_list = CORE_FACTOR_DIVISI.get(divisi_hitung, [])

                        for k in kriteria_list:
                            target = df_target.loc[i, k]
                            aktual = nilai_aktual[k]
                            gap = aktual - target
                            df_gap.loc[i, k] = gap

                            b = bobot_gap(gap)

                            if k in core_list:
                                ncf_t += b
                                ncf_c += 1
                            else:
                                nsf_t += b
                                nsf_c += 1
                                
                        ncf = ncf_t / ncf_c if ncf_c > 0 else 0
                        nsf = nsf_t / nsf_c if nsf_c > 0 else 0
                        hasil_perh.append({
                            'Divisi / Peminatan': row['Divisi / Peminatan'],
                            'NCF': ncf, 'NSF': nsf,
                            'Skor Akhir': (0.6 * ncf) + (0.4 * nsf)
                        })

                    def color_gap(val):
                        if isinstance(val, int):
                            if val == 0: return 'color: #2563EB; font-weight: bold;'
                            elif val > 0: return 'color: #0EA5E9;'
                            elif val < 0: return 'color: #EF4444;'
                        return ''

                    st.markdown("""
                    <div style="background:#FFFFFF;border:1px solid #BFDBFE;border-radius:10px;padding:14px 16px;margin-top:10px;">
                        <div style="font-size:13px;font-weight:600;color:#2563EB;margin-bottom:6px;">ℹ️ Penjelasan Singkat Perhitungan</div>
                        <div style="font-size:12px;color:#475569;line-height:1.7;">
                            <strong>Selisih Nilai</strong> menunjukkan perbedaan antara kemampuan siswa dengan standar ideal divisi.<br>
                            <strong>Kelayakan Karakter</strong> melihat seberapa pas sifat dominan siswa dengan kriteria wajib divisi.<br>
                            <strong>Persentase Kecocokan</strong> adalah total kecocokan akhir siswa untuk direkomendasikan masuk divisi tersebut.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    tampil_detail = st.checkbox("Tampilkan detail perbandingan nilai dan hasil rekomendasi", key=f"detail_hasil_{kd_siswa}")
                    if tampil_detail:
                        st.markdown("### 1. Perbandingan Nilai Siswa dengan Kebutuhan Divisi")
                        st.caption("Angka pada tabel menunjukkan selisih antara nilai siswa dan standar yang dibutuhkan tiap divisi. Nilai 0 berarti sangat sesuai.")
                        st.dataframe(df_gap.style.map(color_gap, subset=kriteria_list), hide_index=True, use_container_width=True)
                        df_hasil = pd.DataFrame(hasil_perh).sort_values("Skor Akhir", ascending=False).reset_index(drop=True)
                        df_hasil = df_hasil.rename(columns={
                            'NCF': 'Nilai Kekuatan Utama',
                            'NSF': 'Nilai Pendukung',
                            'Skor Akhir': 'Skor Rekomendasi'
                        })
                        st.markdown("### 2. Hasil Nilai Utama, Pendukung, dan Skor Rekomendasi")
                        st.caption("Semakin besar skor rekomendasi, semakin cocok siswa ditempatkan pada divisi tersebut.")
                        st.dataframe(df_hasil, hide_index=True, use_container_width=True)

                    render_divider_arabic()
                    if st.button("💾 Simpan Rekomendasi ke Klasemen", type="primary"):
                        try:
                            df_hasil2 = pd.DataFrame(hasil_perh).sort_values("Skor Akhir", ascending=False).reset_index(drop=True)
                            max_skor = df_hasil2['Skor Akhir'].max()
                            top = df_hasil2[df_hasil2['Skor Akhir'] == max_skor]

                            cursor.execute("DELETE FROM hasil_ranking WHERE kd_siswa = %s", (kd_siswa,))
                            saved = []
                            for _, row in top.iterrows():
                                id_div = DIVISI_IDS.get(row['Divisi / Peminatan'])
                                if id_div:
                                    cursor.execute(
                                        "INSERT INTO hasil_ranking (kd_siswa, id_divisi, nilai_ncf, nilai_nsf, skor_akhir) VALUES (%s, %s, %s, %s, %s)",
                                        (kd_siswa, id_div, float(row['NCF']), float(row['NSF']), float(row['Skor Akhir']))
                                    )
                                    saved.append(row['Divisi / Peminatan'])
                            conn.commit()
                            nama_div = " / ".join(saved)
                            catat_log(f"Menyimpan hasil ranking ({nama_div}) untuk siswa ID: {kd_siswa}")
                            st.success(f"✅ Berhasil menyimpan rekomendasi divisi **{nama_div}**! Cek Tab Klasemen.")
                        except Exception as e:
                            st.error(f"Kesalahan: {e}")

        with tab_klasemen:
            render_tabel_klasemen()

    else:
        render_tabel_klasemen()



# ---------------------------------------------------------
# FINAL UI PATCH V3: soft full background, button contrast, rounded topbar
# ---------------------------------------------------------
st.markdown("""
<style>
    /* 1. Background putih-kebiruan dibuat merata, bukan hanya kanan */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 18% 18%, rgba(96,165,250,0.22) 0%, rgba(96,165,250,0.10) 24%, transparent 46%),
            radial-gradient(circle at 82% 10%, rgba(37,99,235,0.18) 0%, rgba(37,99,235,0.09) 28%, transparent 54%),
            radial-gradient(circle at 50% 92%, rgba(147,197,253,0.24) 0%, rgba(147,197,253,0.10) 35%, transparent 62%),
            linear-gradient(135deg, #E6F1FF 0%, #F2F8FF 36%, #EAF3FF 72%, #E2EEFF 100%) !important;
        background-attachment: fixed !important;
    }

    .main .block-container {
        background: transparent !important;
    }

    /* 2. Semua tombol biru / primary di konten harus putih tulisannya */
    button[kind="primary"],
    button[kind="primary"] *,
    button[kind="primary"] p,
    button[kind="primary"] div,
    button[kind="primary"] span {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* 3. Tombol aktif di sidebar juga biru dengan teks putih */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(96,165,250,0.40), rgba(37,99,235,0.92)) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255,255,255,0.45) !important;
        border-left: 5px solid #F59E0B !important;
        box-shadow: 0 12px 24px rgba(15,47,116,0.25) !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"] *,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] p,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] span {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* 4. Download button: PDF dan Excel jelas putih */
    a[data-testid="stDownloadButton"] button,
    a[data-testid="stDownloadButton"] button *,
    a[data-testid="stDownloadButton"] button p,
    a[data-testid="stDownloadButton"] button div,
    a[data-testid="stDownloadButton"] button span {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    a[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #2563EB, #1E40AF) !important;
        border: 1px solid #1D4ED8 !important;
        border-radius: 12px !important;
        box-shadow: 0 12px 26px rgba(37,99,235,0.22) !important;
    }

    /* 5. Tombol filter divisi aktif: teks putih */
    div.stButton > button[kind="primary"],
    div.stButton > button[kind="primary"] *,
    div.stButton > button[kind="primary"] p,
    div.stButton > button[kind="primary"] span {
        color: #FFFFFF !important;
    }

    /* 6. Topbar Streamlit custom di function sudah rounded, ini jaga-jaga agar tidak tajam */
    [data-testid="stHorizontalBlock"] > div:has(div[style*="Tahun Ajaran"]) {
        border-radius: 16px !important;
    }

    /* 7. Card tetap lembut dan tidak terlalu putih polos */
    [data-testid="stMetric"],
    [data-testid="stForm"],
    details,
    [data-testid="stDataFrame"],
    [data-testid="stVegaLiteChart"] {
        background: rgba(255,255,255,0.82) !important;
        border-color: #B7D3FF !important;
    }

    /* 8. Text di tombol sekunder tetap gelap karena background putih */
    button[kind="secondary"],
    button[kind="secondary"] *,
    button[kind="secondary"] p,
    button[kind="secondary"] span {
        color: #102A43 !important;
    }

    section[data-testid="stSidebar"] button[kind="secondary"],
    section[data-testid="stSidebar"] button[kind="secondary"] *,
    section[data-testid="stSidebar"] button[kind="secondary"] p,
    section[data-testid="stSidebar"] button[kind="secondary"] span {
        color: #EAF3FF !important;
    }

    /* 9. Perbaikan kontras teks tombol di alert/area spesifik */
    .stDownloadButton button:hover,
    button[kind="primary"]:hover {
        filter: brightness(0.96);
    }
</style>
""", unsafe_allow_html=True)



# ---------------------------------------------------------
# FINAL UI PATCH V4: stronger contrast for all blue buttons
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Semua tombol primary dan form submit yang berwarna biru harus memakai teks putih */
    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"] *,
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] div,
    .stButton > button[kind="primary"] span,
    .stFormSubmitButton > button,
    .stFormSubmitButton > button *,
    .stFormSubmitButton > button p,
    .stFormSubmitButton > button div,
    .stFormSubmitButton > button span,
    [data-testid="stFormSubmitButton"] button,
    [data-testid="stFormSubmitButton"] button *,
    [data-testid="stFormSubmitButton"] button p,
    [data-testid="stFormSubmitButton"] button div,
    [data-testid="stFormSubmitButton"] button span {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        font-weight: 700 !important;
    }

    .stFormSubmitButton > button,
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #2563EB, #1E40AF) !important;
        border: 1px solid #1D4ED8 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 22px rgba(37,99,235,0.20) !important;
    }

    /* Tombol download PDF dan Excel */
    .stDownloadButton button,
    .stDownloadButton button *,
    .stDownloadButton button p,
    .stDownloadButton button div,
    .stDownloadButton button span,
    a[data-testid="stDownloadButton"] button,
    a[data-testid="stDownloadButton"] button *,
    a[data-testid="stDownloadButton"] button p,
    a[data-testid="stDownloadButton"] button div,
    a[data-testid="stDownloadButton"] button span {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        font-weight: 700 !important;
    }

    .stDownloadButton button,
    a[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #2563EB, #1E40AF) !important;
        border: 1px solid #1D4ED8 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 22px rgba(37,99,235,0.20) !important;
    }

    /* Tombol filter divisi aktif dan tombol aktif lainnya */
    div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stButton"] button[kind="primary"] *,
    div[data-testid="stButton"] button[kind="primary"] p,
    div[data-testid="stButton"] button[kind="primary"] div,
    div[data-testid="stButton"] button[kind="primary"] span {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Tombol logout di sidebar: karena background-nya gelap transparan, teksnya juga putih */
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stButton > button *,
    section[data-testid="stSidebar"] .stButton > button p,
    section[data-testid="stSidebar"] .stButton > button span {
        color: #FFFFFF !important;
    }

    /* Tapi kartu akun aktif di sidebar tetap gelap teksnya karena background putih */
    section[data-testid="stSidebar"] div[style*="Akun Aktif"],
    section[data-testid="stSidebar"] div[style*="Akun Aktif"] * {
        color: inherit !important;
    }

    /* Input password eye icon tetap terlihat */
    [data-testid="stTextInput"] button,
    [data-testid="stTextInput"] button *,
    div[data-baseweb="input"] button,
    div[data-baseweb="input"] button * {
        color: #0F2F74 !important;
        fill: #0F2F74 !important;
    }

    /* Jaga background utama tetap biru lembut merata */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 14% 14%, rgba(96,165,250,0.25) 0%, rgba(96,165,250,0.12) 30%, transparent 58%),
            radial-gradient(circle at 84% 12%, rgba(37,99,235,0.20) 0%, rgba(37,99,235,0.10) 34%, transparent 62%),
            radial-gradient(circle at 50% 92%, rgba(147,197,253,0.26) 0%, rgba(147,197,253,0.12) 38%, transparent 66%),
            linear-gradient(135deg, #E6F1FF 0%, #F2F8FF 34%, #EAF3FF 72%, #E0EDFF 100%) !important;
        background-attachment: fixed !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 12. ROUTING UTAMA & SIDEBAR
# ---------------------------------------------------------
if not st.session_state['logged_in']:
    with st.sidebar:
        render_sidebar_logo()

        if st.session_state['menu_aktif'] != "Login Akses":
            st.markdown("<div style='padding:8px 4px 6px;font-size:10px;color:#DBEAFE;text-transform:uppercase;letter-spacing:1.8px;margin-top:8px;font-weight:800;'>Menu Publik</div>", unsafe_allow_html=True)
            render_sidebar_menu(["🏠 Dashboard", "⭐ Hasil Ranking"], key_prefix="public_menu")

            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            if st.button("🔐 Login Akses", type="primary", use_container_width=True, key="sidebar_login_access"):
                st.session_state['menu_aktif'] = "Login Akses"
                st.rerun()

            st.divider()
            render_sidebar_access_note("public")
        else:
            st.markdown("<div style='padding:8px 4px 6px;font-size:10px;color:#DBEAFE;text-transform:uppercase;letter-spacing:1.8px;margin-top:8px;font-weight:800;'>Portal Login</div>", unsafe_allow_html=True)
            if st.button("← Kembali ke Dashboard", use_container_width=True, key="sidebar_back_dashboard"):
                st.session_state['menu_aktif'] = "🏠 Dashboard"
                st.rerun()
            st.divider()
            render_sidebar_access_note("login")

    page = st.session_state['menu_aktif']
    if page == "🏠 Dashboard":
        halaman_dashboard()
    elif page == "⭐ Hasil Ranking":
        halaman_hasil_spk()
    elif page == "Login Akses":
        halaman_login()

else:
    with st.sidebar:
        render_sidebar_logo()

        role_aktif = st.session_state['role'].lower()
        username = st.session_state['username']

        if role_aktif == 'pengurus':
            daftar_menu = ["🏠 Dashboard", "👥 Data Anggota", "⭐ Hasil Ranking", "⚙️ Pengaturan"]
        elif role_aktif == 'pembina':
            daftar_menu = ["🏠 Dashboard", "📝 Input Penilaian", "⭐ Hasil Ranking", "⚙️ Pengaturan"]
        else:
            daftar_menu = ["🏠 Dashboard", "⚙️ Pengaturan"]

        st.markdown("<div style='padding:8px 4px 6px;font-size:10px;color:#DBEAFE;text-transform:uppercase;letter-spacing:1.8px;margin-top:8px;font-weight:800;'>Menu Utama</div>", unsafe_allow_html=True)
        render_sidebar_menu(daftar_menu, key_prefix="main_menu")
        menu_pilihan = st.session_state.get('menu_aktif') or daftar_menu[0]
        if menu_pilihan not in daftar_menu:
            menu_pilihan = daftar_menu[0]
            st.session_state['menu_aktif'] = menu_pilihan

        st.divider()
        render_sidebar_user_card(username, role_aktif)

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        if st.button("Keluar 🚪", use_container_width=True, key="sidebar_logout"):
            dialog_konfirmasi_logout()

    if menu_pilihan == "🏠 Dashboard":
        halaman_dashboard()
    elif menu_pilihan == "👥 Data Anggota":
        halaman_data_siswa()
    elif menu_pilihan == "📝 Input Penilaian":
        halaman_input_nilai()
    elif menu_pilihan == "⭐ Hasil Ranking":
        halaman_hasil_spk()
    elif menu_pilihan == "⚙️ Pengaturan":
        halaman_profil()
