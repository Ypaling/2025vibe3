import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="나만의 북마크 지도 🗺️", page_icon="📍")

st.title("📍 나만의 북마크 지도")
st.markdown("원하는 장소를 북마크해 지도에 표시해보세요!")

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# -----------------------------
# 북마크 입력 폼
# -----------------------------
with st.form("bookmark_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("📌 장소 이름", "")
    with col2:
        description = st.text_input("📝 설명 (선택)", "")

    lat = st.number_input("위도 (Latitude)", format="%.6f", value=37.5665)
    lon = st.number_input("경도 (Longitude)", format="%.6f", value=126.9780)
    submitted = st.form_submit_button("✅ 북마크 추가")

    if submitted and name.strip():
        st.session_state.bookmarks.append({
            "name": name,
            "description": description,
            "lat": lat,
            "lon": lon
        })
        st.success(f"📍 '{name}' 이(가) 북마크에 추가되었습니다!")

# -----------------------------
# 지도 생성 및 마커 추가
# -----------------------------
# 중심 좌표: 서울
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

for bm in st.session_state.bookmarks:
    popup_text = f"<b>{bm['name']}</b><br>{bm['description']}"
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=popup_text,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

st_folium(m, width=700, height=500)

# -----------------------------
# 북마크 리스트 출력
# -----------------------------
st.markdown("### 📑 북마크 목록")
if st.session_state.bookmarks:
    df = pd.DataFrame(st.session_state.bookmarks)
    st.dataframe(df)
else:
    st.info("아직 추가된 북마크가 없습니다!")

# -----------------------------
# 초기화 버튼
# -----------------------------
if st.button("🗑️ 북마크 전체 삭제"):
    st.session_state.bookmarks = []
    st.warning("모든 북마크가 삭제되었습니다!")
