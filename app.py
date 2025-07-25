import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import os

# -----------------------------
# 설정
# -----------------------------
st.set_page_config(page_title="나만의 북마크 지도 🗺️", page_icon="📍")
st.title("📍 지도 클릭으로 북마크 추가")
CSV_PATH = "bookmarks.csv"

# -----------------------------
# 북마크 로드 함수
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
    st.session_state.book_
