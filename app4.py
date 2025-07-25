import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("🚦 서울 도시고속도로 시간대별 교통량 시각화")

# CSV 경로
CSV_PATH = "서울시설공단_서울도시고속도로 노선별 시간대별 교통량_20250507.csv"

# 데이터 로딩
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH, encoding="cp949")
    return df

df = load_data()

# 도로 목록 + 전체
roads = df["노선"].unique().tolist()
roads.insert(0, "전체")

# 도로 선택
selected_road = st.selectbox("📍 도로(노선)을 선택하세요:", roads)

# ---- [상단] 선택 도로 단일 그래프 ----
st.subheader(f"📊 '{selected_road}' 시간대별 교통량")

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
fig_single.update_traces(line=dict(color="red"))
st.plotly_chart(fig_single)

# ---- [중간] 전체 vs 선택 도로 비교 ----
st.subheader("📊 전체 vs 선택 도로 교통량 비교")

total_traffic = df.groupby("시간대", as_index=False)["교통량"].sum()

if selected_road == "전체":
    selected_traffic = total_traffic.copy()
else:
    selected_traffic = df[df["노선"] == selected_road].groupby("시간대", as_index=False)["교통량"].sum()

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

# ---- [하단] 도로별 교통량 비율 그래프 ----
st.subheader("📈 도로별 전체 교통량 비율")

# 도로별 전체 교통량 합계 및 비율 계산
road_total = df.groupby("노선", as_index=False)["교통량"].sum()
overall_total = road_total["교통량"].sum()
road_total["비율(%)"] = (road_total["교통량"] / overall_total * 100).round(2)

# Plotly 막대그래프
fig_ratio = px.bar(
    road_total,
    x="노선",
    y="비율(%)",
    text="비율(%)",
    title="전체 교통량 대비 각 도로 비율 (%)",
    labels={"노선": "도로", "비율(%)": "비율 (%)"},
    template="plotly_white"
)
fig_ratio.update_traces(marker_color="green", textposition="outside")
fig_ratio.update_layout(yaxis_range=[0, road_total["비율(%)"].max() * 1.2])

st.plotly_chart(fig_ratio)
