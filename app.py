import streamlit as st
import pandas as pd
import datetime
import requests

# 1. 기본 설정
st.set_page_config(page_title="우리 가족 메모장", page_icon="🏠")
st.title("👨‍👩‍👧‍👦 우리 가족 공동 메모장")

# 2. 설정 구간
SHEET_ID = "1MbL6-1fMZTBDdn_9CfyJkjrJsoqrYMEPquMWO7Cos8o"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
FORM_URL = "https://docs.google.com/forms/d/1lUs7h2cj-LGv-0RZjPWrsCLMJmt2CTzh9kvyzV8nlV0/formResponse"

# 설문지 항목 ID
ENTRIES = {
    "date": "entry.1691386708",
    "user": "entry.1460592934",
    "cat": "entry.348705031",
    "text": "entry.1509172605"
}

# 3. 데이터 로드 함수
def load_data():
    try:
        url = f"{READ_URL}&cache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url)
        return df
    except:
        return pd.DataFrame()

# 4. 입력 UI
with st.form("memo_form"):
    user = st.selectbox("누구신가요?", ["아빠", "엄마", "지빈", "도빈"])
    category = st.selectbox("카테고리", ["📅 일정", "🛒 장보기", "💡 아이디어", "💬 기타"])
    content = st.text_input("내용을 입력하세요")
    submit = st.form_submit_button("저장하기")

    if submit and content:
        payload = {
            ENTRIES["date"]: datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            ENTRIES["user"]: user,
            ENTRIES["cat"]: category,
            ENTRIES["text"]: content
        }
        try:
            response = requests.post(FORM_URL, data=payload, timeout=10)
            if response.status_code == 200:
                st.success("✅ 저장 성공!")
                st.rerun()
            else:
                st.error(f"❌ 전송 실패 (상태 코드: {response.status_code})")
        except Exception as e:
            st.error(f"❌ 연결 오류: {e}")

# 5. 메모 목록 표시
st.write("---")
st.subheader("📌 최근 메모")
df = load_data()

if not df.empty:
    try:
        # 시트의 맨 오른쪽 열부터 순서대로 가져옴 (타임스탬프 열이 있어도 무관함)
        for i, row in df.iloc[::-1].head(10).iterrows():
            text = row.iloc[-1]
            cat = row.iloc[-2]
            who = row.iloc[-3]
            when = row.iloc[-4]
            if pd.notna(text):
                st.info(f"**[{cat}] {text}** \n({who} | {when})")
    except:
        st.write("표시할 메모가 아직 없거나 시트 형식이 다릅니다.")
else:
    st.write("표시할 메모가 없습니다. 첫 메모를 남겨보세요!")
