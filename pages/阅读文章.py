import streamlit as st
from utils import render_navbar, render_footer

# 1. 配置与导航
st.set_page_config(page_title="Reading Room", page_icon="📖", layout="wide")
render_navbar()

# 2. 获取要阅读的文章
# 我们通过 st.session_state 接收主页传过来的文章数据
if "current_article" not in st.session_state:
    st.warning("请先在主页选择一篇文章。")
    st.page_link("Home.py", label="返回主页")
else:
    article = st.session_state["current_article"]

    # --- 3. 渲染文章页面 (纽约客风格) ---
    
    # 顶部留白
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 标题区
    st.markdown(f"""
    <div style="text-align: center; max-width: 800px; margin: 0 auto;">
        <div style="font-family:'Lato'; font-weight:900; color:#D0021B; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;">
            {article['category']}
        </div>
        <h1 style="font-family:'Cormorant Garamond'; font-size: 3rem; margin-bottom: 20px; line-height: 1.2;">
            {article['title']}
        </h1>
        <div style="font-family:'Cormorant Garamond'; font-style:italic; color:#666; font-size:1.2rem; margin-bottom: 30px;">
            {article['excerpt']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 封面图 (如果有)
    if article['image']:
        try:
            # 居中显示图片
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.image(article['image'], use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)
        except:
            pass

    # 正文区 (限制宽度，提升阅读体验)
    c_space1, c_text, c_space2 = st.columns([1, 2, 1])
    with c_text:
        # 使用 markdown 渲染正文
        st.markdown(article['content'])
        
        # 返回按钮
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        if st.button("← Back to Archives"):
            st.switch_page("Home.py")

# 4. 页脚
render_footer()