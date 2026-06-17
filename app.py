import streamlit as st
from datetime import datetime

# 設定網頁標題與排版佈局
st.set_page_config(page_title="桃園市觀音生命紀念園區收費判別系統", page_icon="🏢", layout="centered")

# ==========================================
# 🎨 進階網頁 CSS 視覺優化區（全面拔除文字框、強制方格白底）
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
    city = st.text_input("亡者死亡時所在縣市", value="", placeholder="如：桃園市、新北市")
with col_dist:
    district = st.text_input("亡者設籍行政區", placeholder="如：觀音區、新屋區")
with col_vil:
    village = st.text_input("亡者設籍里", placeholder="如：大堀里、清華里")

col1, col2 = st.columns(2)
with col1:
    birth_str = st.text_input("亡者出生年月日 (民國7碼)", placeholder="如：0390520")
with col2:
    death_str = st.text_input("亡者死亡年月日 (民國7碼)", placeholder="如：1150615")

# 綜合判定年齡與設籍狀態
age, is_under_one = calculate_age_roc(birth_str, death_str)
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
    
    st.subheader("🍼 請填寫法定代理人（父母）資料")
    col_pcity, col_pdist, col_pvil = st.columns(3)
    with col_pcity:
        parent_city = st.text_input("法定代理人戶籍縣市", value="", placeholder="如：桃園市")
    with col_pdist:
        parent_district = st.text_input("法定代理人行政區", placeholder="如：觀音區")
    with col_pvil = st.text_input("法定代理人設籍里", placeholder="如：大堀里")

    if "桃園" in parent_city:
        auto_flag_baby_born = True
        st.success("✨ 系統自動辨識：亡者為未滿一歲嬰兒，因法定代理人戶籍在桃園市，已自動導入桃園市民優待基準審查。")

st.write("---")

# ==========================================
# 3. 選擇申請設施種類與櫃位號碼輸入
# ==========================================
st.header("2. 選擇申請設施與輸入櫃位編號")

col_fac, col_num = st.columns(2)
with col_fac:
    facility_type = st.selectbox("請選擇申請設施種類", ["單人骨灰櫃", "單人骨骸櫃", "牌位"])
with col_num:
    cabinet_number = st.text_input("請輸入櫃位號碼後四碼", placeholder="範例：0105")

st.write("---")

# ==========================================
# 4. 勾選符合之特殊減免條件
# ==========================================
st.header("3. 勾選符合之特殊減免條件")
st.caption("💡 依法規『多項優待應擇一申請』，若多選系統會自動挑選最優惠項目。")

is_diverse = st.checkbox("使用多元葬法（例如：樹葬等）")
is_low_income = st.checkbox("亡者為各縣市列冊之「低收入戶」或「中低收入戶」")
is_hero = st.checkbox("亡者為軍公教、民防、義警消「因公殉職」人員")
is_no_owner = st.checkbox("亡者身分確認為「無主墳墓」")
is_no_name = st.checkbox("亡者身分確認為「無名屍體」（且經查明確無財產者）")
is_tower_damaged = st.checkbox("原存放桃園市公立納骨塔因更新或毀損無法繼續使用")
is_body_donation = st.checkbox("大體捐贈")

is_ty_project_5y = st.checkbox("同時符合「因桃園市工程遷葬」且「埋葬桃園市公墓 5 年以上」")
is_ty_project_no_bonus = st.checkbox("屬於「桃園市工程遷葬」且「未領取」加發獎勵金者")

is_self_dig = st.checkbox("屬於桃園市禁葬公墓「自行起掘」遷葬至桃園市公立納骨塔")

is_buried_5y = st.checkbox("亡者已埋葬在桃園市公私立墳墓「5 年以上」或「71年以前已埋葬」")
is_mutual = st.checkbox("亡者原籍地納骨塔與桃園市有公告「互惠合作」")
is_applicant_ty = st.checkbox("來辦理的家屬（配偶/直系血親，無配偶或直系以旁系二等親亦同）連續設籍桃園滿 1 年")

st.write("---")

# ==========================================
# 5. 開始判定結果與金額自動計算
# ==========================================
if st.button("🔍 開始自動判別與計算收費金額", use_container_width=True):
    if not city or not district or not village or not birth_str or not death_str or not cabinet_number:
        st.error("❌ 錯誤：請務必填寫完整基本資料、日期以及櫃位號碼！")
    elif age is None:
        st.error("❌ 錯誤：日期格式不正確，請精準輸入『7碼純數字』。民國99年以前出生請於前方補0（例如：0390520）。")
    else:
        cab_str = cabinet_number.strip()
        if not cab_str.isdigit() or len(cab_str) != 4:
            st.error("🚨 櫃位號碼錯誤：請輸入『剛好4碼純數字』的櫃位編號（例如：0101）。")
        else:
            layer_num = int(cab_str[0:2])
            seq_num = int(cab_str[2:4])
            
            if layer_num == 4:
                st.error("🚨 櫃位編號警示：生命紀念園區『不設第 4 層』櫃位，請重新核對公文書單據！")
            elif seq_num > 51:
                st.error(f"🚨 櫃位編號警示：該層櫃位號碼最多只到 51 號，您輸入了 {seq_num} 號已超出範圍！")
            elif seq_num in [4, 14, 24, 34, 44]:
                st.error(f"🚨 櫃位編號警示：紀念園區為求祥和避諱，『不設尾數為 4』的櫃位（無 4、14、24、34、44 號），請重新確認！")
            else:
                base_price = None
                is_layer_valid = True
                
                if facility_type == "牌位":
                    base_price = 35000
                elif facility_type == "單人骨