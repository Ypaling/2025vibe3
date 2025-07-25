import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from geopy.geocoders import Nominatim
import os

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="나만의 북마크 지도 🗺️", page_icon="📍")
st.title("📍 나만의 북마크 지도")
st.markdown("지도를 클릭하거나 주소를 입력해 북마크를 추가하세요!")

CSV_PATH = "bookmarks.csv"

# -----------------------------
# 북마크 로드
# -----------------------------
@st.cache_data
def load_bookmarks():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH).to_dict(orient="records")
    return []

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = load_bookmarks()

# -----------------------------
# 북마크 저장 함수
# -----------------------------
def save_bookmarks():
    df = pd.DataFrame(st.session_state.bookmarks)
    df.to_csv(CSV_PATH, index=False)

# -----------------------------
# 지도 생성
# -----------------------------
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

for bm in st.session_state.bookmarks:
    popup = f"<b>{bm['name']}</b><br>{bm['description']}"
    folium.Marker(
        location=[bm['lat'], bm['lon']],
        popup=popup,
        icon=folium.Icon(color="red", icon="bookmark")
    ).add_to(m)

st.markdown("### 🖱️ 지도를 클릭해서 북마크")
map_data = st_folium(m, width=700, height=500)

# -----------------------------
# 지도 클릭 폼
# -----------------------------
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    with st.form("clicked_form"):
        st.markdown(f"🧭 클릭한 위치: `{lat:.5f}, {lon:.5f}`")
        name = st.text_input("장소 이름", "")
        desc = st.text_input("설명 (선택)", "")
        submit = st.form_submit_button("📌 북마크 추가")
        if submit and name.strip():
            st.session_state.bookmarks.append({
                "name": name,
                "description": desc,
                "lat": lat,
                "lon": lon
            })
            save_bookmarks()
            st.success(f"✅ '{name}' 북마크 완료!")

# -----------------------------
# 주소 검색 폼
# -----------------------------
st.markdown("### 🔍 주소로 북마크 추가")
with st.form("address_form"):
    address = st.text_input("주소 입력", "")
    place_name = st.text_input("장소 이름", "")
    desc = st.text_input("설명 (선택)", "")
    submit = st.form_submit_button("📍 주소로 북마크")
    if submit and address and place_name:
        geolocator = Nominatim(user_agent="streamlit_app")
        location = geolocator.geocode(address)
        if location:
            st.session_state.bookmarks.append({
                "name": place_name,
                "description": desc,
                "lat": location.latitude,
                "lon": location.longitude
            })
            save_bookmarks()
            st.success(f"✅ '{place_name}' 북마크 완료!")
        else:
            st.error("해당 주소를 찾을 수 없습니다.")

# -----------------------------
# 북마크 목록 표시
# -----------------------------
st.markdown("### 📑 북마크 목록")
if st.session_state.bookmarks:
    df = pd.DataFrame(st.session_state.bookmarks)
    st.dataframe(df)
else:
    st.info("아직 북마크가 없습니다.")

# -----------------------------
# 초기화 버튼
# -----------------------------
if st.button("🗑️ 북마크 전체 삭제"):
    st.session_state.bookmarks = []
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
    st.warning("모든 북마크가 삭제되었습니다.")
