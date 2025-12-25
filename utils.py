# --- 关键补丁：解决 Streamlit Cloud 的 SQLite 版本问题 ---
import sys
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# -------------------------------------------------------

import streamlit as st
import os
import textwrap # <--- 【新增】用于修复HTML缩进问题
from operator import itemgetter # 【关键新增】引入这把“镊子”

# ==========================================
# 1. API 配置 (云端安全版)
# ==========================================
# 尝试从 Streamlit 的保险箱读取 Key，如果读不到（比如在本地），再使用备用字符串
try:
    MY_API_KEY = st.secrets["MY_API_KEY"]
except:
    MY_API_KEY = ""

MY_BASE_URL = "https://api.moonshot.cn/v1"

# ==========================================
# 2. 全局美学 CSS (加粗导航 + 响应式优化)
# ==========================================
def set_style():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Lato:wght@400;700;900&display=swap');
        
        /* 1. 全局背景 */
        .stApp { background-color: #F9F7F2 !important; }
        
        /* 2. 页面容器 */
        .block-container {
            max-width: 85%; 
            padding-top: 1rem;
            padding-bottom: 2rem;
            margin: auto;
        }

        /* 3. 字体设置 */
        html, body, [class*="css"], p, div, li {
            font-family: 'Lato', sans-serif;
            color: #4A4A4A;
            line-height: 1.6;
        }
        h1, h2, h3, h4 {
            font-family: 'Cormorant Garamond', serif !important;
            font-weight: 700;
            color: #2C2C2C;
        }
        
        header, footer, #MainMenu {visibility: hidden;}
        
        /* ============================================================
           导航栏样式升级：更大、更粗
           ============================================================ */
        [data-testid="stPageLink-NavLink"] {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #5C5C5C !important;
            font-family: 'Lato', sans-serif !important;
            font-size: 20px !important;   /* 【修改】加大字号 */
            font-weight: 700 !important;  /* 【修改】加粗 */
            padding: 5px 10px !important;
            margin-top: 12px; 
            letter-spacing: 0.5px; /* 增加一点字间距，更显高级 */
        }

        [data-testid="stPageLink-NavLink"]:hover {
            color: #8B5A2B !important;
            text-decoration: none !important; /* 去掉下划线，改用颜色变化，更像大牌官网 */
            transform: translateY(-1px);      /* 微动效果 */
        }
        
        [data-testid="stPageLink-NavLink"][aria-current="page"] {
            color: #8B5A2B !important;
            border-bottom: 2px solid #8B5A2B !important; /* 选中时下方加一条横线 */
        }

        /* 按钮保持圆润 */
        .stButton > button, .stDownloadButton > button {
            background-color: transparent !important;
            border: 1px solid #D3C4B1 !important;
            color: #5C5C5C !important;
            font-family: 'Cormorant Garamond', serif;
            font-size: 16px; 
            border-radius: 25px !important;
            padding: 5px 15px !important;
            transition: all 0.3s ease;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            border-color: #8B5A2B !important;
            color: #8B5A2B !important;
            background-color: #FFFFFF !important;
        }
        
        a { text-decoration: none !important; color: #5C5C5C !important; }
        a:hover { color: #8B5A2B !important; }
        
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. 顶部导航栏 (升级版：大标题+格言)
# ==========================================
def render_navbar():
    set_style()
    
    with st.container():
        # 布局：左侧 Logo 区加大到 5，右侧菜单区均分
        cols = st.columns([5, 1, 1, 1, 1, 1])
        
        # --- 左侧：网站 Logo + 格言 ---
        with cols[0]:
            st.markdown("""
            <div style="padding-left: 10px;">
                <a href="Home" target="_self" style="text-decoration:none;">
                    <h3 style="margin:0; padding:0; font-size: 34px; font-family: 'Cormorant Garamond', serif; color: #2C2C2C; letter-spacing: 2px;">
                        DIALOGUES WITH JUNG
                    </h3>
                </a>
                <p style="margin: 5px 0 0 0; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 16px; color: #888;">
                    “Who looks outside, dreams; who looks inside, awakes.”
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        # --- 右侧：导航菜单 (在这里修改文字) ---
        with cols[1]: st.page_link("Home.py", label="Home", icon=None)
        with cols[2]: st.page_link("pages/资料库.py", label="Library", icon=None) 
        with cols[3]: st.page_link("pages/名词词典.py", label="Glossary", icon=None) 
        with cols[4]: st.page_link("pages/与荣格对话.py", label="Dialogue", icon=None)
        with cols[5]: st.page_link("pages/心理测试.py", label="Self", icon=None)
        
    # 导航栏下方加一条极细的分割线，增加精致感
    st.markdown("<hr style='margin-top: 20px; margin-bottom: 40px; border: none; border-top: 1px solid #E6E6E6;'>", unsafe_allow_html=True)

# ==========================================
# 4. 荣格大脑 (安全加载版)
# ==========================================
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@st.cache_resource
def get_jung_brain():
    # 【关键修改】所有的重型库都在函数内部导入
    # 这样即使它们加载失败，也不会导致主页打不开
    try:
        from langchain_community.document_loaders import TextLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.runnables import RunnablePassthrough
        from langchain_core.output_parsers import StrOutputParser
    except ImportError as e:
        st.error(f"❌ 依赖库加载失败，请检查 requirements.txt: {e}")
        return None

    book_path = "./data/Men and His Symbols.txt"
    if not os.path.exists(book_path):
        st.error(f"❌ 找不到书籍文件：{book_path}")
        return None

    try:
        loader = TextLoader(book_path, autodetect_encoding=True)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)
        
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(documents=splits, embedding=embedding_model)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        
        llm = ChatOpenAI(
            model="moonshot-v1-8k",
            temperature=0.7,
            api_key=MY_API_KEY,
            base_url=MY_BASE_URL
        )

        system_prompt = (
            "你现在是心理学家卡尔·荣格。请根据【背景知识】回答问题，必须用**中文**。"
            "你的语气深邃、包容、富有哲理。"
            "\n\n【背景知识】:\n{context}"
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        rag_chain = (
            {
                "context": itemgetter("input") | retriever | format_docs,
                "input": itemgetter("input")
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        return rag_chain

    except Exception as e:
        st.error(f"❌ 系统初始化失败 (可能是数据库兼容性问题): {e}")
        return None

# ==========================================
# 5. 全局页脚 (修复版：HTML渲染 + 全站通用)
# ==========================================

def render_footer():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<hr style='border: none; border-top: 4px solid #2C2C2C; margin-bottom: 0;'>", unsafe_allow_html=True)
    
    # 【关键修改】使用 textwrap.dedent 清除缩进，防止被识别为代码块
    footer_html = textwrap.dedent("""
    <style>
        .footer-container {
            background-color: #F0EBE0;
            padding: 50px 20px;
            font-family: 'Lato', sans-serif;
            color: #2C2C2C;
        }
        .footer-col {
            flex: 1;
            min-width: 200px;
            padding: 10px;
        }
        .footer-header {
            font-family: 'Cormorant Garamond', serif;
            font-weight: 700;
            font-size: 1.2rem;
            color: #8B5A2B;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #D3C4B1;
            padding-bottom: 5px;
            display: inline-block;
        }
        .footer-link {
            display: block;
            color: #4A4A4A;
            text-decoration: none;
            margin-bottom: 8px;
            font-size: 0.95rem;
            transition: color 0.2s;
        }
        .footer-link:hover {
            color: #8B5A2B;
            text-decoration: underline;
        }
        .footer-copy {
            font-size: 0.85rem;
            color: #888;
            line-height: 1.6;
            margin-top: 20px;
        }
    </style>

    <div class="footer-container">
        <div style="display: flex; flex-wrap: wrap; max-width: 1200px; margin: 0 auto; gap: 20px;">
            <div class="footer-col">
                <div class="footer-header">The Library</div>
                <a href="资料库" target="_self" class="footer-link">Princeton C.W.</a>
                <a href="资料库" target="_self" class="footer-link">Chinese Editions</a>
                <a href="资料库" target="_self" class="footer-link">Post-Jungian Scholars</a>
            </div>
            <div class="footer-col">
                <div class="footer-header">Tools & Guide</div>
                <a href="名词词典" target="_self" class="footer-link">Symbol Glossary</a>
                <a href="心理测试" target="_self" class="footer-link">Archetype Test</a>
                <a href="名词词典" target="_self" class="footer-link">Key Concepts</a>
            </div>
            <div class="footer-col">
                <div class="footer-header">Interaction</div>
                <a href="与荣格对话" target="_self" class="footer-link">Talk with Jung AI</a>
                <a href="与荣格对话" target="_self" class="footer-link">Dream Analysis</a>
            </div>
            <div class="footer-col">
                <div class="footer-header">About</div>
                <div class="footer-copy">
                    <b>Dialogues with Jung</b><br>
                    A digital sanctuary for the soul.<br>
                    Created by Ruixuan Tang.<br>
                    &copy; 2025 All Rights Reserved.
                </div>
            </div>
        </div>
    </div>
    """)
    
    st.markdown(footer_html, unsafe_allow_html=True)


# ==========================================
# 6. 文章加载器 (新增)
# ==========================================
def load_articles():
    """读取 articles 文件夹下的所有 .md 文件"""
    articles = []
    article_dir = "./articles"
    
    if not os.path.exists(article_dir):
        os.makedirs(article_dir) # 如果没文件夹自动创建一个
        return []

    # 遍历文件夹
    for filename in os.listdir(article_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(article_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            # 简单的解析器：分离头部元数据(---之间)和正文
            try:
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    meta_raw = parts[1].strip()
                    body = parts[2].strip()
                    
                    # 解析元数据
                    meta = {}
                    for line in meta_raw.split("\n"):
                        if ":" in line:
                            key, val = line.split(":", 1)
                            meta[key.strip()] = val.strip()
                    
                    # 打包数据
                    articles.append({
                        "filename": filename,
                        "title": meta.get("title", "Untitled"),
                        "category": meta.get("category", "General"),
                        "excerpt": meta.get("excerpt", ""),
                        "image": meta.get("image", ""),
                        "date": meta.get("date", ""),
                        "content": body
                    })
            except:
                continue # 如果格式不对就跳过
    
    return articles