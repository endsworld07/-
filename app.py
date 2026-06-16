import streamlit as st
from datetime import datetime

st.set_page_config(page_title="桃園市觀音生命紀念園區收費判別系統", page_icon="🏢", layout="centered")

st.title("🏢 桃園市觀音生命紀念園區收費判別系統")
st.caption("版本：1150616 最新修正法規公告版 - 欄位直覺拆分優化")
st.write("---")

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
# 1. 填寫亡者基本資料（區、里拆分版）
# ==========================================
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
    birth_str = st.text_input("亡者出生年月日 (8碼數字)", placeholder="範例：19500520")
with col2:
    death_str = st.text_input("亡者死亡年月日 (8碼數字)", placeholder="範例：20260615")

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
    
    # 智慧交叉判定：如果嬰兒未設籍或外縣市，自動啟用「桃園市出生且未設籍死亡嬰兒」防呆路線
    # 只要行政區或里填無/空白，或者縣市非桃園，只要父母是桃園，即觸發
    is_baby_no_registry = "無" in district or district.strip() == "" or "無" in village or village.strip() == ""
    
    st.subheader("🍼 請填寫法定代理人（父母）資料")
    col_pcity, col_pdist, col_pvil = st.columns(3)
    with col_pcity:
        parent_city = st.text_input("法定代理人戶籍縣市", value="桃園市")
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

# 費用全免項目
is_diverse = st.checkbox("選擇使用「多元葬法專區」（如樹葬、灑葬等環保葬）")
is_low_income = st.checkbox("亡者為各縣市列冊之「低收入戶」或「中低收入戶」")
is_hero = st.checkbox("亡者為軍公教、民防、義警消「因公殉職」人員")
is_no_owner = st.checkbox("亡者身分確認為「無主墳墓」")
is_no_name = st.checkbox("亡者身分確認為「無名屍體」（且經查明確無財產者）")
is_tower_damaged = st.checkbox("原存放納骨塔設施更新或毀損無法使用")
is_body_donation = st.checkbox("大體捐贈")

# 打5折項目
is_ty_project_5y = st.checkbox("同時符合「因桃園市工程遷葬」且「埋葬桃園市公墓 5 年以上」")
is_ty_project_no_bonus = st.checkbox("屬於「桃園市工程遷葬」且「未領取」加發獎勵金者")

# 打9折項目
is_self_dig = st.checkbox("屬於桃園市禁葬公墓「自行起掘」遷葬至桃園市公立納骨塔")

# 比照市民/常態市民項目
is_buried_5y = st.checkbox("亡者已埋葬在桃園市公私立墳墓「5 年以上」或「71年以前已埋葬」")
is_mutual = st.checkbox("亡者原籍地納骨塔與桃園市有公告「互惠合作」")
is_applicant_ty = st.checkbox("來辦理的家屬（配偶/直系血親，無配偶或直系以旁系二等親亦同）連續設籍桃園滿 1 年")

st.write("---")

