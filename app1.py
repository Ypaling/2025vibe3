import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 인구 분석", page_icon="📊", layout="wide")
st.title("📊 서울특별시 연령별 인구 분석 (2025년 6월 기준)")

uploaded_file = st.file_uploader("📁 CSV 파일 업로드 (전치형 구조)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except:
        df = pd.read_csv(uploaded_file, encoding="utf-8")

    # 실제 첫 번째 컬럼명이 있는 행을 기준으로 전치
    df_t = df.set_index(df.columns[0]).T.reset_index()
    df_t.columns.name = None

    # 정확한 서울시 전체 열 이름 (공백 포함!)
    seoul_total_col = "서울특별시  (1100000000)"

    if seoul_total_col not in df_t.columns:
        st.error(f"❌ '{seoul_total_col}' 열을 찾을 수 없습니다. 열 이름이 다르거나 구조가 바뀌었을 수 있어요.")
        st.write("사용 가능한 열 목록:", list(df_t.columns))
    else:
        # 연령 및 숫자 변환 처리
        df_t["연령"] = df_t.iloc[:, 0]
        df_t["전체"] = df_t[seoul_total_col].astype(str).str.replace(",", "").str.strip()
        df_t["전체"] = pd.to_numeric(df_t["전체"], errors="coerce").fillna(0).astype(int)
        df_t["연령"] = df_t["연령"].str.extract(r'(\d+세|100세 이상)').squeeze()
        df_t = df_t.dropna(subset=["연령"])

        if df_t["전체"].sum() == 0:
            st.error("❗ 숫자 변환에 실패하여 모든 인구 수가 0입니다. 원본 파일을 확인해주세요.")
        else:
            st.success("✅ 데이터 분석 성공! 아래 시각화 및 통계를 확인하세요.")

            # 그래프 시각화
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_t["연령"], y=df_t["전체"], mode='lines+markers', name='전체'))
            fig.update_layout(title='서울특별시 연령별 전체 인구수',
                              xaxis_title='연령', yaxis_title='인구수', hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)

            # 인구 많은 연령 TOP 5
            st.subheader("👑 인구 많은 연령 TOP 5")
            top5 = df_t.sort_values(by="전체", ascending=False).head(5)
            st.table(top5[["연령", "전체"]].reset_index(drop=True))

else:
    st.info("CSV 파일을 업로드해주세요.")
