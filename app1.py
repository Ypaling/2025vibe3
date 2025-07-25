import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="연령별 남녀 인구 분석기", page_icon="👫")

st.title("👫 서울시 연령대별 남녀 인구 분석 (2025년 6월 기준)")
st.markdown("CSV 파일을 업로드하면 연령대별 남녀 인구를 시각화해줍니다.")

uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (남녀구분)", type=["csv"])

if uploaded_file is not None:
    try:
        # 인코딩 자동 처리
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding="cp949")

        # 서울시 기준 첫 번째 행만 사용
        row = df.iloc[0]

        # 연령대 남성 열 추출
        male_cols = [col for col in df.columns if "2025년06월" in col and "_남_" in col and "세" in col]
        female_cols = [col.replace("_남_", "_여_") for col in male_cols]
        ages = [col.split("_")[-1] for col in male_cols]

        # 전처리 (NaN → 0, 쉼표 제거 → 정수 변환)
        male_counts = row[male_cols].fillna(0).astype(str).str.replace(",", "").astype(int)
        female_counts = row[female_cols].fillna(0).astype(str).str.replace(",", "").astype(int)

        # 📊 DataFrame 생성
        age_df = pd.DataFrame({
            "연령": ages,
            "남자": male_counts.values,
            "여자": female_counts.values
        })

        st.subheader("📋 연령대별 남녀 인구 데이터")
        st.dataframe(age_df)

        # 📈 시각화
        age_melted = age_df.melt(id_vars="연령", var_name="성별", value_name="인구수")
        fig = px.bar(age_melted, x="연령", y="인구수", color="성별", barmode="group",
                     title="서울특별시 연령대별 남녀 인구 (2025년 6월)",
                     labels={"연령": "연령대", "인구수": "인구 수", "성별": "성별"})
        fig.update_layout(xaxis_tickangle=-45)

        st.plotly_chart(fig, use_container_width=True)

        # 다운로드
        csv = age_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 인구 데이터 CSV 다운로드", data=csv, file_name="연령별_인구.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

else:
    st.info("CSV 파일을 업로드해주세요. 예: 연령별 남녀 인구 통계")