# ==========================================
# 4. 開始判定結果
# ==========================================
if st.button("🔍 開始自動判別收費標準", type="primary", use_container_width=True):
    if not city or not district or not village or not birth_str or not death_str:
        st.error("❌ 錯誤：請務必填寫完整縣市、行政區、里、出生與死亡年月日！")
    else:
        if age is None:
            st.error("❌ 錯誤：日期格式不正確，請精準輸入 8 位數純數字（範例：19500101）。")
        else:
            st.info(f"💡 系統自動核算：亡者死亡時精確年齡為 **{age}** 歲" + (" (⚠ 未滿一歲嬰兒)" if is_under_one else ""))
            
            # 特定里名清單（不含里字以防手動輸入差異）
            local_villages = ['大堀', '大同', '崙坪', '上大', '富源', '藍埔', '金湖', '新坡', '清華']
            
            # A. 檢查亡者本人的行政區與里
            detected_village = None
            # 確定是觀音區或新屋區才比對里
            if "觀音" in district or "新屋" in district:
                for v in local_villages:
                    if v in village:
                        detected_village = v
                        break
                    
            # B. 檢查法定代理人（父母）的行政區與里
            parent_detected_village = None
            if "觀音" in parent_district or "新屋" in parent_district:
                for v in local_villages:
                    if v in parent_village:
                        parent_detected_village = v
                        break

            # 智慧交叉判定：嬰兒本人戶籍不符，但父母符合特定里
            is_baby_local_discount = False
            if is_under_one and "桃園" in parent_city and parent_detected_village is not None:
                is_baby_local_discount = True

            # 綜合判定是否符合桃園市民基本審查路線
            is_ty = is_ty_city or detected_village is not None or auto_flag_baby_born or is_baby_local_discount

            # ==========================================
            # 判斷邏輯核心（從優攔截流）
            # ==========================================
            
            # 1. 費用全免攔截區
            if is_diverse or is_low_income or is_hero or is_no_owner or is_no_name or is_tower_damaged or is_body_donation or (is_ty and age >= 100):
                st.success("🎉 費用全免！")
                st.warning("💡 提示：符合「費用全免」資格的使用者，其塔位使用位置由管理機關指定。若家屬想挑選其他特定位置，可補足差額後使用其他位置。")
                if is_tower_damaged:
                    st.markdown("**依據**：原存放納骨塔設施更新或毀損無法使用，予以免收費用。")
                elif is_body_donation:
                    st.markdown("**依據**：符合大體捐贈免收費用之規定。")
            
            # 2. 特惠：比照市民再打 5 折
            elif is_ty_project_5y:
                st.success("🔥 特惠：直接比照市民價，再打 5 折！")
                st.markdown("**依據**：符合外縣市籍因工程遷葬且埋葬公墓5年以上之複合優待（第4條第2項）。")
            
            # 3. 桃園市民價打 5 折
            elif detected_village is not None or is_baby_local_discount or is_ty_project_no_bonus:
                if is_baby_local_discount:
                    st.success("💰 市民價打 5 折！")
                    st.markdown(f"**依據**：亡者為未滿一歲嬰兒，雖本人未設籍該里，但經系統比對，其父母（法定代理人）戶籍符合存放設施所在地特定里民（{parent_district}{parent_village}）連續設籍滿一年之優待，特予升格並減收 50%。")
                elif detected_village is not None:
                    if is_under_one: # 本人有設籍特定里，加審父母
                        if "桃園" in parent_city and parent_detected_village is not None:
                            st.success("💰 市民價打 5 折！")
                            st.markdown(f"**依據**：未滿一歲嬰兒，且父母（法定代理人）戶籍符合特定里民（{parent_district}{parent_village}）連續設籍滿一年之優待（第5條第2項第1款但書）。")
                        else:
                            st.warning("🟢 常態市民價（1 倍基準價）")
                            st.markdown(f"**依據**：亡者為未滿一歲嬰兒，雖本人設籍特定里，但因父母（法定代理人）戶籍未在特定里連續設籍滿一年，不符5折但書規定，回歸常態市民價。")
                    else:
                        st.success("💰 市民價打 5 折！")
                        st.markdown(f"**依據**：戶籍自動偵測符合桃園市特定區域（{district}{village}）之里民優待（第5條第2項第1款）。")
                else:
                    st.success("💰 市民價打 5 折！")
                    st.markdown("**依據**：屬於桃園市工程遷葬且未領取加發獎勵金者（第5條第2項第2款）。")
            
            # 4. 自行起掘打 9 折（上限一萬）
            elif is_self_dig:
                st.success("💰 市民價打 9 折！（減免上限一萬元）")
                st.markdown("**依據**：屬於桃園市禁葬公墓「自行起掘」遷葬至桃園市公立納骨塔之優待（第5條第3項）。")
            
            # 5. 比照市民 或 常態桃園市民（1倍基準價）
            elif is_buried_5y or auto_flag_baby_born or is_mutual or is_applicant_ty or is_ty_city:
                st.success("🟢 常態市民價（1 倍基準價）")
                if auto_flag_baby_born:
                    st.markdown("**依據**：系統自動判定符合第4條第1項第2款規定：亡者在桃園市出生，且於未設戶籍前死亡之嬰兒（經比對父母設籍桃園市），准予直接比照桃園市民價收費。")
                elif not is_ty_city:
                    st.markdown("**依據**：外縣市籍亡者符合特定特殊原因（如：公墓埋葬5年以上或71年前已埋葬、原籍地互惠、或來辦理的家屬連續設籍桃園滿1年），准予直接比照桃園市民價收費（第4條第1項）。")
                else:
                    st.markdown("**依據**：正常設籍桃園市之市民，依常態基準表收費。")
            
            # 6. 常態外縣市價（3倍計費）
            else:
                st.error("🚨 常態外縣市價")
                st.markdown("**說明**：不符合任何減免與比照市民資格之外縣市亡者，依規定以市民價的 3 倍計費。")