import streamlit as st
from utils import render_navbar, render_footer

# 1. 先渲染导航栏 (这行代码必须放在最前面)
render_navbar()

st.title("🔍 荣格心理学术语词典")

# 1. 你的数据源（以后可以直接在这里改，或者从 Excel 读取）
terms = {
    "阴影 (Shadow)": "人格中未被意识到的、被压抑的、‘负面’的特质。它是通往潜意识的大门。",
    "阿尼玛 (Anima)": "男性无意识中的女性意象。它是情感、直觉和生命力的源泉。",
    "阿尼姆斯 (Animus)": "女性无意识中的男性意象。它代表理智、精神和观点。",
    "自性 (Self)": "心灵的完整性，意识与无意识的统一中心。它是心理发展的终极目标。",
    "共时性 (Synchronicity)": "有意义的巧合。内心状态与外部事件之间非因果的联系。",
    "面具 (Persona)": "个体适应社会而形成的人格面具，我们向外界展示的样子。",
}

# 2. 搜索框
search_query = st.text_input("输入关键词搜索（例如：阴影）...")

# 3. 显示逻辑
found = False
for key, value in terms.items():
    # 如果搜索框为空，或者关键词在标题里，就显示
    if search_query == "" or search_query in key:
        with st.expander(f"📌 {key}", expanded=(search_query != "")):
            st.write(value)
        found = True

if not found:
    st.warning("词典中暂未收录此词条。")

render_footer()