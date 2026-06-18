import streamlit as st
from datetime import datetime

# 設定網頁標題與排版佈局
st.set_page_config(page_title="桃園市觀音生命紀念園區收費標準", page_icon="🏢", layout="centered")

# ==========================================
# 🎨 終極視覺優化區
# ==========================================
st.markdown("""
    <style>
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
    .stWidgetLabel p, p, label, .stToggle p {
        color: #111111 !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
    }
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
    div[data-baseweb="popover"] ul, div[data-baseweb="menu"] li, div[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }
    div[data-baseweb="menu"] li:hover {
        background-color: #D6E4F0 !important;
        color: #000000 !important;
    }
    h1 { 
        color: #1E3D59 !important; 
        font-weight: 800 !important; 
        font-size: calc(18px + 1vw) !important; 
        line-height: 1.3 !important;
        word-break: keep-all !important;
        text-align: left !important;
        margin-bottom: 5px !important; 
    }
    h2 { color: #1E3D59 !important; font-size: 21px !important; font-weight: 700 !important; border-bottom: 2px solid #1E3D59; padding-bottom: 6px; margin-top: 30px !important; }
    
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
# 核心邏輯運算區
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

st.title("🏢 桃園市觀音生命紀念園區收費標準")
st.write("---")

# ==========================================
# 1. 填寫亡者基本資料
# ==========================================
st.header("1. 檢查亡者戶籍等相關資料")

city = st.selectbox("亡者除戶所在縣市", ["桃園市", "外縣市"])
is_ty_city = (city == "桃園市")

district = ""
village = ""

if is_ty_city:
    col_dist, col_vil = st.columns(2)
    with col_dist: district = st.text_input("亡者設籍行政區", placeholder="如：觀音區、新屋區")
    with col_vil: village = st.text_input("亡者設籍里", placeholder="如：大堀里、清華里")

col_b, col_d = st.columns(2)
with col_b: birth_str = st.text_input("亡者出生年月日 (民國7碼)", placeholder="如：0390520")
with col_d: death_str = st.text_input("亡者死亡年月日 (民國7碼)", placeholder="如：1150615")

age, is_under_one = calculate_age_roc(birth_str, death_str)

# 外縣市案件動態觸發審查
applicant_relation = "無需審查"
is_no_closer_kin = False
is_applicant_ty_1y = False

if not is_ty_city:
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
        has_closer_kin = st.radio("亡者是否有配偶或直系血親？", ["有", "無"], index=0)
        if has_closer_kin == "無":
            is_no_closer_kin = True
            st.success("💡 審查提示：已確認亡者無配偶及直系血親，符合旁系二等親代之申請資格。請確認下方申請人設籍是否滿一年。")
            is_applicant_ty_1y = st.toggle("申請人（旁系二等親家屬）是否已「連續設籍桃園市滿一年以上」？")
        else:
            is_no_closer_kin = False
            st.error("🚨 審查結果：不符合第4條第1項第2款資格！（因亡者尚有配偶或直系血親，旁系二等親家屬無法免除限制比照市民價）。")
    elif applicant_relation == "其他親屬/無親屬關係":
        st.error("🚨 審查結果：不符合第4條第1項第2款資格！（非特定家屬身份，無法適用家屬設籍優待條款）。")

# 未滿一歲嬰兒代理人審查
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

is_diverse = is_low_income = is_hero = is_no_owner = is_no_name = is_tower_damaged = is_project_free = is_special_gov = is_body_donation = False
is_ty_project_no_bonus = is_out_project_move = is_self_dig = is_buried_5y = is_mutual = False

if facility_type == "牌位":
    st.caption("💡 提示：目前選擇【牌位】，法規規定牌位為常態固定收費，不適用任何特殊減免優待。")
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
    
    if is_ty_city:
        is_ty_project_no_bonus = st.toggle("10. 桃園市籍亡者因桃園市公墓更新、公共工程或都市發展辦理搬遷，未領取「加發獎勵金」")
        
    if not is_ty_city:
        is_out_project_move = st.toggle("11. 外縣市籍亡者，因桃園市公墓更新、公共工程或都市發展，未領取「加發獎勵金」")
    
    is_self_dig = st.toggle("12. 屬於桃園市禁葬公墓「自行起掘」遷葬至桃園市公立納骨塔")
    is_buried_5y = st.toggle("13. 亡者已埋葬於桃園市公、私立公墓5年以上，或墳墓設置條例施行前已埋葬桃園市土地，經戶政查詢無亡者戶籍資料者")
    is_mutual = st.toggle("14. 桃園市籍亡者收費與外縣市公立納骨塔市民相同收費，並經桃園市政府公告互惠者")

    # 🛸 智慧解析代理人(父母)身分
    local_villages = ['大堀', '大同', '崙坪', '上大', '富源', '藍埔', '金湖', '新坡', '清華']
    detected_village = next((v for v in local_villages if v in village), None) if ("觀音" in district or "新屋" in district) else None
    parent_detected_village = next((v for v in local_villages if v in parent_village), None) if ("觀音" in parent_district or "新屋" in parent_district) else None
    
    # 🌟 修正漏洞：只要是未滿一歲嬰兒且父母設籍特定里，不論嬰兒本身是桃園或外縣市出生除戶，皆享5折
    is_baby_local_discount = True if (is_under_one and parent_detected_village) else False
    is_ty = is_ty_city or detected_village or auto_flag_baby_born or is_baby_local_discount or ("桃園" in parent_city)

    is_free_triggered = (is_diverse or is_low_income or is_hero or is_no_owner or is_no_name or is_tower_damaged or is_project_free or is_special_gov or is_body_donation or (is_ty and age is not None and age >= 100))
    
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
            detected_village = next((v for v in local_villages if v in village), None) if ("觀音" in district or "新屋" in district) else None
            parent_detected_village = next((v for v in local_villages if v in parent_village), None) if ("觀音" in parent_district or "新屋" in parent_district) else None
            
            # 🌟 雙重對齊：確保不論選桃園或外縣市，未滿一歲嬰兒條款皆能打穿限制
            is_baby_local_discount = True if (is_under_one and parent_detected_village) else False
            is_both_out_project_matched = True if (is_out_project_move and is_buried_5y) else False
            is_baby_citizen_discount = True if (is_under_one and "桃園" in parent_city and not parent_detected_village) else False

            status_type = ""
            law_code = ""
            final_bill = 0
            is_free_case = False
            
            # 🚀 第一步：推算此案件的常態收費折數
            discount_ratio = 1.0
            discount_reason = "常態市民價"
            
            if facility_type != "牌位":
                if is_baby_local_discount or detected_village or is_ty_project_no_bonus or is_both_out_project_matched:
                    discount_ratio = 0.5
                    discount_reason = "特定里民/工程減收50%優待價"
                elif is_self_dig:
                    discount_ratio = 0.9
                    discount_reason = "自行起掘減收10%優待價"
                elif is_ty_city or auto_flag_baby_born or is_baby_citizen_discount or is_out_project_move or is_buried_5y or is_mutual or (not is_ty_city and is_applicant_ty_1y and (applicant_relation in ["配偶", "直系血親"] or (applicant_relation == "旁系血親二等親以內" and is_no_closer_kin))):
                    discount_ratio = 1.0
                    discount_reason = "常態市民價"
                else:
                    discount_ratio = 3.0
                    discount_reason = "常態外縣市價（3倍計費）"

            # 🚀 第二步：依大分流計算「指定位置」的常態實收
            if facility_type == "牌位":
                status_type = "常態牌位價"
                final_bill = 35000
                law_code = "無（牌位屬常態固定設施，不開放特殊優待）"
            else:
                # 1. 費用全免大分流
                if is_diverse or is_low_income or is_hero or is_no_owner or is_no_name or is_tower_damaged or is_project_free or is_special_gov or is_body_donation or ( (is_ty_city or detected_village or auto_flag_baby_born or is_baby_local_discount or ("桃園" in parent_city)) and age >= 100 ):
                    status_type = "費用全免"
                    final_bill = 0
                    is_free_case = True
                    if is_diverse: law_code = "第4條第3項：「非本市市民使用多元葬法專區，免收費用。」"
                    elif is_low_income: law_code = "第5條第1項第1款：「各縣市列冊之低收入戶及中低收入戶成員死亡免收費用。」"
                    elif is_hero: law_code = "第5條第1項第2款：「軍公教人員、民防人員、義警、義消或其他依法令從事公務因公殉職人員免收費用。」"
                    elif age >= 100: law_code = "第5條第1項第3款：「本市籍百歲以上人瑞，免收費用。」"
                    elif is_no_owner: law_code = "第5條第1項打4款：「依法應行遷葬之無主墳墓，免收費用。」"
                    elif is_no_name: law_code = "第5條第1項第5款：「無名屍體、無人認領之屍體或無遺囑且無遺產者，免收費用。」"
                    elif is_tower_damaged: law_code = "第5條第1項第6款：「原存放桃園市公立納骨塔因更新或毀損無法繼續使用，免收費用。」"
                    elif is_project_free: law_code = "第5條第1項第7款：「不分本市或外縣市亡者，因桃園市公墓更新、公共工程或都市發展辦理搬遷，未領取遷葬補償費或救濟金者，免收費用。」"
                    elif is_special_gov: law_code = "第5條第1項第8款：「因天災、事變、不可抗力或特殊原因死亡或家屬生活陷於困難，經桃園市政府專案核准者，免收費用。」"
                    elif is_body_donation: law_code = "第5條第1項第9款：「醫療院所捐贈器官或遺體，免收費用。」"
                    
                # 2. 市民價 5 折分流
                elif discount_ratio == 0.5:
                    final_bill = int(base_price * 0.5)
                    if is_baby_local_discount: 
                        status_type = "特定里代理人優待價（市民價打 5 折）"
                        law_code = "第5條第2項第1款但書：「設籍觀音區、新屋區特定里民連續設籍滿一年以上者減收百分之五十。未滿一歲嬰兒，其法定代理人符合前段規定者，亦同。」"
                    elif detected_village:
                        status_type = "特定里民優待價（市民價打 5 折）"
                        law_code = "第5條第2項第1款：「設籍觀音區、新屋區特定里民連續設籍滿一年以上者，減收百分之五十。」"
                    elif is_ty_project_no_bonus: 
                        status_type = "工程搬遷優待價（市民價打 5 折）"
                        law_code = "第5條第2項第2款：「桃園市籍亡者因桃園市公墓更新、公共工程或都市發展辦理搬遷，未領取『加發獎勵金』，減收百分之五十。」"
                    elif is_both_out_project_matched:
                        status_type = "外縣市雙重條件特惠價（市民價再打 5 折）"
                        law_code = "第4條第2項：「外縣市籍亡者同時符合第1項第4款及第5款規定之情形者，除依照桃園市民收費基準外得申請減收50%費用。」"

                # 3. 市民價 9 折分流
                elif discount_ratio == 0.9:
                    status_type = "市民價打 9 折（自行起掘）"
                    final_bill = base_price - min(int(base_price * 0.1), 10000)
                    law_code = "第5條第3項：「屬於桃園市禁葬公墓自行起掘移入者，減收百分之十，最高上限一萬元。」"

                # 4. 常態市民價分流
                elif discount_ratio == 1.0:
                    status_type = "常態市民價（1倍計費）"
                    final_bill = base_price
                    if is_baby_citizen_discount:
                        status_type = "未滿一歲嬰兒代理人比照市民價"
                        law_code = "第4條第1項第2款延伸：嬰兒設籍前死亡，其法定代理人連續設籍本市滿一年以上，比照市民價收費。"
                    elif is_out_project_move:
                        law_code = "第4條第1項第4款：「外縣市籍亡者，因桃園市公墓更新、公共工程或都市發展，未領取『加發獎勵金』，比照本市市民收費基準收取費用。」"
                    elif not is_ty_city and is_applicant_ty_1y: 
                        law_code = "第4條第1項第2款：「申請人為亡者之配偶或直系血親，且連續設籍本市滿一年以上，比照本市市民收費基準收取費用。」"
                    elif auto_flag_baby_born and not is_ty_city: 
                        law_code = "第4條第1項第5款：「本市出生之嬰兒於未設戶籍前死亡，比照本市市民收費基準收取費用。」"
                    elif is_buried_5y and not is_ty_city: 
                        law_code = "第4條第1項第5款：「亡者已埋葬於桃園市公墓5年以上，比照本市市民收費基準收取費用。」"
                    elif is_mutual and not is_ty_city: 
                        law_code = "第4條第1項第1款：「經桃園市政府公告互惠者，比照本市市民收費基準收取費用。」"
                    else: 
                        law_code = "第3條附表：「設籍本市之市民常態收費基準。」"

                # 5. 外縣市三倍計費分流
                else:
                    status_type = "常態外縣市價（3倍計費）"
                    final_bill = base_price * 3
                    law_code = "第4條第1項：「非本市市民之使用費，依基本費率之三倍計費。」"

            # 🚀 第三步：🌟 【徹底修正 Bug】費用全免者辦理補足差額計算引擎
            is_upgrade_error = False
            display_base_price = base_price 
            
            if is_free_case and want_upgrade and target_cab.strip():
                t_price, t_msg = get_base_price(facility_type, target_cab)
                if t_msg == "正常":
                    # 依據法意：指定位置免收（價值等同原指定位置市民價）。
                    # 家屬自選新櫃位時，應繳金額 =「（自選新櫃位市民價 - 原指定位置市民價）× 其原本應適用的身分折數比例」
                    price_diff_市民 = t_price - base_price
                    
                    if price_diff_市民 <= 0:
                        final_bill = 0 # 若自選位置價值等於或小於原指定位置，差額為0
                    else:
                        if discount_ratio == 0.9:
                            final_bill = price_diff_市民 - min(int(price_diff_市民 * 0.1), 10000)
                        elif discount_ratio == 3.0:
                            # 即使外縣市身份符合全免（如無主墓、公共工程），自選升級亦依外縣市3倍補差額
                            final_bill = price_diff_市民 * 3
                        else:
                            final_bill = int(price_diff_市民 * discount_ratio)
                            
                    status_type = f"費用全免（已辦理第5條第6項補足自選差額 ｜ 特惠連動身份：{discount_reason}）"
                    display_base_price = t_price 
                else:
                    is_upgrade_error = True
                    if t_msg == "編號違規": st.error("❌ 錯誤：自選新櫃位號碼違規，無法進行差額計算！")
                    elif t_msg == "層級衝突": st.error("❌ 錯誤：自選新櫃位層級與設施種類衝突！")

            if not is_upgrade_error:
                st.write("---")
                st.success(f"💰 判別結果：【{status_type}】")
                st.markdown(f"**法規依據**：{law_code}")
                
                if is_free_case and want_upgrade and target_cab.strip():
                    st.markdown(f"### 🧮 補足自選差額精密明細：")
                    st.markdown(f"* 管理機關指定原櫃位市民價：`NT$ {base_price:,}` (此基準完全免收)")
                    st.markdown(f"* 家屬自選新櫃位（第 {int(target_cab[0:2])} 層）市民價：`NT$ {t_price:,}`")
                    st.markdown(f"* ⚖️ **純網頁級距差額（市民價差）**：`NT$ {t_price - base_price:,}`")
                    if discount_ratio != 1.0:
                        st.markdown(f"* 🌟 **身份折減同步連動**：此家屬身分同時符合 `{discount_reason}`，自選升級差額部分同步享折減優惠！")

                st.markdown(f"""
                | 結算項目 | 金額與計費細節 |
                | :--- | :--- |
                | 申請設施櫃位 | {facility_type} （第 {layer_num} 層 {seq_num} 號） |
                | 當前計算基準價 | **NT$ {display_base_price:,}** |
                | 收費身份類別 | {status_type} |
                | --- | --- |
                | 🎯 **臨櫃實收總金額** | <span style="color:#D32F2F; font-size:24px; font-weight:900;">**NT$ {final_bill:,}**</span> |
                """, unsafe_allow_html=True)