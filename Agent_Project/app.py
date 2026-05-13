import streamlit as st
import os
import sys

# 这一行是“救命良药”，确保程序能找到你刚才创建的 utils 文件夹
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.rag_engine import get_rag_chain
from utils.document_processor import process_uploaded_files

# --- 1. 页面基本配置 ---
st.set_page_config(
    page_title="电商智能问答全栈系统",
    page_icon="🛍️",
    layout="wide"
)

# --- 2. 侧边栏：配置与知识库更新 ---
with st.sidebar:
    st.title("⚙️ 系统配置")
    # 比赛时评委需要输入他们自己的 API Key
    api_key = st.text_input("请输入 DashScope API Key", type="password")
    
    st.divider()
    
    st.header("📚 知识库离线更新")
    st.caption("基于 MD5 去重技术")
    # 上传实验用的电商数据文件
    uploaded_files = st.file_uploader("上传电商数据 (TXT格式)", accept_multiple_files=True)
    
    if st.button("一键更新知识库"):
        if not api_key:
            st.error("请先在上方输入 API Key！")
        elif not uploaded_files:
            st.warning("请先上传文件！")
        else:
            with st.spinner("正在进行向量化处理..."):
                try:
                    # 调用 utils 里的处理逻辑
                    count = process_uploaded_files(uploaded_files, api_key)
                    st.success(f"更新成功！共新增 {count} 条知识片段。")
                except Exception as e:
                    st.error(f"更新失败: {e}")

# --- 3. 主界面：智能问答 ---
st.title("💬 电商智能客服中心")
st.caption("技术栈：LangChain + Chroma + 通义千问 + Streamlit")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 渲染历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("您可以问我：这款衣服的尺码怎么选？"):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 生成 AI 回答
    with st.chat_message("assistant"):
        if not api_key:
            st.error("系统提示：请先在左侧侧边栏配置 API Key")
        else:
            with st.spinner("正在检索知识库..."):
                try:
                    # 获取 RAG 问答链
                    qa_chain = get_rag_chain(api_key)
                    # 运行问答链
                    result = qa_chain({"question": prompt, "chat_history": st.session_state.chat_history})
                    answer = result["answer"]
                    
                    st.markdown(answer)
                    
                    # 存入历史记录
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.session_state.chat_history.append((prompt, answer))
                except Exception as e:
                    st.error(f"对话出错: {e}")

# 侧边栏底部增加清空功能
if st.sidebar.button("清空对话历史"):
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.rerun()