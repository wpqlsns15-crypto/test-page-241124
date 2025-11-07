import streamlit as st
import random
from collections import Counter
import time


st.set_page_config(page_title="주사위 굴리기", page_icon="🎲")

st.title("� 주사위 굴리기 앱")
st.write("사이드바에서 설정한 후 '굴리기' 버튼을 눌러 보세요.")

# 사이드바: 설정
st.sidebar.header("설정")
num_dice = st.sidebar.slider("주사위 개수", min_value=1, max_value=10, value=2)
sides = st.sidebar.selectbox("면 수", options=[4, 6, 8, 10, 12, 20], index=1)
use_seed = st.sidebar.checkbox("고정 시드 사용", value=False)
seed = None
if use_seed:
    seed = st.sidebar.number_input("시드 값 (정수)", value=42, step=1)

# 세션 상태: 기록 저장
if "history" not in st.session_state:
    st.session_state.history = []  # 최신 항목이 앞에 오도록 insert(0, ...)


def roll_dice(n, sides, seed=None):
    """n개의 주사위를 굴려 1..sides 사이의 정수를 리스트로 반환한다.

    seed가 주어지면 결정론적으로 굴림(같은 seed는 같은 결과)한다.
    """
    if seed is not None:
        rng = random.Random(int(seed))
        return [rng.randint(1, sides) for _ in range(n)]
    else:
        return [random.randint(1, sides) for _ in range(n)]


if st.button("🎯 굴리기"):
    rolls = roll_dice(num_dice, sides, seed if use_seed else None)
    rec = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "num": num_dice,
        "sides": sides,
        "rolls": rolls,
        "sum": sum(rolls),
        "avg": round(sum(rolls) / len(rolls), 2),
    }
    st.session_state.history.insert(0, rec)
    st.success("주사위를 굴렸습니다!")


# 최근 결과 표시
if st.session_state.history:
    latest = st.session_state.history[0]
    st.subheader("최근 결과")
    st.markdown(f"**시간:** {latest['time']}  ")
    st.markdown(f"**주사위:** {latest['num']}개  |  **면 수:** {latest['sides']}")
    st.write("개별 결과:", latest["rolls"])
    st.write("합계:", latest["sum"], "  — 평균:", latest["avg"])

    # 빈도(히스토그램)
    counts = Counter(latest["rolls"])  # face -> count
    # bar chart을 위해 정렬된 리스트로 변환
    faces = list(range(1, latest["sides"] + 1))
    values = [counts.get(f, 0) for f in faces]
    st.bar_chart({"face": faces, "count": values})
else:
    st.info("아직 굴린 기록이 없습니다. '굴리기' 버튼을 눌러보세요.")


with st.expander("모든 기록 보기"):
    if st.session_state.history:
        for i, rec in enumerate(st.session_state.history):
            st.write(f"{i+1}. [{rec['time']}] 주사위 {rec['num']}개, 면 {rec['sides']} → {rec['rolls']} (합 {rec['sum']}, 평균 {rec['avg']})")
    else:
        st.write("기록이 없습니다.")


# 기록 초기화
if st.button("기록 초기화"):
    st.session_state.history = []
    st.info("기록을 초기화했습니다.")

