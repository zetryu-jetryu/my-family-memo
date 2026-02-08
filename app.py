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

# 3. 데이터 로드 (열 이름 대신 순서로 읽기)
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
        # 전송할 데이터 준비
        payload = {
            ENTRIES["date"]: datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            ENTRIES["user"]: user,
            ENTRIES["cat"]: category,
            ENTRIES["text"]: content
        }
        
        try:
            # 주소 끝이 /formResponse인지 다시 확인하세요!
            response = requests.post(FORM_URL, data=payload, timeout=10)
            
            if response.status_code == 200:
                st.success("✅ 저장 성공!")
                st.rerun()
            else:
                st.error(f"❌ 전송 실패 (상태 코드: {response.status_code})")
                st.write("설문지 주소나 질문 번호(entry ID)를 확인해 주세요.")
                
        except Exception as e:
            # 상세 에러 메시지 출력
            st.error(f"❌ 실제 연결 에러 내용: {e}")
            st.write("인터넷 연결이나 라이브러리 설치 상태를 확인하세요.")

# 5. 메모 목록 표시 (열 이름 에러 방지)
st.write("---")
st.subheader("📌 최근 메모")
df = load_data()

if not df.empty:
    try:
        # 열 이름을 쓰지 않고 '위치'로 데이터를 가져옵니다.
        # 보통 설문지 연결 시: [0]타임스탬프, [1]날짜, [2]작성자, [3]카테고리, [4]내용
        # 만약 타임스탬프가 없다면 순서가 당겨질 수 있으므로 안전하게 처리합니다.
        for i, row in df.iloc[::-1].head(10).iterrows():
            # 리스트의 뒤에서부터 가져오면 열이 추가되어도 안전합니다.
            text = row.iloc[-1] # 마지막 열 (내용)
            cat = row.iloc[-2]  # 마지막에서 두 번째 (카테고리)
            who = row.iloc[-3]  # 마지막에서 세 번째 (작성자)
            when = row.iloc[-4] # 마지막에서 네 번째 (날짜)
            
            if pd.notna(text):
                st.info(f"**[{cat}] {text}** \n({who} | {when})")
    except Exception as e:
        st.error(f"목록 표시 오류: 시트의 열 개수가 부족합니다.")
else:
    st.write("표시할 메모가 없습니다. 첫 메모를 남겨보세요!")

