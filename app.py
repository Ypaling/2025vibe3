import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="나만의 북마크 지도 🗺️", page_icon="📍")
st.title("📍 나만의 북마크 지도")
st.markdown("지도를 클릭해 북마크를 추가해보세요!")

# -----------------------------
# 세션 초기화
# -----------------------------
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# -----------------------------
# 지도 만들기 (기본: 서울)
# -----------------------------
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 기존 북마크 마커 표시
for bm in st.session_state.bookmarks:
    popup_text = f"<b>{bm['name']}</b><br>{bm['description']}"
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=popup_text,
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 클릭한 위치 가져오기
st.markdown("### 🖱️ 지도를 클릭해 위치를 추가하세요")
map_data = st_folium(m, width=700, height=500)

# -----------------------------
# 클릭한 좌표가 있을 경우 입력 폼 표시
# -----------------------------
if map_data and map_data["last_clicked"]:
    clicked_lat = map_data["last_clicked"]["lat"]
    clicked_lon = map_data["last_clicked"]["lng"]
    
    with st.form("add_clicked_point"):
        st.markdown(f"**📌 클릭한 위치:** 위도 {clicked_lat:.6f}, 경도 {clicked_lon:.6f}")
        name = st.text_input("장소 이름", "")
        description = st.text_input("설명 (선택)", "")
        submit = st.form_submit_button("✅ 북마크 추가")

        if submit and name.strip():
            st.session_state.bookmarks.append({
                "name": name,
                "description": description,
                "lat": clicked_lat,
                "lon": clicked_lon
            })
            st.success(f"'{name}' 이(가) 북마크에 추가되었습니다!")

# -----------------------------
# 북마크 목록 출력
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
    st.warning("모든 북마크가 삭제되었습니다!")
