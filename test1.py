import streamlit as st
import random

# -------------------------------
# 페이지 설정
# -------------------------------
st.set_page_config(page_title="가위바위보 게임", page_icon="✌️")
st.title("✊✋✌️ 가위바위보 게임 ✨")

# -------------------------------
# 세션 상태 초기화
# -------------------------------
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0
if "draws" not in st.session_state:
    st.session_state.draws = 0
if "total_games" not in st.session_state:
    st.session_state.total_games = 0

# -------------------------------
# 사용자 입력
# -------------------------------
st.markdown("## 당신의 선택은?")
user_choice = st.radio("👇 아래에서 선택하세요!", ("✊ 가위", "✋ 바위", "✌️ 보"))

if st.button("🎮 대결 시작!"):
    choices = {"✊ 가위": "scissors", "✋ 바위": "rock", "✌️ 보": "paper"}
    reverse_choices = {v: k for k, v in choices.items()}

    user = choices[user_choice]
    computer = random.choice(["scissors", "rock", "paper"])
    computer_display = reverse_choices[computer]

    st.write(f"🤖 **컴퓨터의 선택:** {computer_display}")

    # 게임 판정
    if user == computer:
        st.session_state.draws += 1
        st.session_state.total_games += 1
        st.info("❓ 비겼습니다!")
    elif (user == "scissors" and computer == "paper") or \
         (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock"):
        st.session_state.wins += 1
        st.session_state.total_games += 1
        st.balloons()
        st.success("👏 당신이 이겼습니다!")
    else:
        st.session_state.losses += 1
        st.session_state.total_games += 1
        st.error("😢 졌습니다...")

# -------------------------------
# 결과 요약 표시
# -------------------------------
st.markdown("## 📊 전적 요약")
wins = st.session_state.wins
losses = st.session_state.losses
draws = st.session_state.draws
total = st.session_state.total_games

if total > 0:
    win_rate = (wins / total) * 100
else:
    win_rate = 0.0

st.write(f"✅ 이긴 횟수: {wins}")
st.write(f"❌ 진 횟수: {losses}")
st.write(f"🔁 비긴 횟수: {draws}")
st.write(f"🎮 총 경기 수: {total}")
st.write(f"🏆 승률: **{win_rate:.2f}%**")

# -------------------------------
# 초기화 버튼
# -------------------------------
if st.button("🔄 기록 초기화"):
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.draws = 0
    st.session_state.total_games = 0
    st.success("기록이 초기화되었습니다!")

# -------------------------------
# 푸터
# -------------------------------
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")



