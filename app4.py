import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("🚦 서울 도시고속도로 시간대별 교통량 시각화")

# CSV 경로 (Streamlit 앱과 같은 폴더에 위치할 경우)
CSV_PATH = "서울시설공단_서울도시고속도로 노선별 시간대별 교통량_20250507.csv"

# CSV 직접 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH, encoding="cp949")
    return df

df = load_data()

# 노선 목록 + 전체
roads = df["노선"].unique().tolist()
roads.insert(0, "전체")

# 도로 선택
selected_road = st.selectbox("📍 도로(노선)을 선택하세요:", roads)

# ---- [상단] 선택 도로 단일 그래프 ----
st.subheader(f"📊 '{selected_road}' 시간대별 교통량 그래프")

if selected_road == "전체":
    road_df = df.groupby("시간대", as_index=False)["교통량"].sum()
else:
    road_df = df[df["노선"] == selected_road].groupby("시간대", as_index=False)["교통량"].sum()

fig_single = px.line(
    road_df,
    x="시간대",
    y="교통량",
    markers=True,
    title=f"{selected_road} 시간대별 교통량",
    labels={"시간대": "시간대 (시)", "교통량": "교통량 (대수)"},
    template="plotly_white"
)
fig_single.update_traces(line=dict(color="red"))  # 빨간색 라인
st.plotly_chart(fig_single)

# ---- [하단] 전체 vs 선택 도로 비교 그래프 ----
st.subheader("📊 전체 vs 선택 도로 교통량 비교")

# 전체 교통량 데이터
total_traffic = df.groupby("시간대", as_index=False)["교통량"].sum()

# 선택 도로 교통량 데이터
if selected_road == "전체":
    selected_traffic = total_traffic.copy()
else:
    selected_traffic = df[df["노선"] == selected_road].groupby("시간대", as_index=False)["교통량"].sum()

# Plotly 비교 그래프
fig_compare = go.Figure()

fig_compare.add_trace(go.Scatter(
    x=total_traffic["시간대"],
    y=total_traffic["교통량"],
    mode="lines+markers",
    name="전체 교통량",
    line=dict(color="blue")
))

fig_compare.add_trace(go.Scatter(
    x=selected_traffic["시간대"],
    y=selected_traffic["교통량"],
    mode="lines+markers",
    name=f"{selected_road} 교통량",
    line=dict(color="red")
))

fig_compare.update_layout(
    title=f"⏱️ 시간대별 교통량 비교: 전체 vs {selected_road}",
    xaxis_title="시간대 (시)",
    yaxis_title="교통량 (대수)",
    template="plotly_white"
)

st.plotly_chart(fig_compare)
