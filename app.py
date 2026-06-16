import streamlit as st
from datetime import datetime

# 設定網頁標題與排版佈局
st.set_page_config(page_title="桃園市觀音生命紀念園區收費判別系統", page_icon="🏢", layout="centered")

# ==========================================
# 🎨 進階網頁 CSS 視覺優化區
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
    
    /* 強制所有文字輸入框內部背景改為【純白色】，字體為【深黑色】 */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #CCCCCC !important;
    }
    
    /* 強制下方「勾選方塊的格子」背景為【純白色】 */
    .stCheckbox div[data-testid="stMarkdownContainer"]::before {
        background-color: #FFFFFF !important;
    }
    div[data-testid="stCheckbox"] > label > div:first-child {
        background-color: #FFFFFF !important;
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
# 🌟 核心邏輯運算區（升級：嚴格固定7碼民國年換算引擎）
# ==========================================
def parse_roc_date_strict7(roc_str):
    """嚴格將7碼民國年純數字字串轉換為西元 datetime 物件"""
    roc_str = roc_str.strip()
    if not roc_str.isdigit() or len(roc_str) != 7:
        return None
        
    try:
        # 🟢 修正：嚴格固定前3碼為年，第4-5碼為月，第6-7碼為日
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
st.caption("版本：1150616 最新修正法規公告版 (統一民國7碼版)")
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
    # 🟢 修正：提示字統一改為 7 碼規範範例
    birth_str = st.text_input("亡者出生年月日 (民國7碼)", placeholder="如：0390520")
with col2:
    # 🟢 修正：提示字統一改為 7 碼規範範例
    death_str = st.text_input("亡者死亡年月日 (民國7碼)", placeholder="如：1150615")

# 綜合判定年齡與設籍狀態（採用民國年全新引擎）
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
    
    is_baby_no_registry = "無" in district or district.strip() == "" or "無" in village or village.strip() == ""
    
    st.subheader("🍼 請填寫法定代理人（父母）資料")
    col_pcity, col_pdist, col_pvil = st.columns(3)
    with col_pcity:
        parent_city = st.text_input("法定代理人戶籍縣市", value="", placeholder="如：桃園市")
    with col_pdist:
        parent_district = st.text_input("法定代理人行政區", placeholder="如：觀音區")
    with col_pvil:
        parent_village = st.text_input("法定代理人設籍里", placeholder="如：大堀里")

    if "桃園" in parent_city:
        auto_flag_baby_born = True
        st.success("✨ 系統自動辨識：亡者為未滿一歲嬰兒，因法定代理人戶籍在桃園市，已自動導入桃園市民優待基準審查。")

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
# 4. 開始判定結果
# ==========================================
if st.button("🔍 開始自動判別收費標準", use_container_width=True):
    if not city or not district or not village or not birth_str or not death_str:
        st.error("❌ 錯誤：請務必填寫完整縣市、行政區、里、出生與死亡年月日！")
    else:
        if age is None:
            st.error("❌ 錯誤：日期格式不正確，請精準輸入『7碼純數字』。民國99年以前出生請於前方補0（例如：民國39年5月20日請輸入 0390520）。")
        else:
            st.info(f"💡 系統自動核算：亡者死亡時精確年齡為 **{age}** 歲" + (" (⚠ 未滿一歲嬰兒)" if is_under_one else ""))
            
            local_villages = ['大堀', '大同', '崙坪', '上大', '富源', '藍埔', '金湖', '新坡', '清華']
            
            detected_village = None
            if "觀音" in district or "新屋" in district:
                for v in local_villages:
                    if v in village:
                        detected_village = v
                        break
                    
            parent_detected_village = None
            if "觀音" in parent_district or "新屋" in parent_district:
                for v in local_villages:
                    if v in parent_village:
                        parent_detected_village = v
                        break

            is_baby_local_discount = False
            if is_under_one and "桃園" in parent_city and parent_detected_village is not None:
                is_baby_local_discount = True

            is_ty = is_ty_city or detected_village is not None or auto_flag_baby_born or is_baby_local_discount

            # ==========================================
            # 判斷邏輯核心（從優攔截流、100% 原始法條還原版）
            # ==========================================
            if is_diverse or is_low_income or is_hero or is_no_owner or is_no_name or is_tower_damaged or is_body_donation or (is_ty and age >= 100):
                st.success("🎉 費用全免！")
                st.warning("💡 提示：符合「費用全免」資格的使用者，其塔位使用位置由管理機關指定。若家屬想挑選其他特定位置，可補足差額後使用其他位置。")
                if is_diverse:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第4條第3項**")
                elif is_low_income:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第1項第1款**")
                elif is_hero:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第1項第2款**")
                elif age >= 100:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第1項第3款**")
                elif is_no_name:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第1項第4款**")
                elif is_no_owner:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第1項**第5款")
                elif is_tower_damaged:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第1項第6款**")
                elif is_body_donation:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第1項第7款**")
            
            elif is_ty_project_5y:
                st.success("🔥 特惠：直接比照市民價，再打 5 折！")
                st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第4條第2項**")
            
            elif detected_village is not None or is_baby_local_discount or is_ty_project_no_bonus:
                if is_baby_local_discount:
                    st.success("💰 市民價打 5 折！")
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第2項第1款但書**")
                elif detected_village is not None:
                    if is_under_one:
                        if "桃園" in parent_city and parent_detected_village is not None:
                            st.success("💰 市民價打 5 折！")
                            st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第2項第1款邊但書**")
                        else:
                            st.warning("🟢 常態市民價（1 倍基準價）")
                            st.markdown("說明：雖本人設籍特定里，但因其法定代理人戶籍未符合同條款但書連續設籍滿一年之規定，故不適用5折優惠，回歸常態市民價。")
                    else:
                        st.success("💰 市民價打 5 折！")
                        st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第2項第1款**")
                else:
                    st.success("💰 市民價打 5 折！")
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第2項第2款**")
            
            elif is_self_dig:
                st.success("💰 市民價打 9 折！（減免上限一萬元）")
                st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第5條第3項**")
            
            elif is_buried_5y or auto_flag_baby_born or is_mutual or is_applicant_ty or is_ty_city:
                st.success("🟢 常態市民價（1 倍基準價）")
                if auto_flag_baby_born and not is_ty_city:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第4條第1項第5款**")
                elif is_buried_5y and not is_ty_city:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第4條第1項**第4款")
                elif is_mutual and not is_ty_city:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第4條第1項第3款**")
                elif is_applicant_ty and not is_ty_city:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第4條第1項第5款**")
                else:
                    st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第3條附表**")
            
            else:
                st.error("🚨 常態外縣市價")
                st.markdown("**依據**：桃園市公立殯葬設施使用收費標準 **第4條第1項**")