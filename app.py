import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import os

# -----------------------------
# 설정
# -----------------------------
st.set_page_config(page_title="나만의 북마크 지도 🗺️", page_icon="📍")
st.title("📍 지도 클릭 + 이름 입력으로 북마크 추가")
CSV_PATH = "bookmarks.csv"

# -----------------------------
# 북마크 불러오기
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

if "last_clicked" not in st.session_state:
    st.session_state.last_clicked = None

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
    folium.Marker(
        location=[bm['lat'], bm['lon']],
        popup=bm['name'],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

map_data = st_folium(m, width=700, height=500)

# -----------------------------
# 지도 클릭 시 좌표 저장
# -----------------------------
if map_data and map_data.get("last_clicked"):
    st.session_state.last_clicked = map_data["last_clicked"]

# -----------------------------
# 폼으로 북마크 이름 입력 받기
# -----------------------------
if st.session_state.last_clicked:
    lat = st.session_state.last_clicked["lat"]
    lon = st.session_state.last_clicked["lng"]
    st.markdown(f"🧭 클릭한 위치: `{lat:.5f}, {lon:.5f}`")

    with st.form("add_bookmark_form", clear_on_submit=True):
        name = st.text_input("북마크 이름을 입력하세요", "")
        submit = st.form_submit_button("📌 북마크 추가")

        if submit and name.strip():
            # 중복 방지
            already_exists = any(
                abs(bm['lat'] - lat) < 1e-6 and abs(bm['lon'] - lon) < 1e-6
                for bm in st.session_state.bookmarks
            )
            if not already_exists:
                new_bm = {
                    "name": name,
                    "description": "",
                    "lat": lat,
                    "lon": lon
                }
                st.session_state.bookmarks.append(new_bm)
                save_bookmarks()
                st.success(f"✅ '{name}' 북마크가 추가되었습니다!")
                st.session_state.last_clicked = None
            else:
                st.warning("⚠️ 이미 이 위치에 북마크가 있습니다.")

# -----------------------------
# 북마크 목록
# -----------------------------
st.markdown("### 📑 북마크 목록")
if st.session_state.bookmarks:
    df = pd.DataFrame(st.session_state.bookmarks)
    st.dataframe(df)
else:
    st.info("현재 북마크가 없습니다.")

# -----------------------------
# 초기화 버튼
# -----------------------------
if st.button("🗑️ 북마크 전체 삭제"):
    st.session_state.bookmarks = []
    st.session_state.last_clicked = None
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
    st.warning("모든 북마크가 삭제되었습니다.")


