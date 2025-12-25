import streamlit as st
from utils import get_jung_brain, set_style # 引入样式函数
from utils import render_navbar, get_jung_brain, render_footer # 记得导入 render_navbar

# 1. 先渲染导航栏 (这行代码必须放在最前面)
render_navbar()
# 1. 设置样式
set_style()

# 2. 页面标题
st.markdown("## 🕯️ 荣格医师的诊室")
st.caption("在这里，你可以放下防御，安全地倾诉你的梦境。")

# 3. 加载大脑
chain = get_jung_brain()

# 4. 聊天容器
# 我们用一个容器把聊天记录包起来，增加一点边距
chat_container = st.container()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是荣格。请告诉我你的梦，或者你心中的困惑。"}]

with chat_container:
    for msg in st.session_state.messages:
        # Streamlit 现在的 chat_message 样式比较固定
        # 但因为我们全局设置了 config.toml 为 light，现在它会是白底黑字，看着很舒服
        with st.chat_message(msg["role"], avatar="🕯️" if msg["role"] == "assistant" else "👤"):
            st.write(msg["content"])

# 5. 输入框
if user_input := st.chat_input("在此输入你的梦境..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)

        with st.chat_message("assistant", avatar="🕯️"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            # 直接调用 invoke，得到的就是回答字符串
        response = chain.invoke({"input": user_input}) 
        
        # 不需要再用 ['answer'] 去取了，response 本身就是答案
        message_placeholder.markdown(response)
    
    # 保存历史
    st.session_state.messages.append({"role": "assistant", "content": response})


render_footer()