import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 경로
FILE_PATH = "서울시_시간대별_총_교통량.csv"

# CSV 로딩
@st.cache_data
def load_data():
    df = pd.read_csv(FILE_PATH)
    return df

df = load_data()

# 페이지 제목
st.title("🛣️ 서울시 시간대별 총 교통량 분석")
st.markdown("서울시 도시고속도로의 시간대별 전체 교통량을 분석한 시각화입니다.")

# 기본 선 그래프
fig = px.line(df,
              x="시간대",
              y="교통량",
              title="시간대별 총 교통량 추이",
              labels={"시간대": "시간 (시)", "교통량": "총 교통량 (대수)"},
              markers=True)

fig.update_layout(xaxis=dict(dtick=1),  # 시간 간격 1시간
                  hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)

# 바 차트로도 시각화
st.subheader("📊 시간대별 총 교통량 (막대 차트)")
bar_fig = px.bar(df,
                 x="시간대",
                 y="교통량",
                 labels={"시간대": "시간 (시)", "교통량": "총 교통량 (대수)"},
                 text_auto=True)

bar_fig.update_layout(xaxis=dict(dtick=1),
                      bargap=0.2)

st.plotly_chart(bar_fig, use_container_width=True)

# 피크 시간대 강조
peak_hour = df.loc[df["교통량"].idxmax()]
st.success(f"🚗 교통량이 가장 많은 시간대는 **{peak_hour['시간대']}시**로, 약 **{peak_hour['교통량']:,}대**입니다.")

