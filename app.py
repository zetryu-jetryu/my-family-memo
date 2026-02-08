import streamlit as st
import pandas as pd
import datetime
import requests

# 앱 설정
st.set_page_config(page_title="우리 가족 메모장", page_icon="🏠")
st.title("👨‍👩‍👧‍👦 우리 가족 공동 메모장")

# --- [설정 구간] ---
# 1. 읽기용: 구글 시트 CSV 주소 (본인 시트 ID 확인)
SHEET_ID = "1MbL6-1fMZTBDdn_9CfyJkjrJsoqrYMEPquMWO7Cos8o"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# 2. 쓰기용: 구글 설문지 제출 주소 (알려주신 주소 기반)
FORM_URL = "https://docs.google.com/forms/d/1lUs7h2cj-LGv-0RZjPWrsCLMJmt2CTzh9kvyzV8nlV0/formResponse"

# 3. 항목별 ID (제가 찾아드린 번호입니다)
ENTRIES = {
    "date": "entry.1691386708",
    "user": "entry.1460592934",
    "cat": "entry.348705031",
    "text": "entry.1509172605"
}
# ------------------

# 데이터 로드 함수 (시트에서 읽어오기만 함)
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
            # 설문지로 데이터 전송 (이게 '쓰기' 역할을 대신합니다)
            payload = {
                ENTRIES["date"]: datetime.datetime.now().strftime("%m/%d %H:%M"),
                ENTRIES["user"]: user,
                ENTRIES["cat"]: category,
                ENTRIES["text"]: content
            }
            try:
                response = requests.post(FORM_URL, data=payload)
                if response.status_code == 200:
                    st.success("성공적으로 전송되었습니다!")
                    st.rerun()
                else:
                    st.error("전송에 실패했습니다. 설문지 설정을 확인하세요.")
            except:
                st.error("연결 오류가 발생했습니다.")

# 메모 리스트 출력
st.divider()
df = load_data()
if not df.empty:
    # 최신순으로 20개만 표시 (내용이 있는 것만)
    display_df = df.dropna(subset=['내용'])
    for i, row in display_df.iloc[::-1].head(20).iterrows():
        st.info(f"**[{row['카테고리']}] {row['내용']}** \n({row['작성자']} | {row['날짜']})")
else:
    st.write("아직 등록된 메모가 없거나 불러오는 중입니다.")
