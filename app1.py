import streamlit as st
import pandas as pd
import os

# -----------------------------
# Streamlit 페이지 설정
# -----------------------------
st.set_page_config(page_title="📊 데이터 자동 처리기", page_icon="📂")
st.title("📤 데이터 업로드 + 자동 시각화")

# -----------------------------
# 파일 업로더
# -----------------------------
uploaded_file = st.file_uploader("📂 엑셀 또는 CSV 파일을 업로드하세요", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        file_name = uploaded_file.name
        _, ext = os.path.splitext(file_name)

        # -----------------------------
        # 파일 읽기 (확장자별 처리)
        # -----------------------------
        if ext.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(uploaded_file)
        elif ext.lower() == ".csv":
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding="cp949")
        else:
            st.error("❌ 지원하지 않는 파일 형식입니다.")
            st.stop()

        # -----------------------------
        # 데이터 미리보기
        # -----------------------------
        st.subheader("📄 원본 데이터 미리보기")
        st.dataframe(df.head())

        # -----------------------------
        # 숫자형 열만 추출하여 시각화
        # -----------------------------
        numeric_cols = df.select_dtypes(include='number').columns.tolist()

        if numeric_cols:
            st.subheader("📊 숫자형 열 시각화 (Bar Chart)")
            st.bar_chart(df[numeric_cols])
        else:
            st.info("📌 시각화할 수 있는 숫자형 열이 없습니다.")

        # -----------------------------
        # 전체 데이터 + 다운로드
        # -----------------------------
        st.subheader("✅ 전체 데이터")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 처리된 CSV 다운로드",
            data=csv,
            file_name="처리된_데이터.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

else:
    st.info("좌측에서 엑셀 또는 CSV 파일을 업로드해주세요.")
