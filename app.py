import streamlit as st
from datetime import datetime

# 設定網頁標題與排版佈局
st.set_page_config(page_title="桃園市觀音生命紀念園區收費判別系統", page_icon="🏢", layout="centered")

# ==========================================
# 🎨 終極視覺優化區（強制白底、文字黑字）
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
    
    /* 強制點開選單後的「彈出下拉清單選項」為【白底黑字】 */
    div[data-baseweb="popover"] ul, div[data-baseweb="menu"] li, div[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }
    div[data-baseweb="menu"] li:hover {
        background-color: #D6E4F0 !important;
        color: #000000 !important;
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
    
    /* 核心按鈕 */
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
st.caption("版本：1150617 公告版")
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
    with col_pvil:
        parent_village = st.text_input("法定代理人設籍里", placeholder="如：大堀里")

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

# 即時警告防呆機制
if cabinet_number.strip():
    cab_check = cabinet_number.strip()
    if not cab_check.isdigit() or len(cab_check) != 4:
        st.warning("⚠️ 櫃位號碼格式提示：請輸入『剛好 4 碼純數字』的櫃位編號。")
    else:
        l_num = int(cab_check[0:2])
        s_num = int(cab_check[2:4])
        if l_num == 4:
            st.error("🚨 櫃位編號即時警示：生命紀念園區『不設第 4 層』櫃位，請重新核對公文書單據！")
        elif s_num > 51:
            st.error(f"🚨 櫃位編號即時警示：該層櫃位號碼最多只到 51 號，您輸入了 {s_num} 號已超出範圍！")
        elif s_num in [4, 14, 24, 34, 44]:
            st.error(f"🚨 櫃位編號即時警示：紀念園區為求祥和避諱，『不設尾數為 4』的櫃位（無 4、14、24、34、44 號），請重新確認！")

st.write("---")

# ==========================================
# 4. 勾選符合之特殊減免條件（🌟 終極修正：全面改用原生 HTML，100% 徹底拔除外框）
# ==========================================
st.header("3. 勾選符合之特殊減免條件")

if facility_type == "牌位":
    st.caption("💡 提示：目前選擇【牌位】，法規規定牌位為常態固定收費，不適用任何特殊減免優待。")
    # 牌位模式下，所有勾選按鈕自動隱藏或失效
    is_diverse = is_low_income = is_hero = is_no_owner = is_no_name = is_tower_damaged = is_body_donation = False
    is_ty_project_5y = is_ty_project_no_bonus = is_self_dig = is_buried_5y = is_mutual = is_applicant_ty = False
else:
    st.caption("💡 依法規『多項優待應擇一申請』，若多選系統會自動挑選最優惠項目。")
    
    # 採用全新原生白底無框排列
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
            
            if layer_num == 4 or seq_num > 51 or seq_num in [4, 14, 24, 34, 44]:
                st.error("❌ 錯誤：櫃位號碼違反園區編號法規規則（不設4層、無尾數4、最大51號），無法進行計費，請修正櫃位編號！")
            else:
                base_price = None
                is_layer_valid = True
                
                # 🌟 核心修正 1：只要是牌位，價格直接卡死 35000，不進行任何層數判定
                if facility_type == "牌位":
                    base_price = 35000
                elif facility_type == "單人骨灰櫃":
                    if layer_num in [1, 10, 11, 12]:
                        base_price = 45000
                    elif layer_num in [2, 3, 8, 9]:
                        base_price = 50000
                    elif layer_num in [5, 7]:
                        base_price = 55000
                    elif layer_num == 6:
                        base_price = 60000
                    else:
                        is_layer_valid = False
                elif facility_type == "單人骨骸櫃":
                    if layer_num == 6:
                        base_price = 60000
                    elif layer_num in [1, 5]:
                        base_price = 70000
                    elif layer_num in [2, 3]:
                        base_price = 90000
                    else:
                        is_layer_valid = False

                if not is_layer_valid or base_price is None:
                    st.error(f"🚨 櫃位與設施衝突：您選擇了【{facility_type}】，但輸入的層數第 【{layer_num}】 層並無規劃此設施櫃位，請核對單據！")
                else:
                    st.info(f"💡 櫃位自動辨識：第 **{layer_num}** 層、第 **{seq_num}** 號 ｜ 亡者精確年齡為 **{age}** 歲" + (" (⚠ 未滿一歲嬰兒)" if is_under_one else ""))
                    
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

                    status_type = ""
                    law_code = ""
                    final_bill = 0
                    
                    # ==========================================
                    # 判斷邏輯核心（牌位獨立攔截流，其餘設施走法條）
                    # ==========================================
                    if facility_type == "牌位":
                        status_type = "常態牌位價"
                        final_bill = 35000
                        law_code = "無（牌位屬常態固定設施，無減免與身份條件限制，依標準收取費用）"
                        
                    else:
                        # 其餘設施走正常減免法條流
                        if is_diverse or is_low_income or is_hero or is_no_owner or is_no_name or is_tower_damaged or is_body_donation or (is_ty and age >= 100):
                            status_type = "費用全免"
                            final_bill = 0
                            if is_diverse: law_code = "第4條第3項：「使用多元葬法專區，免收費用。」"
                            elif is_low_income: law_code = "第5條第1項第1款：「本市列冊之低收入戶，免收費用；中低收入戶，減收百分之五十。」（多項減免從優免收）"
                            elif is_hero: law_code = "第5條第1項第2款：「因公殉職人員，免收費用。」"
                            elif age >= 100: law_code = "第5條第1項第3款：「本市籍百歲以上人瑞，免收費用。」"
                            elif is_no_name: law_code = "第5條第1項第4款：「設籍本市之無名屍體，經查明確無財產者，免收費用。」"
                            elif is_no_owner: law_code = "第5條第1項第5款：「本市轄區內收容之無主墳墓，起掘骨灰骸免收費用。」"
                            elif is_tower_damaged: law_code = "第5條第1項第6款：「原存放桃園市公立納骨塔因更新或毀損無法繼續使用，免收費用。」"
                            elif is_body_donation: law_code = "第5條第1項第7款：「大體捐贈，免收費用。」"
                            
                        elif is_ty_project_5y or detected_village is not None or is_baby_local_discount or is_ty_project_no_bonus:
                            status_type = "市民價打 5 折"
                            final_bill = int(base_price * 0.5)
                            if is_baby_local_discount: 
                                law_code = "第5條第2項第1款但書：「本市籍亡者設籍或存放設施所在地特定里民連續設籍滿一年以上者，減收百分之五十。未滿一歲嬰兒，其法定代理人符合前設籍規定者，亦同。」"
                            elif detected_village is not None:
                                if is_under_one:
                                    if "桃園" in parent_city and parent_detected_village is not None:
                                        law_code = "第5條第2項第1款但書：「未滿一歲嬰兒，其法定代理人符合前設籍規定者，亦同（減收百分之五十）。」"
                                    else:
                                        status_type = "常態市民價"
                                        final_bill = base_price
                                        law_code = "第4條第1項第2款：「在本市出生，且於未設戶籍前死亡之嬰兒，比照本市市民收費基準收取費用。」（說明：雖亡者設籍特定里，但因其法定代理人未於特定里連續設籍滿一年，故不符第5條第2項第1款但書之五折優待，回歸市民價基準。）"
                                else:
                                    law_code = "第5條第2項第1款：「本市籍亡者設籍或存放設施所在地特定里民連續設籍滿一年以上者，減收百分之五十。」"
                            elif is_ty_project_no_bonus: 
                                law_code = "第5條第2項第2款：「屬於桃園市工程遷葬且未領取加發獎勵金者，減收百分之五十。」"
                            elif is_ty_project_5y:
                                status_type = "外縣市工程遷葬特惠（市民價 5 折）"
                                law_code = "第4條第2項：「同時符合第1項第4款及第5款特殊原因者，得比照本市市民收費基準之百分之五十收取費用。」"

                        elif is_self_dig:
                            status_type = "市民價打 9 折（自行起掘）"
                            discount_amount = int(base_price * 0.1)
                            if discount_amount > 10000:
                                discount_amount = 10000
                            final_bill = base_price - discount_amount
                            law_code = "第5條第3項：「屬於桃園市列管禁葬公墓自行起掘移入者，減收百分之十，最高減免一萬元。」"

                        elif is_buried_5y or auto_flag_baby_born or is_mutual or is_applicant_ty or is_ty_city:
                            status_type = "常態市民價（1倍計費）"
                            final_bill = base_price
                            if auto_flag_baby_born and not is_ty_city: 
                                law_code = "第4條第1項第5款：「申請人為亡者之配偶或直系血親，且連續設籍本市滿一年以上。比照本市市民收費基準收取費用。」"
                            elif is_buried_5y and not is_ty_city: 
                                law_code = "第4條第1項第4款：「埋葬於本市公墓或公私立納骨塔、堂骨灰（骸）移出，其埋葬或存放期間達五年以上。比照本市市民收費基準收取費用。」"
                            elif is_mutual and not is_ty_city: 
                                law_code = "第4條第1項第3款：「原籍地公立納骨塔、堂與本市有公告互惠合作。比照本市市民收費基準收取費用。」"
                            elif is_applicant_ty and not is_ty_city: 
                                law_code = "第4條第1項第5款：「申請人為亡者之配偶或直系血親，且連續設籍本市滿一年以上。比照本市市民收費基準收取費用。」"
                            else: 
                                law_code = "第3條附表：「正常設籍本市之市民，依公立殯葬設施使用常態市民基準價收費。」"

                        else:
                            status_type = "常態外縣市價（3倍計費）"
                            final_bill = base_price * 3
                            law_code = "第4條第1項：「非本市市民之使用費，依基本費率之三倍計費。但符合特殊原因之一者，得比照本市市民收費基準收取費用。」"

                    # 輸出視覺面板
                    st.write("---")
                    if "全免" in status_type:
                        st.success(f"🎉 判別結果：【{status_type}】")
                    elif "外縣市" in status_type:
                        st.error(f"🚨 判別結果：【{status_type}】")
                    else:
                        st.success(f"💰 判別結果：【{status_type}】")
                        
                    st.markdown(f"**法規依據**：{law_code}")
                    
                    st.markdown(f"""
                    | 結算項目 | 金額與計費細節 |
                    | :--- | :--- |
                    | 申請設施櫃位 | {facility_type} （第 {layer_num} 層 {seq_num} 號） |
                    | 標準市民基準價 | **NT$ {base_price:,}** |
                    | 收費身份類別 | {status_type} |
                    | --- | --- |
                    | 🎯 **臨櫃實收總金額** | <span style="color:#D32F2F; font-size:24px; font-weight:900;">**NT$ {final_bill:,}**</span> |
                    """, unsafe_allow_html=True)
                    
                    if "費用全免" in status_type:
                        st.warning("💡 提示：符合「費用全免」資格者，其塔位使用位置由管理機關指定。若家屬想挑選其他特定位置，須補足差額。")