import streamlit as st
from datetime import datetime

# 設定網頁標題與排版佈局
st.set_page_config(page_title="桃園市觀音生命紀念園區收費判別系統", page_icon="🏢", layout="centered")

# ==========================================
# 🎨 進階網頁 CSS 視覺優化區（輸入框換回純白版）
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
    
    /* 強制所有輸入框、打勾項目的標籤文字為【深黑色】 */
    .stWidgetLabel p, .stCheckbox p, p {
        color: #111111 !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
    }
    
    /* 🌟 強制所有文字輸入框內部背景改為【純白色】，字體為【深黑色】 */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #CCCCCC !important;
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
# 核心邏輯運算區
# ==========================================
def calculate_age(birth_str, death_str):
    try:
        if len(birth_str.strip()) != 8 or len(death_str.strip()) != 8:
            return None, None
        birth_date = datetime.strptime(birth_str.strip(), "%Y%m%d")
        death_date = datetime.strptime(death_str.strip(), "%Y%m%d")
        age = death_date.year - birth_date.year
        if (death_date.month, death_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        is_under_one_year = (death_date - birth_date).days < 365
        return age, is_under_one_year
    except ValueError:
        return None, None

# ==========================================
# 1. 填寫亡者基本資料
# ==========================================
st.title("🏢 桃園市觀音生命紀念園區收費判別系統")
st.caption("版本：1150616 最新修正法規公告版")
st.write("---")

st.header("1. 檢查亡者戶籍等相關資料")

col_city, col_dist, col_vil = st.columns(3)
with col_city:
    city = st.text_input("亡者死亡時所在縣市", value="", placeholder="如：桃園市、新北市")
with col_dist:
    district = st.text_input("亡者設籍行政區", placeholder="如：觀音區、新屋區")
with col_vil:
    village = st.text_input("亡者設籍里", placeholder="如：大堀里、清華里")

col1, col2 = st.columns(2)
with col1:
    birth_str = st.text_input("亡者出生年月日", placeholder="如：19500520")
with col2:
    death_str = st.text_input("亡者死亡年月日", placeholder="如：20260615")

# 綜合判定年齡與設籍狀態
age, is_under_one = calculate_age(birth_str, death_str)
is_ty_city = "桃園" in city if city else False

# ==========================================
# 2. 智慧動態欄位：未滿一歲嬰兒才觸發特定檢查
# ==========================================
parent_city = ""
parent_district = ""
parent_village = ""
auto_flag_baby_born = False

if age is not None and is_under_one:
    st.write("---")
    st.error("👶 系統偵測：亡者為【未滿一歲嬰兒】！")
    
    is_baby_no_registry = "無" in district or district.strip() == "" or "無" in village or village.strip() == ""
    
    st.subheader("🍼 請填寫法定代理人（父母）資料")
    col_pcity, col_pdist, col_pvil = st.columns(3)
    with col_pcity:
        parent_city = st.text_input("法定代理人戶籍縣市", value="", placeholder="如：桃園市")
    with col_pdist:
        parent_district = st.text_input("法定代理人行政區", placeholder="如：觀音區")
    with col_pvil:
        parent_village = st.text_input("法定代理人設籍里", placeholder="如：大堀里")

    if (is_baby_no_registry or not is_ty_city) and "桃園" in parent_city:
        auto_flag_baby_born = True
        st.success("✨ 系統自動辨識：亡者為未設籍或外縣市嬰兒，但父母戶籍在桃園市，已自動導入「桃園市出生且未設籍前死亡嬰兒」優待標準。")

st.write("---")

# ==========================================
# 3. 勾選符合之特殊減免條件
# ==========================================
st.header("2. 勾選符合之特殊減免條件")
st.caption("💡 依法規『多項優待應擇一申請』，若多選系統會自動挑選最優惠項目。")

is_diverse = st.checkbox("選擇使用「多元葬法專區」（如樹葬、灑葬等環保葬）")
is_low_income = st.checkbox("亡者為各縣市列冊之「低收入戶」或「中低收入戶」")
is_hero = st.checkbox("亡者為軍公教、民防、義警消「因公殉職」人員")
is_no_owner = st.checkbox("亡者身分確認為「無主墳墓」")
is_no_name = st.checkbox("亡者身分確認為「無名屍體」（且經查明確無財產者）")
is_tower_damaged = st.checkbox("原存放納骨塔設施更新或毀損無法使用")
is_body_donation = st.checkbox("大體捐贈")

is_ty_project_5y = st.checkbox("同時符合「因桃園市工程遷葬」且「埋葬桃園市公墓 5 年以上」")
is_ty_project_no_bonus = st.checkbox("屬於「桃園市工程遷葬」且「未領取」加發獎勵金者")

is_self_dig = st.checkbox("屬於桃園市禁葬公墓「自行起掘」遷葬至桃園市公立納骨塔")

is_buried_5y = st.checkbox("亡者已埋葬在桃園市公私立墳墓「5 年以上」或「71年以前已埋葬」")
is_mutual = st.checkbox("亡者原籍地納骨塔與桃園市有公告「互惠合作」")
is_applicant_ty = st.checkbox("來辦理的家屬（配偶/直系血親，無配偶或直系以旁系二等親亦同）連續設籍桃園滿 1 年")

st.write("---")

# ==========================================
# 4. 开始判定结果
# ==========================================
if st.button("🔍 開始自動判別收費標準", use_container_width=True):