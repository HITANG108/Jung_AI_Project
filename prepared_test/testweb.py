import streamlit as st
import time

# ==========================================
# 1. 页面配置与基础设置
# ==========================================
st.set_page_config(
    page_title="C.G. Jung Archives",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. 自定义 CSS (打造深邃、神秘风格)
# ==========================================
# 这里的 CSS 负责将默认的 Streamlit 界面改造为“荣格风格”
# 颜色：#0E1117 (深黑背景), #D4AF37 (炼金术金), #C0C0C0 (银灰文字)
custom_css = """
<style>
    /* 全局背景色 */
    .stApp {
        background-color: #0E1117;
        color: #C0C0C0;
        font-family: 'Georgia', serif; /* 使用衬线字体增加古典感 */
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-family: 'Georgia', serif;
        font-weight: 300;
        letter-spacing: 2px;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #333;
    }
    
    /* 按钮样式 - 模拟古书按钮 */
    .stButton>button {
        color: #D4AF37;
        border: 1px solid #D4AF37;
        background-color: transparent;
        border-radius: 0px;
        transition: all 0.3s;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #D4AF37;
        color: #0E1117;
        border-color: #D4AF37;
    }
    
    /* 搜索框和输入框样式 */
    .stTextInput>div>div>input {
        background-color: #1E232B;
        color: #E0E0E0;
        border: 1px solid #444;
    }
    
    /* 卡片/容器背景 */
    .feature-card {
        background-color: #161B22;
        padding: 20px;
        border: 1px solid #333;
        border-radius: 5px;
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .feature-card:hover {
        border-color: #D4AF37;
        transform: translateY(-2px);
    }
    
    /* 隐藏默认的 Streamlit 菜单 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 3. 状态管理 (Session State)
# ==========================================
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [
        {"role": "assistant", "content": "你好，我是卡尔·荣格的数字映像。告诉我你的梦，或者你心中的困惑。"}
    ]

# 导航函数
def navigate_to(page_name):
    st.session_state['current_page'] = page_name

# ==========================================
# 4. 侧边栏设计 (曼陀罗与导航)
# ==========================================
with st.sidebar:
    # 曼陀罗图案 (使用占位符，你可以替换为本地图片的路径)
    # st.image("path/to/mandala.png") 
    # 这里用SVG绘制一个简单的曼陀罗示意图
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <svg viewBox="0 0 100 100" width="150" height="150">
                <circle cx="50" cy="50" r="48" stroke="#D4AF37" stroke-width="1" fill="none"/>
                <circle cx="50" cy="50" r="40" stroke="#D4AF37" stroke-width="0.5" fill="none"/>
                <path d="M50 2 L50 98 M2 50 L98 50" stroke="#333" stroke-width="0.5"/>
                <rect x="28" y="28" width="44" height="44" stroke="#D4AF37" stroke-width="0.5" fill="none" transform="rotate(45 50 50)"/>
            </svg>
            <p style="color: #666; font-size: 0.8em; margin-top: 10px;">THE RED BOOK</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # 侧边栏导航
    if st.button("🏛️ 回到主页 / Home"):
        navigate_to("Home")
    
    st.markdown("### 探索 / Explore")
    if st.button("📚 相关资料 / Archives"):
        navigate_to("Materials")
    if st.button("🗝️ 名词解释 / Lexicon"):
        navigate_to("Terms")
    if st.button("🕯️ 与荣格对话 / Dialogue"):
        navigate_to("Chat")
    if st.button("👁️ 自我测试 / Psyche Test"):
        navigate_to("Tests")

# ==========================================
# 5. 核心页面逻辑
# ==========================================

# --- 头部标题 ---
st.markdown(f"<h1 style='text-align: center; margin-bottom: 40px;'>CARL GUSTAV JUNG</h1>", unsafe_allow_html=True)

# --- 页面 A: 主页 ---
if st.session_state['current_page'] == 'Home':
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 荣格照片占位符
        st.markdown("""
        <div style="border: 1px solid #D4AF37; padding: 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Carl_Jung.jpg/467px-Carl_Jung.jpg" width="100%" style="filter: sepia(40%) contrast(1.1);">
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("### 欢迎来到潜意识的深处")
        st.write("""
        这是一个致力于探索卡尔·古斯塔夫·荣格（Carl Gustav Jung）分析心理学的数字空间。
        在这里，你可以通过 AI 技术与荣格的思想进行跨越时空的对话，查阅珍贵的心理学文献，或通过测试探索你的内心原型。
        
        > "向外看的人在做梦，向内看的人醒着。"
        
        本网站不仅是一个资料库，更是一个协助你进行「个体化」（Individuation）过程的工具。
        """)
        
        st.markdown("#### 功能概览")
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.info("📚 **文献资料**\n\n中英对照的核心著作整理。")
        with c2: st.info("🗝️ **词汇索引**\n\n原型、阴影、阿尼玛等术语解释。")
        with c3: st.info("🕯️ **AI 对话**\n\n基于 RAG 技术的深度心理咨询。")
        with c4: st.info("👁️ **心理测试**\n\n简单的原型与人格测试。")

# --- 页面 B: 资料库 ---
elif st.session_state['current_page'] == 'Materials':
    st.markdown("## 📚 相关资料 / Archives")
    st.write("精选的荣格著作及其中文对应版本。")
    
    materials = [
        {"title": "The Red Book (Liber Novus)", "cn": "《红书》", "desc": "荣格与潜意识对抗的记录，包含了大量曼陀罗手绘。"},
        {"title": "Memories, Dreams, Reflections", "cn": "《回忆、梦、思考》", "desc": "荣格的自传，理解他思想起源的关键。"},
        {"title": "Man and His Symbols", "cn": "《人及其象征》", "desc": "面向大众读者的最后一部著作，解释了梦的象征意义。"},
        {"title": "Psychology and Alchemy", "cn": "《心理学与炼金术》", "desc": "探讨炼金术象征与个体化过程的关系。"}
    ]
    
    for book in materials:
        with st.container():
            st.markdown(f"""
            <div class="feature-card">
                <h3 style="margin:0;">{book['cn']}</h3>
                <p style="color: #888; font-style: italic;">{book['title']}</p>
                <p>{book['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# --- 页面 C: 名词解释 ---
elif st.session_state['current_page'] == 'Terms':
    st.markdown("## 🗝️ 专有名词 / Lexicon")
    
    # 模拟数据
    terms_db = {
        "Archetype (原型)": "集体潜意识中存在的原始心理结构，如英雄、母亲、智慧老人。",
        "Shadow (阴影)": "人格中被压抑、未被认可的阴暗面，通常包含原始的本能和负面情绪。",
        "Anima/Animus (阿尼玛/阿尼姆斯)": "男性心理中的女性意象（Anima）和女性心理中的男性意象（Animus）。",
        "Self (自性)": "心灵的完整性与调节中心，是个体化的终极目标。",
        "Individuation (个体化)": "从集体心理中分化出来，成为一个独立、完整的人格的过程。",
        "Synchronicity (共时性)": "由因果律之外的意义将两个事件联系起来的现象。"
    }
    
    search_query = st.text_input("🔍 搜索关键词 (例如：阴影, 原型)...", "")
    
    found = False
    for term, definition in terms_db.items():
        if search_query.lower() in term.lower():
            found = True
            st.markdown(f"""
            <div class="feature-card">
                <h4 style="color: #D4AF37;">{term}</h4>
                <p>{definition}</p>
            </div>
            """, unsafe_allow_html=True)
            
    if not found:
        st.warning("未找到相关词条。")

# --- 页面 D: AI 对话 (你的核心需求) ---
elif st.session_state['current_page'] == 'Chat':
    st.markdown("## 🕯️ 与荣格对话 / Dialogue")
    st.caption("基于 RAG 技术增强的 AI 模拟（当前为演示模式，请在代码中接入你的 Python 逻辑）")

    # ----------------------------------------------------------------
    #  关键部分：这里是你的 RAG 接口
    # ----------------------------------------------------------------
    def get_my_rag_response(user_input):
        """
        [未来开发接口]
        在这里调用你自己的 Python RAG 代码。
        例如：
        context = retrieval_system.search(user_input)
        response = llm.generate(context, user_input)
        return response
        """
        # 模拟延时和思考
        time.sleep(1) 
        
        # 这是一个模拟回复，请替换为你的真实函数调用
        return f"（RAG 模拟回复）这是一个很有趣的问题... 关于 '{user_input}'，在我的《红书》中，我也曾遇到过类似的象征。这或许是你潜意识中阴影的投射..."

    # 显示历史消息
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 处理用户输入
    if prompt := st.chat_input("向荣格博士提问..."):
        # 1. 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # 2. 获取 AI 回复
        with st.chat_message("assistant"):
            with st.spinner("博士正在思考..."):
                response_text = get_my_rag_response(prompt)
                st.markdown(response_text)
        
        # 3. 保存 AI 回复
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})

# --- 页面 E: 简单测试 ---
elif st.session_state['current_page'] == 'Tests':
    st.markdown("## 👁️ 自我测试 / Psyche Test")
    st.write("一个简短的原型倾向测试。")
    
    with st.form("test_form"):
        q1 = st.radio("1. 当你面对巨大的未知挑战时，你的第一反应是？", 
                      ("制定计划，掌控局势", "寻找其中的深层意义", "寻求他人的帮助", "独自面对，将其视为冒险"))
        
        q2 = st.radio("2. 你最害怕失去什么？", 
                      ("自由", "安全感", "与他人的联系", "自我认知"))
        
        submitted = st.form_submit_button("查看分析")
        
        if submitted:
            st.success("测试完成。")
            st.markdown("""
            <div class="feature-card">
                <h4>分析结果</h4>
                <p>根据你的选择，你当前的能量似乎更倾向于 <b>探险家 (The Explorer)</b> 与 <b>智者 (The Sage)</b> 的混合原型。</p>
                <p>你渴望理解世界的本质，同时也需要保持个体的独立性。</p>
            </div>
            """, unsafe_allow_html=True)

# 底部版权
st.markdown("---")
st.markdown("<p style='text-align: center; color: #444; font-size: 0.8em;'>© 2024 Jungian Archives Project. Designed for Depth Psychology.</p>", unsafe_allow_html=True)