import streamlit as st
import random

# -------------------------------
# 설정
# -------------------------------
st.set_page_config(page_title="가위바위보 게임", page_icon="✌️")
st.title("✊✋✌️ 가위바위보 게임 ✨")

st.markdown("## 당신의 선택은?")
user_choice = st.radio("👇 아래에서 선택하세요!", ("✊ 가위", "✋ 바위", "✌️ 보"))

if st.button("🎮 대결 시작!"):
    choices = {"✊ 가위": "scissors", "✋ 바위": "rock", "✌️ 보": "paper"}
    reverse_choices = {v: k for k, v in choices.items()}

    user = choices[user_choice]
    computer = random.choice(["scissors", "rock", "paper"])
    computer_display = reverse_choices[computer]

    st.write(f"🤖 컴퓨터의 선택: {computer_display}")

    # 게임 로직
    if user == computer:
        st.success("❓ 비겼습니다!")
    elif (user == "scissors" and computer == "paper") or \
         (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock"):
        st.balloons()
        st.success("👏 당신이 이겼습니다!")
    else:
        st.error("😢 졌습니다...")

# 푸터
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")

