import streamlit as st
import google.generativeai as genai

# ✅ Streamlit secrets에서 API 키 가져오기
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# ✅ Gemini 설정
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Streamlit UI
st.set_page_config(page_title="Git diff 기반 커밋 메시지 생성기", layout="centered")
st.title("💡 Git diff 기반 자동 커밋 메시지 생성기 (Gemini API)")

# ✅ 파일 업로드
uploaded_file = st.file_uploader("🔄 `.diff` 파일을 업로드하세요", type=["diff", "txt"])

if uploaded_file is not None:
    diff_content = uploaded_file.read().decode("utf-8")

    st.subheader("📋 업로드된 diff 내용")
    st.code(diff_content, language="diff")

    # ✅ 프롬프트 생성
    prompt = f"""
아래는 Git 커밋 메시지 규칙입니다:

// Header, Body, Footer는 빈 행으로 구분한다.
타입(스코프): 주제(제목) // Header

본문 // Body

바닥글 // Footer

타입(feat, fix, docs, style, refactor, test, chore, revert)와 스코프(기능 단위)를 명확히 파악해서 아래 변경사항에 맞는 커밋 메시지를 생성해줘.

변경사항:
{diff_content}
"""

    if st.button("💬 커밋 메시지 생성하기"):
        with st.spinner("Gemini가 커밋 메시지를 생성 중입니다..."):
            try:
                # ✅ chat 방식으로 생성
                chat = genai.ChatModel(model_name="models/chat-bison-001").start_chat()
                response = chat.send_message(prompt)

                st.success("✅ 커밋 메시지 생성 완료!")
                st.subheader("📜 자동 생성된 커밋 메시지")
                st.code(response.text.strip(), language="markdown")

            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")
else:
    st.info("🔼 `.diff` 파일을 업로드 해주세요.")

st.markdown("---")
st.caption("Powered by Streamlit + Gemini API")
