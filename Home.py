import streamlit as st
from utils import render_navbar, render_footer, load_articles

# 1. 页面基础配置
st.set_page_config(
    page_title="Dialogues with Jung",
    page_icon="🕯️",
    layout="wide"
)

# 2. 加载导航栏
render_navbar()

# ==============================================================================
# SECTION 1: HERO
# ==============================================================================
spacer1, main_col, spacer2 = st.columns([1, 2.2, 1])
with main_col:
    st.markdown("<br>", unsafe_allow_html=True)
    try:
        st.image("./assets/mandala.png", use_container_width=True) 
    except:
        pass
    
    st.markdown("""
    <div style="text-align: center; margin-top: 10px; margin-bottom: 60px;">
        <h1 style="font-size: 3.5rem; letter-spacing: 4px; font-weight: 400; color: #1A1A1A; margin-bottom: 0px; text-transform: uppercase; line-height: 1.2;">
            INDIVIDUATION
        </h1>
        <p style="font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; color: #8B5A2B; font-style: italic; margin-top: 5px;">
            The Journey to the Self
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# SECTION 2: ABOUT JUNG
# ==============================================================================
st.markdown("<hr style='border: none; border-top: 1px solid #D3C4B1; margin-bottom: 40px;'>", unsafe_allow_html=True)
col_text, col_img = st.columns([1.5, 1], gap="large")

with col_text:
    st.markdown("""
    <div style="padding-right: 20px;">
        <h3 style="margin-top:0; color: #8B5A2B; font-size: 2rem;">The Digital Sanctuary</h3>
        <p style="line-height: 1.8; font-size: 1.15rem; color: #4A4A4A; text-align: justify; margin-top: 20px;">
            This is not merely a website, but a vessel for introspection. 
            Here, amidst the noise of the modern world, we invite you to pause and listen to the whispers of the unconscious.
            <br><br>
            Drawing from C.G. Jung's profound insights in <i>The Red Book</i> and his Collected Works, 
            this space offers a bridge between your waking life and the symbolic depths within.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_img:
    try:
        st.image("./assets/jung_photo.jpg", caption="Carl Gustav Jung", use_container_width=True)
    except:
        st.info("请在 assets 文件夹放入 jung_photo.jpg")


# ==============================================================================
# SECTION 3: FROM THE ARCHIVES (修复报错版 + 新标题设计)
# ==============================================================================
st.markdown("<br><br>", unsafe_allow_html=True)

# --- 【修改点 1】: 新的标题设计 (仿 Figure 2 风格) ---
st.markdown("""
<div style="
    border-top: 2px solid #2C2C2C; 
    margin-top: 40px; 
    padding-top: 20px; 
    margin-bottom: 40px; 
    text-align: center;
">
    <h2 style="
        font-family: 'Cormorant Garamond', serif; 
        font-size: 2.5rem; 
        font-weight: 700; 
        color: #2C2C2C; 
        text-transform: uppercase; 
        letter-spacing: 2px;
        margin: 0;
    ">
        FROM THE ARCHIVES
    </h2>
    <p style="
        font-family: 'Lato', sans-serif; 
        font-size: 0.9rem; 
        color: #D0021B; 
        font-weight: 700; 
        letter-spacing: 1px; 
        margin-top: 8px; 
        text-transform: uppercase;
    ">
        Selected Readings & Essays
    </p>
</div>
""", unsafe_allow_html=True)

# --- 【修改点 2】: 稳定的跳转逻辑 ---
# 定义一个回调函数，专门处理点击事件
def read_article(article_data):
    st.session_state["current_article"] = article_data
    # 这里的 switch_page 必须配合 callback 使用才安全
    # 注意：在 callback 里不能直接 switch_page，我们要设置一个标记，在主循环里跳转
    st.session_state["do_navigate"] = True

# 检查是否需要跳转 (放在页面渲染的最外层)
if st.session_state.get("do_navigate", False):
    st.session_state["do_navigate"] = False # 重置标记
    st.switch_page("pages/阅读文章.py")


# 加载文章
all_articles = load_articles()

if not all_articles:
    st.info("暂无文章，请在 articles 文件夹中添加 .md 文件。")
else:
    # 逻辑：如果没有点击 View All，只显示前 6 篇
    if "show_all_archives" not in st.session_state:
        st.session_state.show_all_archives = False
    
    display_articles = all_articles if st.session_state.show_all_archives else all_articles[:6]
    
    # 渲染网格
    rows = [display_articles[i:i+3] for i in range(0, len(display_articles), 3)]
    
    for row in rows:
        cols = st.columns(3, gap="medium")
        for i, article in enumerate(row):
            # 为了防止 key 冲突，我们使用文章标题的哈希或者简单的循环索引作为 key
            unique_key = f"btn_{i}_{article['filename']}"
            
            with cols[i]:
                # 1. 图片区
                if article['image']:
                    try:
                        st.image(article['image'], use_container_width=True)
                    except:
                        st.markdown("<div style='height:180px; background:#F0EBE0;'></div>", unsafe_allow_html=True)
                
                # 2. 文字区
                st.markdown(f"""
                <div style="margin-top: 15px; margin-bottom: 10px;">
                    <div style="font-family:'Lato'; font-weight:bold; font-size:0.75rem; color:#D0021B; letter-spacing:1px; margin-bottom:5px;">
                        {article['category']}
                    </div>
                    <div style="font-family:'Cormorant Garamond'; font-weight:700; font-size:1.4rem; color:#2C2C2C; line-height:1.2; height: 3.4rem; overflow:hidden;">
                        {article['title']}
                    </div>
                    <div style="font-family:'Lato'; font-size:0.95rem; color:#666; line-height:1.5; height: 4.5rem; overflow:hidden; text-overflow: ellipsis;">
                        {article['excerpt']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 3. 按钮区 (修复版)
                # 使用 on_click 回调，这是最稳定的方式
                st.button(
                    "Read Article", 
                    key=unique_key, 
                    use_container_width=True,
                    on_click=read_article,
                    args=(article,)
                )
        
        st.markdown("<br>", unsafe_allow_html=True)

    # View All 按钮逻辑
    if len(all_articles) > 6 and not st.session_state.show_all_archives:
        st.markdown("<hr style='border:none; border-top:1px dashed #D3C4B1; margin: 20px 0;'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("View All Archives →", use_container_width=True):
                st.session_state.show_all_archives = True
                st.rerun() # 立即刷新页面显示所有文章

# 4. 全局页脚
render_footer()