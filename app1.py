import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="서울시 연령별 인구 분석", layout="wide")

st.title("📊 서울특별시 연령별 인구 분석 (2025년 6월 기준)")

# 파일 업로드
uploaded_file = st.file_uploader("📁 '연령별인구현황_월간_합계.csv' 파일을 업로드하세요", type="csv")

if uploaded_file:
    try:
        # 데이터 로드
        df = pd.read_csv(uploaded_file, encoding='cp949')

        # 서울특별시 전체 행 추출
        seoul_total = df[df["행정구역"].str.contains("서울특별시  ", regex=False)].iloc[0]

        # 연령별 컬럼만 추출
        age_cols = [col for col in df.columns if "세" in col and "계" in col]

        # 인구 수 데이터 전처리
        age_total_values = seoul_total[age_cols].str.replace(",", "").fillna("0").astype(int)
        age_labels = [col.split("_")[-1] for col in age_cols]

        # 시각화
        st.subheader("🧒👵 연령별 인구 수")

        fig, ax = plt.subplots(figsize=(18, 6))
        ax.bar(age_labels, age_total_values, color="skyblue")
        ax.set_xlabel("연령", fontsize=12)
        ax.set_ylabel("인구 수", fontsize=12)
        ax.set_title("서울특별시 연령별 인구 수 (2025년 6월)", fontsize=16)
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # 추가 통계 분석
        st.subheader("📌 인구 구성 분석")

        young = sum(age_total_values[:15])          # 0~14세
        working = sum(age_total_values[15:65])      # 15~64세
        old = sum(age_total_values[65:])            # 65세 이상

        st.markdown(f"""
        - 🧒 **유소년 인구 (0-14세)**: {young:,}명  
        - 🧑‍💼 **생산 가능 인구 (15-64세)**: {working:,}명  
        - 👵 **고령 인구 (65세 이상)**: {old:,}명  
        """)

        # 파이 차트
        fig2, ax2 = plt.subplots()
        ax2.pie([young, working, old],
                labels=["0-14세", "15-64세", "65세 이상"],
                autopct='%1.1f%%',
                startangle=140,
                colors=["#FFD700", "#90EE90", "#FFB6C1"])
        ax2.axis('equal')
        st.pyplot(fig2)

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
else:
    st.info("⬆️ 상단에서 CSV 파일을 업로드하세요.")
