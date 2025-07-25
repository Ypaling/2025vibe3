import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# -----------------------------
# 앱 기본 설정
# -----------------------------
st.set_page_config(page_title="북마크 지도", page_icon="📍")
st.title("📍 지도 클릭 + 북마크 이름 입력")

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

if "last_clicked" not in st.session_state:
    st.session_state.last_clicked = None

# -----------------------------
# 지도 만들기
# -----------------------------
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 북마크 마커 그리기
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=bm["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 렌더링
map_data = st_folium(m, width=700, height=500)

# -----------------------------
# 지도 클릭 좌표 처리
# -----------------------------
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.session_state.last_clicked = (lat, lon)

# -----------------------------
# 클릭된 위치에 이름 입력
# -----------------------------
if st.session_state.last_clicked:
    lat, lon = st.session_state.last_clicked
    st.markdown(f"🧭 클릭한 위치: `{lat:.5f}, {lon:.5f}`")

    with st.form("add_bookmark_form", clear_on_submit=True):
        name = st.text_input("북마크 이름 입력")
        submitted = st.form_submit_button("📌 북마크 추가")
        if submitted and name.strip():
            st.session_state.bookmarks.append({
                "name": name,
                "lat": lat,
                "lon": lon
            })
            st.success(f"✅ '{name}' 북마크가 추가되었습니다!")
            st.session_state.last_clicked = None
            st.experimental_rerun()

# -----------------------------
# 북마크 목록 보기
# -----------------------------
st.markdown("### 📑 북마크 목록")
if st.session_state.bookmarks:
    df = pd.DataFrame(st.session_state.bookmarks)
    st.dataframe(df)
else:
    st.info("지도 위를 클릭해 북마크를 추가하세요!")

# -----------------------------
# 초기화 버튼
# -----------------------------
if st.button("🗑️ 전체 북마크 삭제"):
    st.session_state.bookmarks = []
    st.session_state.last_clicked = None
    st.warning("모든 북마크가 삭제되었습니다.")
