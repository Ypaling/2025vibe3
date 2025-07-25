import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("서울 도시고속도로 시간대별 교통량 비교 시각화")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="cp949")

    # 도로 목록 + 전체
    roads = df["노선"].unique().tolist()
    roads.insert(0, "전체")

    selected_road = st.selectbox("도로(노선)을 선택하세요:", roads)

    # 전체 교통량 데이터
    total_traffic = df.groupby("시간대", as_index=False)["교통량"].sum()

    # 선택 도로 데이터
    if selected_road == "전체":
        selected_traffic = total_traffic.copy()
    else:
        selected_traffic = df[df["노선"] == selected_road].groupby("시간대", as_index=False)["교통량"].sum()

    # Plotly 그래프
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=total_traffic["시간대"],
        y=total_traffic["교통량"],
        mode="lines+markers",
        name="전체 교통량",
        line=dict(color="blue")
    ))

    fig.add_trace(go.Scatter(
        x=selected_traffic["시간대"],
        y=selected_traffic["교통량"],
        mode="lines+markers",
        name=f"{selected_road} 교통량",
        line=dict(color="red")
    ))

    fig.update_layout(
        title=f"시간대별 교통량 비교 - 전체 vs {selected_road}",
        xaxis_title="시간대 (시)",
        yaxis_title="교통량 (대수)",
        template="plotly_white"
    )

    st.plotly_chart(fig)

