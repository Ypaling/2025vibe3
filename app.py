import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import os

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="나만의 북마크 지도 🗺️", page_icon="📍")
st.title("📍 지도 클릭으로 북마크 추가")
CSV_PATH = "bookmarks.csv"

# -----------------------------
# 북마크 불러오기 함수
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

if "bookmark_count" not in st.session_state:
    st.session_state.bookmark_count = len(st.session_state.bookmarks)

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

# 북마크 마커 추가
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm['lat'], bm['lon']],
        popup=bm['name'],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 표시 + 클릭 정보 가져오기
map_data = st_folium(m, width=700, height=500)

# -----------------------------
# 지도 클릭 시 북마크 자동 추가
# -----------------------------
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    # 중복 체크: 같은 위치가 이미 있는지
    already_exists = any(
        abs(bm['lat'] - lat) < 1e-6 and abs(bm['lon'] - lon) < 1e-6
        for bm in st.session_state.bookmarks
    )

    if not already_exists:
        st.session_state.bookmark_count += 1
        name = f"북마크 {st.session_state.bookmark_count}"

        new_bm = {
            "name": name,
            "description": "",
            "lat": lat,
            "lon": lon
        }
        st.session_state.bookmarks.append(new_bm)
        save_bookmarks()
        st.success(f"🆕 '{name}' 이 추가되었습니다!")

# -----------------------------
# 북마크 목록 보기
# -----------------------------
st.markdown("### 📑 북마크 목록")
if st.session_state.bookmarks:
    df = pd.DataFrame(st.session_state.bookmarks)
    st.dataframe(df)
else:
    st.info("현재 북마크가 없습니다. 지도를 클릭해서 추가해보세요!")

# -----------------------------
# 초기화 버튼
# -----------------------------
if st.button("🗑️ 북마크 전체 삭제"):
    st.session_state.bookmarks = []
    st.session_state.bookmark_count = 0
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
    st.warning("모든 북마크가 삭제되었습니다.")
