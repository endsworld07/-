import streamlit as st
from datetime import datetime

st.set_page_config(page_title="桃園市納骨塔收費標準判別系統", page_icon="🏢", layout="centered")

st.title("🏢 桃園市納骨塔收費標準自動判別系統")
st.caption("版本：115年最新修正公告法規防呆版")
st.write("---")

def calculate_age(birth_str, death_str):
    try:
        birth_date = datetime.strptime(birth_str.strip(), "%Y%m%d")
        death_date = datetime.strptime(death_str.strip(), "%Y%m%d")
        age = death_date.year - birth_date.year
        if (death_date.month, death_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        is_under_one_year = (death_date - birth_date).days < 365
        return age, is_under_one_year
    except ValueError:
        return None, None

st.header("1. 填寫亡者基本資料")
col1, col2 = st.columns(2)
with col1:
    city = st.text_input("亡者死亡時所在縣市", value="桃園市")
    birth_str = st.text_input("亡者出生年月日 (YYYYMMDD)", placeholder="範例：19500520")
with col2:
    district_village = st.text_input("亡者設籍哪一區哪一里", placeholder="範例：觀音區大堀里")
    death_str = st.text_input("亡者死亡年月日 (YYYYMMDD)", placeholder="範例：20260615")

st.header("2. 填寫法定代理人資料 (選填)")
st.caption("⚠️ 僅當亡者為『未滿一歲嬰兒』時，系統才會自動啟用此區塊進行智慧判定。")
col3, col4 = st.columns(2)
with col3:
    parent_city = st.text_input("法定代理人戶籍縣市", value="桃園市")
with col4:
    parent_village = st.text_input("法定代理人哪一區哪一里", placeholder="範例：觀音區大堀里")

st.write("---")

st.header("3. 勾選符合之特殊減免條件")
st.caption("💡 依法規『多項優待應擇一申請』，若多選系統會自動攔截並挑選最優惠（免費）項目。")

st.subheader("【免收費用項目】")
is_diverse = st.checkbox("使用多元葬法專區（如樹葬、灑葬）")
is_low_income = st.checkbox("為各縣市列冊之低收入戶或中低收入戶")
is_hero = st.checkbox("為軍公教、民防、義警消因公殉職人員")
is_free_reason = st.checkbox("符合特定免收條件（無主墳/無名屍且無財產/設施毀損/大體捐贈等）")

st.subheader("【減收費用項目】")
is_ty_project_no_bonus = st.checkbox("因桃園市公墓更新或公共工程遷葬，且『未領取加發獎勵金』")
is_self_dig = st.checkbox("為桃園市各區列管禁葬公墓『自行起掘』者")

st.subheader("【外縣市籍亡者專用審查項目】")
is_buried_5y = st.checkbox("（外縣市專用）已埋葬於桃園市公私立公墓 5 年以上")
is_ty_born = st.checkbox("（外縣市專用）在桃園市出生，且於未設戶籍前死亡之嬰兒")
is_mutual = st.checkbox("（外縣市專用）原籍地之納骨塔與桃園市有公告互惠")
is_applicant_ty = st.checkbox("（外縣市專用）申請人為配偶/直系血親且連續設籍桃園市滿一年")

st.write("---")

if st.button("🔍 開始自動判別收費標準", type="primary", use_container_width=True):
    if not city or not district_village or not birth_str or not death_str:
        st.error("❌ 錯誤：請務必填寫縣市、區里、出生與死亡年月日！")
    else:
        age, is_under_one = calculate_age(birth_str, death_str)
        if age is None:
            st.error("❌ 錯誤：日期格式不正確，請輸入 8 位數純數字（範例：19500101）。")
        else:
            st.info(f"💡 系統自動核算：亡者死亡時精確年齡為 **{age}** 歲" + (" (⚠ 未滿一歲嬰兒)" if is_under_one else ""))
            
            local_villages = ['大堀', '大同', '崙坪', '上大', '富源', '藍埔', '金湖', '新坡', '清華']
            
            detected_village = None
            for v in local_villages:
                if v in district_village:
                    detected_village = v
                    break
                    
            parent_detected_village = None
            for v in local_villages:
                if v in parent_village:
                    parent_detected_village = v
                    break

            is_ty = "桃園" in city or detected_village is not None

            if is_diverse:
                st.success("🎉 【判定結果】：免收費用")
                st.markdown("**【原因依據】**：使用多元葬法專區，不分戶籍一律免收費用（第4條第3項）。")
            
            elif is_low_income or is_hero:
                st.success("🎉 【判定結果】：免收費用")
                if is_ty:
                    st.markdown("**【原因依據】**：本市籍且符合低收/中低收或因公殉職免收規定（第5條第1項第1、2款）。")
                else:
                    st.markdown("**【原因依據】**：外縣市籍低收/中低收或因公殉職，依第4條第1項第6款比照市民基準，再依第5條第1項第1款予以免收。")
            
            elif is_ty:
                if age >= 100:
                    st.success("🎉 【判定結果】：免收費用")
                    st.markdown(f"**【原因依據】**：桃園市籍且系統判定年齡達 {age} 歲，為百歲以上人瑞（第5條第1項第3款）。")
                elif is_free_reason:
                    st.success("🎉 【判定結果】：免收費用")
                    st.markdown("**【原因依據】**：符合第5條第1項之特定免收條款（無主墳、無名屍、設施毀損、大體捐贈等）。")
                elif detected_village is not None:
                    if is_under_one:
                        if "桃園" in parent_city and parent_detected_village is not None:
                            st.success("🎉 【判定結果】：減收 50%（市民價打 5 折）")
                            st.markdown(f"**【原因依據】**：未滿一歲嬰兒，且法定代理人戶籍自動偵測符合在地特定里民（{parent_detected_village}里）滿一年之優待（第5條第2項第1款但書）。")
                        else:
                            st.warning("⚠️ 【判定結果】：桃園市民常態收費（1倍基準價）")
                            st.markdown(f"**【原因依據】**：亡者為未滿一歲嬰兒，但因法定代理人戶籍（{parent_city}{parent_village}）不符合存放設施所在地特定里民滿一年之規定，故不適用5折，回歸常態市民價。")
                    else:
                        st.success("🎉 【判定結果】：減收 50%（市民價打 5 折）")
                        st.markdown(f"**【原因依據】**：區里自動偵測符合在地特定里民（{detected_village}里）之優待（第5條第2項第1款）。")
                elif is_ty_project_no_bonus:
                    st.success("🎉 【判定結果】：減收 50%（市民價打 5 折）")
                    st.markdown("**【原因依據】**：符合本市工程遷葬未領獎勵金之減免（第5條第2項第2款）。")
                elif is_self_dig:
                    st.success("🎉 【判定結果】：減收 10%（最高減新臺幣一萬元）")
                    st.markdown("**【原因依據】**：本市列管禁葬公墓自行起掘移入（第5條第3項）。")
                else:
                    st.warning("⚠️ 【判定結果】：桃園市民常態收費（1倍基準價）")
                    st.markdown("**【原因依據】**：正常設籍本市之市民，依常態基準表收費。")
            
            else:
                if is_ty_project_no_bonus and is_buried_5y:
                    st.success("🎉 【判定結果】：比照市民價後，再減收 50%（市民價打 5 折）")
                    st.markdown("**【原因依據】**：同時符合第4條第1項第四款及第五款之複合優待（第4條第2項）。")
                elif is_ty_born or is_mutual or is_applicant_ty or is_ty_project_no_bonus or is_buried_5y:
                    st.warning("⚠️ 【判定結果】：比照桃園市民基準收費（1倍價）")
                    st.markdown("**【原因依據】**：符合第4條第1項之特定比照市民條款，免除 3 倍費率。")
                else:
                    st.error("🚨 【判定結果】：常態非本市籍收費（3倍計費）")
                    st.markdown("**【原因依據】**：不符合任何減免與比照市民資格之外縣市亡者，依基本外縣市費率計費。")