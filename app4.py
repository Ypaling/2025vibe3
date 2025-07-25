import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("서울시설공단_서울도시고속도로 노선별 시간대별 교통량_20250507.csv", encoding="cp949")
    return df

df = load_data()

# 노선 목록 + "전체"
roads = df["노선"].unique().tolist()
roads.insert(0, "전체")

# 사용자 선택
selected_road = st.selectbox("도로(노선)을 선택하세요:", roads)

# 선택된 도로 기준 데이터 필터링
if selected_road == "전체":
    filtered_df = df.groupby("시간대", as_index=False)["교통량"].sum()
else:
    filtered_df = df[df["노선"] == selected_road].groupby("시간대", as_index=False)["교통량"].sum()

# Plotly 그래프
fig = px.line(
    filtered_df,
    x="시간대",
    y="교통량",
    markers=True,
    labels={"시간대": "시간대 (시)", "교통량": "교통량 (대수)"},
    title=f"{selected_road} 시간대별 교통량"
)

# Streamlit 출력
st.title("서울 도시고속도로 시간대별 교통량 시각화")
st.plotly_chart(fig)
