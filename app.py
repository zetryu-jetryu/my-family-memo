import streamlit as st
import pandas as pd
import datetime
import requests

# 앱 설정
st.set_page_config(page_title="우리 가족 메모장", page_icon="🏠")
st.title("👨‍👩‍👧‍👦 우리 가족 공동 메모장")

# --- [설정 구간] ---
SHEET_ID = "1MbL6-1fMZTBDdn_9CfyJkjrJsoqrYMEPquMWO7Cos8o"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
FORM_URL = "https://docs.google.com/forms/d/1lUs7h2cj-LGv-0RZjPWrsCLMJmt2CTzh9kvyzV8nlV0/formResponse"

# 항목별 ID
ENTRIES = {
    "date": "entry.1691386708",
    "user": "entry.1460592934",
    "cat": "entry.348705031",
    "text": "entry.1509172605"
}
# ------------------

def load_data():
    try:
        # 캐시 방지를 위해 시간값을 파라미터로 추가
        url = f"{READ_URL}&cache={datetime.datetime.now().timestamp()}"
        return pd.read_csv(url)
    except:
        return pd.DataFrame(columns=["날짜", "작성자", "카테고리", "내용"])

# 입력 화면
with st.expander("📝 새 메모 남기기", expanded=True):
    user = st.selectbox("누구신가요?", ["아빠", "엄마", "지빈", "도빈"])
    category = st.selectbox("카테고리", ["📅 일정", "🛒 장보기", "💡 아이디어", "💬 기타"])
    content = st.text_input("내용을 입력하세요")

    if st.button("저장하기"):
        if content:
            payload = {
                ENTRIES["date"]: datetime.datetime.now().strftime("%m/%d %H:%M"),
                ENTRIES["user"]: user,
                ENTRIES["cat"]: category,
                ENTRIES["text"]: content
            }
            try:
                # ⭐️ 중요한 변경: 주소 및 데이터 전송 방식 강화
                response = requests.post(FORM_URL, data=payload, timeout=10)
                
                # 성공 시 (보통 구글은 성공 시 200번을 줍니다)
                if response.ok:
                    st.success("성공적으로 전송되었습니다!")
                    st.rerun()
                else:
                    st.error(f"전송 실패! 에러 코드: {response.status_code}")
                    st.write("설문지의 '모든 사용자 응답 허용' 설정을 다시 확인해 주세요.")
            except Exception as e:
                st.error(f"연결 오류 상세내용: {e}")

# 메모 리스트 출력
st.divider()
df = load_data()
if not df.empty:
    # '내용' 컬럼이 있는 경우만 최신순 표시
    if "내용" in df.columns:
        display_df = df.dropna(subset=['내용'])
        for i, row in display_df.iloc[::-1].head(20).iterrows():
            st.info(f"**[{row['카테고리']}] {row['내용']}** \n({row['작성자']} | {row['날짜']})")
else:
    st.write("아직 등록된 메모가 없습니다.")

