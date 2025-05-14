import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Custom commit message format description
FORMAT_DESCRIPTION = """
아래 형식에 맞게 커밋 메시지를 분석하거나 재작성해줘:

// Header, Body, Footer는 빈 행으로 구분한다.
타입(스코프): 주제(제목) // Header

본문 // Body

바닥글 // Footer

타입 목록: feat, fix, docs, style, refactor, test, chore, revert
"""

# Streamlit UI
st.set_page_config(page_title="Git 커밋 메시지 포매터", layout="centered")
st.title("🧠 Git 커밋 메시지 요약 · 포맷터 (Gemini API 기반)")

mode = st.radio("작업 선택", ["분석", "포맷 재작성"], horizontal=True)

input_message = st.text_area("💬 커밋 메시지를 입력하세요", height=200, placeholder="예: 로그인 기능 추가 및 오류 수정...")

if st.button("Gemini에게 맡기기 ✨") and input_message.strip():
    with st.spinner("Gemini가 처리 중입니다..."):

        prompt = ""
        if mode == "분석":
            prompt = f"{FORMAT_DESCRIPTION}\n\n아래 커밋 메시지를 분석해줘:\n\n{input_message}"
        else:
            prompt = f"{FORMAT_DESCRIPTION}\n\n아래 커밋 메시지를 위 형식에 맞춰 다시 작성해줘:\n\n{input_message}"

        try:
            response = model.generate_content(prompt)
            st.subheader("📋 결과")
            st.code(response.text.strip(), language="markdown")
        except Exception as e:
            st.error(f"오류 발생: {e}")

st.markdown("---")
st.caption("💡 Powered by Streamlit + Gemini API")
