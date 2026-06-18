import streamlit as st
from datetime import datetime

# 設定網頁標題與排版佈局
st.set_page_config(page_title="桃園市觀音生命紀念園區收費標準", page_icon="🏢", layout="centered")

# ==========================================
# 🎨 終極視覺優化區（網頁完全洗白、主標題 RWD 自適應）
# ==========================================
st.markdown("""
    <style>
    /* 網頁底層與核心區塊完全改為純白，徹底拔除所有陰影與框線 */
    .stApp, .block-container {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        box-shadow: none !important;
        border: none !important;
        border-style: none !important;
        outline: none !important;
        padding: 20px 20px !important;
        margin: 0px auto !important;
    }
    
    /* 強制所有輸入框標籤、提示文字、Toggle 文字為【深黑色】 */
    .stWidgetLabel p, p, label, .stToggle p {
        color: #111111 !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
    }
    
    /* 強制所有文字輸入框與下拉選單本體樣式 */
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
    
    /* 下拉清單選項樣式 */
    div[data-baseweb="popover"] ul, div[data-baseweb="menu"] li, div[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }
    div[data-baseweb="menu"] li:hover {
        background-color: #D6E4F0 !important;
        color: #000000 !important;
    }
    
    /* 將所有開關與容器組件的外層隱形容器框線全部清空 */
    div[data-testid="stCheckbox"], 
    div[data-testid="stToggle"],
    div[data-testid="element-container"] {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* 主標題動態響應式放大 */
    h1 { 
        color: #1E3D59 !important; 
        font-weight: 800 !important; 
        font-size: calc(18px + 1vw) !important; 
        line-height: 1.3 !important;
        word-break: keep-all !important;
        text-align: left !important;
        margin-bottom: 5px !important; 
    }
    @media screen and (max-width: 600px) {
        h1 { font-size: 6vw !important; }
    }
    h2 { color: #1E3D59 !important; font-size: 21px !important; font-weight: 700 !important; border-bottom: 2px solid #1E3D59; padding-bottom: 6px; margin-top: 30px !important; }
    
    /* 計算按鈕 */
    div.stButton > button:first-child {
        background-color: #D6E4F0 !important;
        color: #000000 !important;
        font-size: 19px !important;
        font-weight: 900 !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        border: 2px solid #1E3D59 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 核心邏輯運算區（7碼民國年與櫃位計價引擎）
# ==========================================
def parse_roc_date_strict7(roc_str):
    roc_str = roc_str.strip()
    if not roc_str.isdigit() or len(roc_str) != 7: return None
    try:
        roc_year = int(roc_str[0:3])
        month = int(roc_str[3:5])
        day = int(roc_str[5:7])
        return datetime(roc_year + 1911, month, day)
    except ValueError: return None

def calculate_age_roc(birth_roc_str, death_roc_str):
    birth_date = parse_roc_date_strict7(birth_roc_str)
    death_date = parse_roc_date_strict7(death_roc_str)
    if birth_date is None or death_date is None: return None, None
    try:
        age = death_date.year - birth_date.year
        if (death_date.month, death_date.day) < (birth_date.month, birth_date.day): age -= 1
        return age, (death_date - birth_date).days < 365
    except Exception: return None, None

def get_base_price(f_type, c_num):
    cab_str = c_num.strip()
    if not cab_str.isdigit() or len(cab_str) != 4: return None, "格式錯誤"
    layer_num = int(cab_str[0:2])
    seq_num = int(cab_str[2:4])
    
    if layer_num == 4 or seq_num > 51 or seq_num in [4, 14, 24, 34, 44]:
        return None, "編號違規"
        
    if f_type == "牌位": return 35000, "正常"
    elif f_type == "單人骨灰櫃":
        if layer_num in [1, 10, 11, 12]: return 45000, "正常"
        elif layer_num in [2, 3, 8, 9]: return 50000, "正常"
        elif layer_num in [5, 7]: return 55000, "正常"
        elif layer_num == 6: return 60000, "正常"
    elif f_type == "單人骨骸櫃":
        if layer_num == 6: return 60000, "正常"
        elif layer_num in [1, 5]: return 70000, "正常"
        elif layer_num in [2, 3]: return 90000, "正常"
    return None, "層級衝突"

# 顯示主標題
st.title("🏢 桃園市觀音生命紀念園區收費標準")
st.write("---")

# ==========================================
# 1. 填寫亡者基本資料
# ==========================================
st.header("1. 檢查亡者戶籍等相關資料")

# 🌟【精簡二分流】：下拉選單只留桃園市與外縣市，點選即一秒觸發！
city = st.selectbox("亡者除戶所在縣市", ["桃園市", "外縣市"])
is_ty_city = (city == "桃園市")

district = ""
village = ""

# 如果選取桃園市，自動且即時顯現行政區與里，免按 Tab/Enter
if is_ty_city:
    col_dist, col_vil = st.columns(2)
    with col_dist: district = st.text_input("亡者設籍行政區", placeholder="如：觀音區、新屋區")
    with col_vil: village = st.text_input("亡者設籍里", placeholder="如：大堀里、清華里")

col_b, col_d = st.columns(2)
with col_b: birth_str = st.text_input("亡者出生年月日 (民國7碼)", placeholder="如：0390520")
with col_d: death_str = st.text_input("亡者死亡年月日 (民國7碼)", placeholder="如：1150615")

age, is_under_one = calculate_age_roc(birth_str, death_str)

# 外縣市審查大分流
applicant_relation = "無需審查"
is_no_closer_kin = False
is_applicant_ty_1y = False

if city == "外縣市":
    st.write("---")
    st.warning("🔍 系統提示：偵測到亡者為【外縣市籍】，啟動收費標準第4條第1項第2款（家屬設籍優待）動態審查。")
    
    applicant_relation = st.selectbox(
        "請選擇「申請人」與亡者的親屬關係：",
        ["請選擇...", "配偶", "直系血親", "旁系血親二等親以內", "其他親屬/無親屬關係"]
    )
    
    if applicant_relation in ["配偶", "直系血親"]:
        st.success("💡 審查提示：符合第4條第1項第2款前段之申請人資格。請確認下方申請人設籍是否滿一年。")
        is_applicant_ty_1y = st.toggle("申請人（配偶或直系血親）是否已「連續設籍桃園市滿一年以上」？")
    elif applicant_relation == "旁系血親二等親以內":
        st.info("ℹ️ 審查提示：依據法規，旁系二等親提出申請時，須以「亡者無配偶及直系血親」為前提。")
        has_closer_kin = st.radio("亡者是否有配偶或直系血親？", ["原", "無"], index=0)
        if has_closer_kin == "無":
            is_no_closer_kin = True
            st.success("💡 審查提示：已確認亡者無配偶及直系血親，符合旁系二等親代之申請資格。請確認下方申請人設籍是否滿一年。")
            is_applicant_ty_1y = st.toggle("申請人（旁系二等親家屬）是否已「連續設籍桃園市滿一年以上」？")
        else:
            is_no_closer_kin = False
            st.error("🚨 審查結果：不符合第4條第1項第2款資格！（因亡者尚有配偶或直系血親，旁系二等親家屬無法免除限制比照市民價）。")
    elif applicant_relation == "其他親屬/無親屬關係":
        st.error("🚨 審查結果：不符合第4條第1項第2款資格！（非特定家屬身份，無法適用家屬設籍優待條款）。")

# 本市出生未設籍死亡嬰兒 (第4條第1項第5款)
parent_city = parent_district = parent_village = ""
auto_flag_baby_born = False
if age is not None and is_under_one:
    st.write("---")
    st.error("👶 系統偵測：亡者為【未滿一歲嬰兒】！")
    st.subheader("🍼 請填寫法定代理人（父母）資料")
    col_pcity, col_pdist, col_pvil = st.columns(3)
    with col_pcity: parent_city = st.text_input("法定代理人戶籍縣市", value="", placeholder="如：桃園市")
    with col_pdist: parent_district = st.text_input("法定代理人行政區", placeholder="如：觀音區")
    with col_pvil: parent_village = st.text_input("法定代理人設籍里", placeholder="如：大堀里")
    if "桃園" in parent_city: auto_flag_baby_born = True

st.write("---")

# ==========================================
# 2. 選擇申請設施種類與櫃位號碼輸入
# ==========================================
st.header("2. 選擇申請設施與輸入櫃位編號")
col_fac, col_num = st.columns(2)
with col_fac: facility_type = st.selectbox("請選擇申請設施種類", ["單人骨灰櫃", "單人骨骸櫃", "牌位"])
with col_num: cabinet_number = st.text_input("請輸入櫃位號碼後四碼", placeholder="範例：0105")

if cabinet_number.strip():
    _, check_msg = get_base_price(facility_type, cabinet_number)
    if check_msg == "編號違規":
        cab_check = cabinet_number.strip()
        layer_num = int(cab_check[0:2])
        seq_num = int(cab_check[2:4])
        if layer_num == 4: st.error("🚨 櫃位編號即時警示：生命紀念園區『不設第 4 層』櫃位，請重新核對公文書單據！")
        elif seq_num > 51: st.error(f"🚨 櫃位編號即時警示：該層櫃位號碼最多只到 51 號，您輸入了 {seq_num} 號已超出範圍！")
        elif seq_num in [4, 14, 24, 34, 44]: st.error(f"🚨 櫃位編號即時警示：紀念園區不設尾數為 4 的櫃位，請重新確認！")

st.write("---")

# ==========================================
# 3. 勾選符合之特殊減免條件
# ==========================================
st.header("3. 勾選符合之特殊減免條件")

want_upgrade = False
target_cab = ""

if facility_type == "牌位":
    st.caption("💡 提示：目前選擇【牌位】，法規規定牌位為常態固定收費，不適用 any 特殊減免優待。")
    is_diverse = is_low_income = is_hero = is_no_owner = is_no_name = is_tower_damaged = is_project_free = is_special_gov = is_body_donation = False
    is_ty_project_no_bonus = is_out_project_move = is_self_dig = is_buried_5y = is_mutual = False
else:
    is_diverse = st.toggle("1. 非桃園市亡者使用多元葬法專區")
    is_low_income = st.toggle("2. 亡者為各縣市列冊之「低收入戶」或「中低收入戶」")
    is_hero = st.toggle("3. 亡者為軍公教人員、民防人員、義警、義消或其他依法令從事公務「因公殉職」人員")
    is_no_owner = st.toggle("4. 依法應行遷葬之無主墳墓")
    is_no_name = st.toggle("5. 無名屍體、無人認領之屍體或無遺囑且無遺產者")
    is_tower_damaged = st.toggle("6. 原存放桃園市公立納骨塔因更新或毀損無法繼續使用")
    is_project_free = st.toggle("7. 因桃園市公墓更新、公共工程或都市發展辦理搬遷作業，未領取「遷葬補償費」或「救濟金」者【無論本市或外縣市籍】")
    is_special_gov = st.toggle("8. 因天災、事變、不可抗力或特殊原因死亡或家屬生活陷於困難，經桃園市政府專案核准")
    is_body_donation = st.toggle("9. 醫療院所捐贈器官或遺體")
    
    is_ty_project_no_bonus = False
    is_out_project_move = False

    # 🛸 智慧自適應隱藏流
    if is_ty_city:
        is_ty_project_no_bonus = st.toggle("10. 桃園市籍亡者因桃園市公墓更新、公共工程或都市發展辦理搬遷，未領取「加發獎勵金」")
        
    if not is_ty_city:
        is_out_project_move = st.toggle("11. 外縣市籍亡者，因桃園市公墓更新、公共工程或都市發展，未領取「加發獎勵金」")
    
    is_self_dig = st.toggle("12. 屬於桃園市禁葬公墓「自行起掘」遷葬至桃園市公立納骨塔")
    is_buried_5y = st.toggle("13. 亡者已埋葬於桃園市公、私立公墓5年以上，或墳墓設置條例施行前已埋葬桃園市土地，經戶政查詢無亡者戶籍資料者")
    is_mutual = st.toggle("14. 桃園市籍亡者收費與外縣市公立納骨塔市民相同收費，並經桃園市政府公告互惠者")

    # 🛸 核心優待基準判別
    local_villages = ['大堀', '大同', '崙坪', '上大', '富源', '藍埔', '金湖', '新坡', '清華']
    detected_village = next((v for v in local_villages if v in village), None) if "觀音" in district or "新屋" in district else None
    parent_detected_village = next((v for v in local_villages if v in parent_village), None) if "觀音" in parent_district or "新屋" in parent_district else None
    is_baby_local_discount = True if (is_under_one and city == "桃園市" and parent_detected_village) else False
    is_ty = is_ty_city or detected_village or auto_flag_baby_born or is_baby_local_discount

    is_free_triggered = (is_diverse or is_low_income or is_hero or is_no_owner or is_no_name or is_tower_damaged or is_project_free or is_special_gov or is_body_donation or (is_ty and age is not None and age >= 100))
    
    # 🌟 補足差額功能區
    if is_free_triggered:
        st.write("---")
        st.warning("⚠️ **依據第5條第6項**：免收費用者得使用之位置，由管理機關指定之，但得補足差額後使用其他位置。")
        want_upgrade = st.toggle("⚙️ 家屬欲自行挑選特定櫃位（辦理補足差額）")
        
        if want_upgrade:
            target_cab = st.text_input("請輸入家屬自行選定之「自選新櫃位號碼後4碼」", value="", placeholder="如：0612")

st.write("---")

# ==========================================
# 4. 開始判定結果與金額自動計算
# ==========================================
if st.button("🔍 開始自動判別與計算收費金額", use_container_width=True):
    if (is_ty_city and (not district or not village)) or not birth_str or not death_str or not cabinet_number:
        st.error("❌ 錯誤：請務必填寫完整基本資料、日期以及櫃位號碼！")
    elif age is None:
        st.error("❌ 錯誤：日期格式不正確，請精準輸入『7碼純數字』。")
    else:
        base_price, check_msg = get_base_price(facility_type, cabinet_number)
        if check_msg == "編號違規":
            st.error("❌ 錯誤：櫃位號碼違反園區編號規則，請重新修正櫃位編號！")
        elif check_msg == "層級衝突":
            st.error(f"🚨 櫃位與設施衝突：您選擇了【{facility_type}】，但該層無此設施！")
        else:
            cab_str = cabinet_number.strip()
            layer_num = int(cab_str[0:2])
            seq_num = int(cab_str[2:4])
            
            st.info(f"💡 櫃位自動辨識：第 **{layer_num}** 層、第 **{seq_num}** 號 ｜ 亡者精確年齡為 **{age}** 歲")
            
            local_villages = ['大堀', '大同', '崙坪', '上大', '富源', '藍埔', '金湖', '新坡', '清華']
            detected_village = next((v for v in local_villages if v in village), None) if "觀音" in district or "新屋" in district else None
            parent_detected_village = next((v for v in local_villages if v in parent_village), None) if "觀音" in parent_district or "新屋" in parent_district else None
            is_baby_local_discount = True if (is_under_one and city == "桃園市" and parent_detected_village) else False
            is_ty = is_ty_city or detected_village or auto_flag_baby_born or is_baby_local_discount
            is_both_out_project_matched = True if (is_out_project_move and is_buried_5y) else False

            status_type = ""
            law_code = ""
            final_bill = 0
            is_free_case = False
            
            # 🚀 預先計算該亡者如果不