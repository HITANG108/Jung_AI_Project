import streamlit as st
import os
import sys

# ==========================================
# 1. 基础配置与页面设置
# ==========================================
st.set_page_config(page_title="荣格解梦室", page_icon="🕯️")
st.title("🕯️ 卡尔·荣格的私人诊室")
st.markdown("### *“向外看的人在做梦，向内看的人是清醒的。”*")

# 侧边栏：放一些说明
with st.sidebar:
    st.header("关于")
    st.write("这是一个基于 RAG 技术的 AI 荣格。")
    st.write("它阅读了英文版《人及其象征》，并用中文为你解惑。")
    st.write("---")
    st.info("提示：你可以问关于梦的象征，或者书中的概念。")

# ==========================================
# 2. 核心逻辑（只加载一次，提高速度）
# ==========================================
@st.cache_resource
def load_jung_brain():
    """
    这个函数负责初始化 AI 和数据库。
    加了 @st.cache_resource 后，它只会运行一次，
    不会每次你发消息都重新加载模型。
    """
    # --- 这里填入你的配置 ---
    MY_API_KEY = "sk-6CqRNrrPMboZ8tqVbvAZ8wkCV0Wcf3jvpTBJ3hTRvneOnK80" 
    MY_BASE_URL = "https://api.moonshot.cn/v1" # Kimi 地址
    BOOK_PATH = "./data/Man and His Symbols.txt"
    # -----------------------

    os.environ["OPENAI_API_KEY"] = MY_API_KEY
    os.environ["OPENAI_API_BASE"] = MY_BASE_URL

    # 导入库
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_openai import ChatOpenAI
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain_core.prompts import ChatPromptTemplate

    # 1. 加载数据
    if not os.path.exists(BOOK_PATH):
        st.error(f"找不到文件：{BOOK_PATH}")
        return None

    loader = TextLoader(BOOK_PATH, encoding='utf-8') # 如果报错改为 autodetect_encoding=True
    docs = loader.load()
    
    # 2. 切片
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    # 3. 向量化 (本地模型)
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embedding_model)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # 4. 大模型 (Kimi)
    llm = ChatOpenAI(
        model="moonshot-v1-8k", 
        temperature=0.7,
        api_key=MY_API_KEY,
        base_url=MY_BASE_URL
    )

    # 5. 提示词
    system_prompt = (
        "你现在是心理学家卡尔·荣格。你面前坐着一位寻求指引的朋友。"
        "请根据【背景知识】（《人及其象征》）回答问题，必须用**中文**。"
        "风格要求：深邃、温暖、富有哲理，像一位智者。"
        "\n\n【背景知识】:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))
    return chain

# 加载荣格大脑（如果显示 Spinner 说明正在加载）
with st.spinner("荣格医师正在整理笔记...（初次运行可能需要几分钟）"):
    chain = load_jung_brain()

if chain is None:
    st.stop() # 如果加载失败就停止

# ==========================================
# 3. 聊天界面逻辑
# ==========================================

# 初始化聊天记录（Session State）
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好，我是荣格。请告诉我你的梦，或者你心中的困惑。"}
    ]

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 处理用户输入
if user_input := st.chat_input("在这里输入你的梦..."):
    # 1. 显示用户的话
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. 生成回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...") # 思考时的占位符
        
        # 调用 RAG 链
        response = chain.invoke({"input": user_input})
        answer = response['answer']
        
        # 显示结果
        message_placeholder.markdown(answer)
    
    # 3. 保存回复到历史
    st.session_state.messages.append({"role": "assistant", "content": answer})