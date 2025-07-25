import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import os

# -----------------------------
# Firebase 초기화
# -----------------------------
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")  # ← Firebase 키 JSON 파일 경로
    firebase_admin.initialize_app(cred)
db = firestore.client()

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="공유 북마크 지도", page_icon="📍")
st.title("📍 Firebase 기반 공유 북마크 지도")

# -----------------------------
# Firestore 북마크 가져오기
# -----------------------------
@st.cache_data(ttl=30)
def get_bookmarks():
    docs = db.collection("bookmarks").stream()
    return [
        {
            "id": doc.id,
            **doc.to_dict()
        }
        for doc in docs
    ]

# -----------------------------
# 북마크 저장 함수
# -----------------------------
def add_bookmark(name, lat, lon):
    doc = {
        "name": name,
        "lat": lat,
        "lon": lon
    }
    db.collection("bookmarks").add(doc)

def delete_all_bookmarks():
    docs = db.collection("bookmarks").stream()
    for doc in docs:
        db.collection("bookmarks").document(doc.id).delete()

# -----------------------------
# 지도 생성
# -----------------------------
bookmarks = get_bookmarks()
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

for bm in bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=bm["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

st.markdown("### 🖱️ 지도를 클릭해 북마크 추가")

map_data = st_folium(m, width=700, height=500)

# -----------------------------
# 클릭한 위치에 북마크 이름 입력
# -----------------------------
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.markdown(f"🧭 클릭한 위치: `{lat:.5f}, {lon:.5f}`")

    with st.form("bookmark_form", clear_on_submit=True):
        name = st.text_input("북마크 이름 입력")
        submitted = st.form_submit_button("📌 북마크 추가")
        if submitted and name.strip():
            add_bookmark(name, lat, lon)
            st.success(f"✅ '{name}' 북마크 추가 완료!")
            st.experimental_rerun()

# -----------------------------
# 북마크 목록
# -----------------------------
st.markdown("### 📑 북마크 목록")
if bookmarks:
    df = pd.DataFrame(bookmarks)[["name", "lat", "lon"]]
    st.dataframe(df)
else:
    st.info("아직 북마크가 없습니다.")

# -----------------------------
# 초기화 버튼
# -----------------------------
if st.button("🗑️ 북마크 전체 삭제"):
    delete_all_bookmarks()
    st.warning("모든 북마크가 삭제되었습니다.")
    st.experimental_rerun()
