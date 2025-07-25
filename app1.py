import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="👫 연령별 남녀 인구 분석기", page_icon="👫")
st.title("👫 서울시 연령대별 남녀 인구 분석기 (CSV 업로드 기반)")

uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (남녀 구분)", type=["csv"])

if uploaded_file is not None:
    try:
        # ================================
        # 1. 인코딩 자동 감지
        # ================================
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding="cp949")

        # ================================
        # 2. 데이터 미리보기 & 구조 확인
        # ================================
        st.subheader("✅ 원본 데이터 미리보기")
        st.write("열 이름:", df.columns.tolist())
        st.write("총 행 수:", df.shape[0])
        st.dataframe(df.head())

        # ================================
        # 3. 연령별 남녀 열 자동 탐색
        # ================================
        male_cols = [col for col in df.columns if "남" in col and "세" in col]
        female_cols = [col for col in df.columns if "여" in col and "세" in col]

        if not male_cols or not female_cols:
            st.error("❌ '남' 또는 '여' 열이 자동으로 인식되지 않았습니다.")
            st.stop()

        # 서울특별시 기준 첫 행 사용 (또는 원하는 지역 선택 기능 추가 가능)
        row = df.iloc[0]

        # 연령 추출 (열 이름에서 '0세', '1세', ..., '100세 이상' 부분만)
        ages = [col.split("_")[-1] for col in male_cols]

        # 값 전처리: 쉼표 제거 + NaN → 0 → int 변환
        male_counts = row[male_cols].fillna(0).astype(str).str.replace(",", "").astype(int)
        female_counts = row[female_cols].fillna(0).astype(str).str.replace(",", "").astype(int)

        # ================================
        # 4. 데이터프레임 구성 및 출력
        # ================================
        age_df = pd.DataFrame({
            "연령": ages,
            "남자": male_counts.values,
            "여자": female_counts.values
        })

        st.subheader("📊 연령대별 남녀 인구 데이터")
        st.dataframe(age_df)

        # ================================
        # 5. Plotly 시각화
        # ================================
        melted = age_df.melt(id_vars="연령", var_name="성별", value_name="인구수")

        fig = px.bar(
            melted,
            x="연령", y="인구수", color="성별", barmode="group",
            title="서울특별시 연령대별 남녀 인구",
            labels={"연령": "연령대", "인구수": "인구 수", "성별": "성별"}
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        # ================================
        # 6. CSV 다운로드
        # ================================
        csv = age_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 분석 결과 CSV 다운로드", data=csv, file_name="연령대별_남녀_인구.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

else:
    st.info("👆 왼쪽에서 CSV 파일을 업로드해주세요.")

