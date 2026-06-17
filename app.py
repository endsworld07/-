import streamlit as st
from datetime import datetime

# 設定網頁標題與排版佈局
st.set_page_config(page_title="桃園市觀音生命紀念園區收費判別系統", page_icon="🏢", layout="centered")

# ==========================================
# 🎨 全面阻斷黑夜模式之強效 CSS 視覺優化區
# ==========================================
st.markdown("""
    <style>
    /* 調整網頁整體底色 */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* 核心中央白色護眼區塊 */
    .block-container {
        background-color: #FFFFFF !important;
        padding: 35px 45px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
        margin-top: 20px !important;
    }
    
    /* 強制所有輸入框標籤、提示文字為【深黑色】 */
    .stWidgetLabel p, p, label {
        color: #111111 !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
    }
    
    /* 強制所有文字輸入框與下拉選單本體為【純白色】，邊框一致 */
    .stTextInput input, div[data-testid="stSelectbox"] div[text] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }
    div[data-testid="stSelectbox"] > div:first-child > div:first-child {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 4px !important;
    }
    
    /* 強制點開選單後的「彈出下拉清單選項」也必須是【白底黑字】 */
    div[data-baseweb="popover"] ul, div[data-baseweb="menu"] li, div[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }
    div[data-baseweb="menu"] li:hover {
        background-color: #D6E4F0 !important;
        color: #000000 !important;
    }
    
    /* 🌟 核心修正：強制所有勾選方塊 (Checkbox) 的正方形小格子，在電腦端也絕對為【純白底色】與【淡灰細框】 */
    div[data-testid="stCheckbox"] label div:first-child,
    div[data-testid="stCheckbox"] label div:first-child div,
    div[data-testid="stCheckbox"] [data-testid="stMarkdownContainer"]::before {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 4px !important;
    }
    div[data-testid="stCheckbox"] input[type="checkbox"] {
        background-color: #FFFFFF !important;
    }
    
    /* 當方塊被「打勾」之後的狀態（維持原本的高質感深藍） */
    div[data-testid="stCheckbox"] input[type="checkbox"]:checked + div {
        background-color: #1E3D59 !important;
        border-color: #1E3D59 !important;
    }
    
    /* 🌟 核心修正：徹底拔除所有 Checkbox 後方文字的外框、底色與陰影（文字絕對不要有框） */
    div[data-testid="stCheckbox"] [data-testid="stMarkdownContainer"],
    div[data-testid="stCheckbox"] div,
    div[data-testid="stCheckbox"] label {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    div[data-testid="stCheckbox"] p {
        color: #111111 !important;
        font-weight: 600 !important;
        background-color: transparent !important;
        background: transparent !important;
    }
    
    /* 主標題與副標題 */
    h1 {
        color: #1E3D59 !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px;
        margin-bottom: 5px !important;
    }
    .stCaption {
        color: #666666 !important;
        font-size: 14px !important;
    }
    
    /* 段落大標題 */
    h2 {
        color: #1E3D59 !important;
        font-size: 21px !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #1E3D59;
        padding-bottom: 6px;
        margin-top: 30px !important;
        margin-bottom: 15px !important;
    }
    
    /* 核心按鈕：高質感深藍、粗黑字體、黃金圓角 */
    div.stButton > button:first-child {
        background-color: #D6E4F0 !important;
        color: #000000 !important;
        font-size: 19px !important;
        font-weight: 900 !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        border: 2px solid #1E3D59 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.3s ease !important;
        margin-top: 15px !important;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #B6C9DB !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.12) !important;
        color: #000000 !important;
    }
    
    /* 輸入框聚焦提示線 */
    .stTextInput div div input:focus {
        border-color: #1E3D59 !important;
        box-shadow: 0 0 0 1px #1E3D59 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 核心邏輯運算區（7碼民國年與櫃位計價引擎）
# ==========================================
def parse_roc_date_strict7(roc_str):
    roc_str = roc_str.strip()
    if not roc_str.isdigit() or len(roc_str) != 7:
        return None
    try:
        roc_year = int(roc_str[0:3])
        month = int(roc_str[3:5])
        day = int(roc_str[5:7])
        ad_year = roc_year + 1911
        return datetime(ad_year, month, day)
    except ValueError:
        return None

def calculate_age_roc(birth_roc_str, death_roc_str):
    birth_date = parse_roc_date_strict7(birth_roc_str)
    death_date = parse_roc_date_strict7(death_roc_str)
    if birth_date is None or death_date is None:
        return None, None
    try:
        age = death_date.year - birth_date.year
        if (death_date.month, death_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        is_under_one_year = (death_date - birth_date).days < 365
        return age, is_under_one_year
    except Exception:
        return None, None

# ==========================================
# 1. 填寫亡者基本資料
# ==========================================
st.title("🏢 桃園市觀音生命紀念園區收費判別系統")
st.caption("版本：1150617 畫面視覺精緻優化版")
st.write("---")

st.header("1. 檢查亡者戶籍等相關資料")

col_city, col_dist, col_vil = st.columns(3)
with col_city:
    city = st.text_input("亡者死亡時所在縣市", value