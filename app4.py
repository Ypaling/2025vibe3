import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("/mnt/data/서울시설공단_서울도시고속도로 노선별 시간대별 교통량_20250507.csv", encoding="cp949")
    return df

df = load_data()

# 노선 목록 + 전체
roads = df["노선"].unique().tolist()
roads.insert(0, "전체")

# 사용자 선택
selected_road = st.selectbox("도로(노선)을 선택하세요:", roads)

# 전체 데이터 (시간대별 합계)
total_traffic = df.groupby("시간대", as_index=False)["교통량"].sum()

# 선택 도로 데이터
if selected_road == "전체":
    selected_traffic = total_traffic.copy()
else:
    selected_traffic = df[df["노선"] == selected_road].groupby("시간대", as_index=False)["교통량"].sum()

# Plotly 그래프 객체 생성
fig = go.Figure()

# 전체 교통량 - 파란색
fig.add_trace(go.Scatter(
    x=total_traffic["시간대"],
    y=total_traffic["교통량"],
    mode="lines+markers",
    name="전체 교통량",
    line=dict(color="blue")
))

# 선택된 도로 교통량 - 빨간색
fig.add_trace(go.Scatter(
    x=selected_traffic["시간대"],
    y=selected_traffic["교통량"],
    mode="lines+markers",
    name=f"{selected_road} 교통량",
    line=dict(color="red")
))

# 레이아웃 설정
fig.update_layout(
    title=f"시간대별 교통량 비교 - 전체 vs {selected_road}",
    xaxis_title="시간대 (시)",
    yaxis_title="교통량 (대수)",
    template="plotly_white"
)

# Streamlit 출력
st.title("서울 도시고속도로 시간대별 교통량 비교")
st.plotly_chart(fig)
