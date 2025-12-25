import streamlit as st
import os
from utils import render_navbar, render_footer

# 1. 加载导航栏
render_navbar()

# ==============================================================================
# 0. 辅助功能：智能下载按钮生成器
# ==============================================================================
def render_download_btn(file_name, label="下载 / Download", unique_key=None):
    """
    检查 data 文件夹里有没有这个文件。
    如果有 -> 显示复古风下载按钮
    如果没有 -> 显示灰色不可点按钮
    """
    base_path = "./data/"
    full_path = os.path.join(base_path, file_name) if file_name else None
    
    if full_path and os.path.exists(full_path):
        with open(full_path, "rb") as f:
            st.download_button(
                label=f"📥 {label}",
                data=f,
                file_name=file_name,
                mime="application/pdf", 
                key=unique_key,
                use_container_width=True
            )
    else:
        st.button(f"🔒 暂无", disabled=True, key=unique_key, use_container_width=True)

# 标题区
st.markdown("""
<div style="text-align: center; margin-bottom: 40px;">
    <h2 style="font-size: 2.5rem; color: #8B5A2B; margin-bottom: 10px;">The Library</h2>
    <p style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 1.1rem; color: #666;">
        “I am not what happened to me, I am what I choose to become.”
    </p>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# Part I: C.W. 普林斯顿全集
# ==============================================================================
# --- 顶部大下载按钮区 ---
st.markdown("""
<div style="border-left: 3px solid #8B5A2B; padding-left: 20px; margin-bottom: 20px;">
    <h3 style="margin: 0;">Part I: The Collected Works (C.W.)</h3>
    <p style="font-size: 0.95rem; color: #888; margin-top: 5px;">Princeton University Press Edition</p>
</div>
""", unsafe_allow_html=True)

CW_FULL_ZIP = "The Collected Works of C. G. Jung.epub" 

col_info, col_btn = st.columns([3, 1])
with col_info:
    st.markdown("<div style='color: #666; padding-top: 5px;'>💡 这里存放了普林斯顿版 C.W. 的核心资料整理，右侧按钮可一键下载全集。</div>", unsafe_allow_html=True)
with col_btn:
    render_download_btn(CW_FULL_ZIP, label="Download All (ZIP)", unique_key="cw_all")

st.markdown("<br>", unsafe_allow_html=True)

# --- C.W. 数据录入区 ---
cw_data = [
    {"vol": "Vol. 1", "title": "Psychiatric Studies (1902-1905)", "note": "从荣格博士论文《论神智现象的心理学和病理学》开始，暂未找到中文版", "file": ""},
    {"vol": "Vol. 2", "title": "Experimental Researches", "note": "主要是词语联想实验相关，暂未找到中文版", "file": ""},
    {"vol": "Vol. 3", "title": "Psychogenesis of Mental Disease", "note": "精神病学研究，暂未找到中文版", "file": ""},
    {"vol": "Vol. 4", "title": "Freud and Psychoanalysis", "note": "《弗洛伊德与精神分析》—荣格文集九册（国际文化出版公司）", "file": ""},
    {"vol": "Vol. 5", "title": "Symbols of Transformation", "note": "《转化的象征》（荣格与弗洛伊德决裂之作）—荣格文集九册（国际文化出版公司）", "file": ""},
    {"vol": "Vol. 6", "title": "Psychological Types", "note": "《心理类型》，版本较多，推荐译林吴康版以及商汤（繁体）版", "file": ""},
    {"vol": "Vol. 7", "title": "Two Essays on Analytical Psychology", "note": "《分析心理学二论》（包含《自我与无意识》）", "file": ""},
    {"vol": "Vol. 7-1", "title": "On the Psychology of the Unconscious", "note": "暂未找到中文版", "file": ""},
    {"vol": "Vol. 7-2", "title": "The Relations between the Ego and the Unconscious", "note": "《自我与无意识》--庄仲黎译", "file": ""},
    {"vol": "Vol. 8", "title": "The Structure and Dynamics of the Psyche", "note": "《心理结构与心理动力学》—荣格文集九册（国际文化出版公司）", "file": ""},
    {"vol": "Vol. 9.1", "title": "Archetypes and the Collective Unconscious", "note": "《原型与集体无意识》 (核心必读)—荣格文集九册（国际文化出版公司）", "file": ""},
    {"vol": "Vol. 9.2", "title": "AION: Researches into the Phenomenology of the Self", "note": "《伊雍：自性现象学研究》--译林出版社（白）", "file": ""},
    {"vol": "Vol. 10", "title": "Civilization in Transition", "note": "《文明的变迁》—荣格文集九册（国际文化出版公司）", "file": ""},
    {"vol": "Vol. 11", "title": "Psychology and Religion: West and East", "note": "《精神分析与灵魂治疗》—（红）译林出版社（其中东方的部分有，易经、西藏度亡经评述）", "file": ""},
    {"vol": "Vol. 12", "title": "Psychology and Alchemy", "note": "心理学与炼金术--译林出版社（白1+4）", "file": ""},
    
    # --- Vol 13 ---
    {
        "vol": "Vol. 13", 
        "title": "Alchemical Studies", 
        "note": "炼金术研究",
        "subs": [
            "1. Commentary on 'The Secret of the Golden Flower' (1929) - 《金花的秘密》评述",
            "2. The Visions of Zosimos (1938, 1954) - 佐西莫斯的幻象,《精灵墨丘利》 —（白）译林出版社",
            "3. Paracelsus as a Spiritual Phenomenon (1942) - 作为精神现象的帕拉塞尔苏斯,《精灵墨丘利》 —（白）译林出版社",
            "4. The Spirit Mercurius - 精灵墨丘利,《精灵墨丘利》 —（白）译林出版社",
            "5. The Philosophical Tree - 《哲学树》 —（白）译林出版社"
        ]
    },
    
    {"vol": "Vol. 14", "title": "Mysterium Coniunctionis", "note": "神秘融合 (荣格晚年大成之作)，暂未找到中文版", "file": ""},
    {"vol": "Vol. 15", "title": "The Spirit in Man, Art, and Literature", "note": "《人、艺术与文学中的精神》—荣格文集九册（国际文化出版公司）", "file": ""},
    {"vol": "Vol. 16", "title": "The Practice of Psychotherapy", "note": "《移情心理学》/《心理治疗实践》", "file": ""},
    {"vol": "Vol. 17", "title": "The Development of Personality", "note": "《人格的发展》—荣格文集九册（国际文化出版公司）", "file": ""},
    {"vol": "Vol. 18", "title": "The Symbolic Life", "note": "《象征生活》（杂文补遗）--荣格文集九册（国际文化出版公司）【仅对应1-4】", "file": ""},
]

# --- C.W. 表格渲染 ---
# 表头
st.markdown("""
<div style="display: grid; grid-template-columns: 1fr 3fr 3fr 1.5fr; border-bottom: 2px solid #D3C4B1; padding-bottom: 10px; margin-bottom: 15px; font-family: 'Cormorant Garamond', serif; font-weight: bold; color: #8B5A2B; font-size: 1.1rem;">
    <div>Volume</div>
    <div>Title</div>
    <div>Note / Chinese Version</div>
    <div style="text-align: right;">Download</div>
</div>
""", unsafe_allow_html=True)

for i, item in enumerate(cw_data):
    c1, c2, c3, c4 = st.columns([1, 3, 3, 1.5])
    # 【修改】：在这里加入了 font-size: 1.15rem 来单独放大表格内的文字
    with c1: st.markdown(f"**{item['vol']}**")
    with c2: st.markdown(f"<span style='font-family: Cormorant Garamond; font-size: 1.15rem;'>{item['title']}</span>", unsafe_allow_html=True)
    with c3: st.markdown(f"<span style='font-size: 1.05rem;'>{item['note']}</span>", unsafe_allow_html=True)
    with c4: render_download_btn(item.get('file'), label="PDF", unique_key=f"cw_{i}")

    if "subs" in item:
        for sub in item["subs"]:
            with st.container():
                sc1, sc2 = st.columns([1, 6])
                with sc2:
                    st.markdown(f"<div style='font-size: 0.95rem; color: #666; border-left: 2px solid #E0DCD5; padding-left: 10px;'>{sub}</div>", unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 5px 0; border: none; border-top: 1px dashed #E0DCD5;'>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)


# ==============================================================================
# Part II: 中文译本
# ==============================================================================
st.markdown("""
<div style="border-left: 3px solid #8B5A2B; padding-left: 20px; margin-bottom: 30px; margin-top: 40px;">
    <h3 style="margin: 0;">Part II: Chinese Translations</h3>
    <p style="font-size: 0.95rem; color: #888; margin-top: 5px;">Yilin Press Editions & Others</p>
</div>
""", unsafe_allow_html=True)

# --- 数据定义 ---
red_data = {
    "title": "🔴 译林·红版 (早期经典)",
    "dl_file": "Yilin_Red_Pack.zip", 
    "image_path": "./assets/red_book_cover.jpg", 
    "books": [
        {"name": "《自传：回忆、梦、思考》", "note": "必读入门"},
        {"name": "《心理学与文学》", "note": "C.W. 15 节选"},
        {"name": "《分析心理学的理论与实践》", "note": "1935年塔维斯托克讲座"},
        {"name": "《心理分析与梦的诠释》", "note": "C.W. 16 节选"},
        {"name": "《精神分析与灵魂治疗》", "note": "C.W. 11 节选"},
        {"name": "《潜意识与心灵成长》", "note": "《Man and His Symbols》,推荐立绪文化版"},
        {"name": "《心理类型》 (吴康译)", "note": "C.W. 6"},
    ]
}

white_data = {
    "title": "⚪ 译林·白版 (进阶研究)",
    "dl_file": "Yilin_White_Pack.zip",
    "image_path": "./assets/white_book_cover.jpg",
    "books": [
        {"name": "《心理学与炼金术》", "note": "C.W. 12 Part 1 & 3"},
        {"name": "《东方的智慧》", "note": "C.W. 11 节选"},
        {"name": "《伊雍：自性现象学研究》", "note": "C.W. 9 Part 2"},
        {"name": "《炼金术之梦》", "note": "C.W. 12 Part 2"},
        {"name": "《英雄与母亲》", "note": "C.W. 5 节选（PART2）"},
        {"name": "《哲学树》", "note": "C.W. 13 节选"},
        {"name": "《移情心理学》", "note": "C.W. 16 节选"},
        {"name": "《精灵墨丘利》", "note": "C.W. 13 节选"},
    ]
}

changchun_data = {
    "title": "📚 荣格文集 (2014长春出版社)",
    "dl_file": "", # 如有文件可填
    "image_path": "", # 如有图片可填
    "books": [
        {"name": "《1》", "note": "待补充"},
        {"name": "《2》", "note": "待补充"},
        {"name": "《3》", "note": "待补充"},
        {"name": "《4》", "note": "待补充"},
        {"name": "《5》", "note": "待补充"},
        {"name": "《6》", "note": "待补充"},
        {"name": "《7》", "note": "待补充"},
        {"name": "《8》", "note": "待补充"},
        {"name": "《9》", "note": "待补充"},
    ]
}

other_data = {
    "title": "📚 其他国内译本",
    "dl_file": "",
    "image_path": "",
    "books": [
        {"name": "《待补充》", "note": "待补充"},
    ]
}

# --- 渲染函数 ---
def render_chinese_block(data_dict):
    """渲染一个中文译本区块"""
    c_content, c_img = st.columns([3, 1], gap="large") 
    
    with c_content:
        # 标题头与下载按钮
        h_col, d_col = st.columns([2, 1])
        with h_col: st.markdown(f"#### {data_dict['title']}")
        with d_col: render_download_btn(data_dict['dl_file'], label="打包下载", unique_key=f"dl_{data_dict['title']}")
        
        st.markdown("---")
        
        # 小表格表头
        st.markdown("""
        <div style="display: grid; grid-template-columns: 2fr 1fr; font-weight: bold; color: #8B5A2B; font-size: 1rem; margin-bottom: 10px;">
            <div>书名 (Title)</div><div>备注 (Note)</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 渲染书籍行
        for book in data_dict['books']:
            bc1, bc2 = st.columns([2, 1])
            # 【修改】：单独放大表格内文字
            with bc1: st.markdown(f"<span style='color:#555; font-size: 1.1rem;'>{book['name']}</span>", unsafe_allow_html=True)
            with bc2: st.markdown(f"<span style='color:#888; font-size: 0.95rem;'>{book['note']}</span>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 5px 0; border: none; border-top: 1px dashed #E0DCD5;'>", unsafe_allow_html=True)

    with c_img:
        # 右侧图片展示区
        img_path = data_dict.get("image_path")
        if img_path and os.path.exists(img_path):
            st.image(img_path, width=200) # 固定宽度200
        else:
            st.markdown(f"""
            <div style="width: 200px; height: 260px; background-color: #F0EBE0; border: 2px dashed #D3C4B1; display: flex; align-items: center; justify-content: center; color: #999; font-size: 0.8rem; text-align: center; padding: 10px;">
                此处可放置<br>{data_dict['title'][:4]}<br>封面
            </div>
            """, unsafe_allow_html=True)

# --- 【关键修正】调用渲染函数 ---
# 只有在这里调用了，网页上才会显示
render_chinese_block(red_data)
st.markdown("<br>", unsafe_allow_html=True)
render_chinese_block(white_data)
st.markdown("<br>", unsafe_allow_html=True)
render_chinese_block(changchun_data) # 新增：长春版
st.markdown("<br>", unsafe_allow_html=True)
render_chinese_block(other_data)     # 新增：其他版

st.markdown("<br><br>", unsafe_allow_html=True)


# ==============================================================================
# Part III: 后荣格学派 (完美修复版：无代码块Bug + 新增Murray Stein)
# ==============================================================================
st.markdown("""
<div style="border-left: 3px solid #8B5A2B; padding-left: 20px; margin-bottom: 30px;">
    <h3 style="margin: 0;">Part III: Post-Jungian Scholars</h3>
</div>
""", unsafe_allow_html=True)

# --- 数据区 ---
scholars = [
    {
        "name": "Edward Edinger (爱德华·爱丁格)",
        "intro": "美国荣格心理学派的领军人物，被誉为“最接近荣格的人”。",
        # 详细生平
        "bio": """Edward F. Edinger (December 13, 1922, in Cedar Rapids, Iowa – July 17, 1998, in Los Angeles, California) was a medical psychiatrist, Jungian analyst and American writer.<br><br>爱德华·F·艾丁格（1922 年 12 月 13 日出生于爱荷华州锡达拉普斯——1998 年 7 月 17 日逝世于加利福尼亚州洛杉矶）是一位医学精神病学家、荣格分析师和美国作家。""",
        # 维基链接
        "wiki": "https://en.wikipedia.org/wiki/Edward_F._Edinger",
        "image": "./assets/Edward Edinger.png", 
        "books": [
            {"title": "Ego and Archetype", "note": "必读神作", "file": "Edinger_Ego.pdf"},
            {"title": "The Creation of Consciousness", "note": "意识的创造", "file": ""},
        ]
    },
    {
        "name": "Marie-Louise von Franz (冯·法兰兹)",
        "intro": "荣格最亲密的合作者，也是他思想的继承人。",
        # 详细生平
        "bio": """Marie-Louise von Franz (1915–1998) was a Swiss Jungian analyst and scholar, known for her psychological interpretations of fairy tales and of alchemical manuscripts. She worked and collaborated with Carl Jung from 1933, when she met him, until he died in 1961.<br><br>玛丽-路易斯·冯·弗兰兹（1915–1998）是一位瑞士荣格派分析师和学者，以其对童话和炼金术手稿的心理解读而闻名。她从 1933 年遇见荣格开始，直到 1961 年荣格去世，一直与他共事并合作。""",
        # 维基链接
        "wiki": "https://en.wikipedia.org/wiki/Marie-Louise_von_Franz",
        "image": "./assets/Marie-Louise-von-Franz.jpg",
        "books": [
            {"title": "The Interpretation of Fairy Tales", "note": "童话解读", "file": ""},
        ]
    },
    # 【新增实例】 Murray Stein
    {
        "name": "Murray Stein (默里·斯泰因)",
        "intro": "当代著名的荣格派分析师，曾任国际分析心理学会（IAAP）主席。",
        "bio": """Murray Stein (born 1943) is a graduate of Yale University and the C.G. Jung Institute Zurich. He is a training and supervising analyst at the International School of Analytical Psychology in Zurich (ISAPZurich). His writings have been crucial in structuring Jungian psychology for the modern era.<br><br>默里·斯泰因（1943年出生）毕业于耶鲁大学和苏黎世荣格学院。他是苏黎世国际分析心理学学院（ISAPZurich）的培训和督导分析师。他的著作为现代读者系统化理解荣格心理学做出了巨大贡献。""",
        "wiki": "https://www.murraystein.com/wp/",
        "image": "./assets/Murray Stein.jpg", 
        "books": [
            {"title": "Jung's Map of the Soul", "note": "荣格心灵地图 (最好的入门书)", "file": ""},
            {"title": "Transformation", "note": "转化：自性的显现", "file": ""},
        ]
    }
]

# --- 渲染区  ---
for i, scholar in enumerate(scholars):
    with st.container():
        # 1. 学者卡片区域
        col_img, col_desc = st.columns([1, 5], gap="medium")
        with col_img:
            if os.path.exists(scholar.get('image', '')): st.image(scholar['image'], width=220) 
            else: st.markdown(f"<div style='width:220px; height:220px; background-color:#E0DCD5; display:flex; align-items:center; justify-content:center; color:#888; border-radius: 4px;'>暂无照片</div>", unsafe_allow_html=True)
        
        with col_desc:
            st.markdown(f"<h4 style='margin:0; color:#8B5A2B; font-size: 1.4rem;'>{scholar['name']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#2C2C2C; font-weight:bold; font-size:1.1rem; margin-top:10px;'>{scholar['intro']}</p>", unsafe_allow_html=True)

            if "bio" in scholar:
                st.markdown(f"<p style='color:#555; font-size:1rem; line-height:1.6; margin-top:8px; border-left: 2px solid #E0DCD5; padding-left: 10px;'>{scholar['bio']}</p>", unsafe_allow_html=True)
            if "wiki" in scholar:
                st.markdown(f"<div style='margin-top: 10px;'><a href='{scholar['wiki']}' target='_blank' style='color: #8B5A2B; font-family: Cormorant Garamond; border-bottom: 1px dotted #8B5A2B;'>🌐 Read more on Personal Website →</a></div>", unsafe_allow_html=True)
         
         # 2. 书籍列表区
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 【[需求3] 完美包裹】使用原生容器，自带边框，完美统一
            with st.container(border=True):
                st.markdown(f"<div style='font-weight:bold; color:#8B5A2B; margin-bottom:10px;'>📖 Recommended Readings</div>", unsafe_allow_html=True)
                for book in scholar['books']:
                    b_col1, b_col2, b_col3 = st.columns([3, 2, 1.2])
                    with b_col1: st.markdown(f"<span style='font-family:Cormorant Garamond; font-size:1.15rem; font-weight:600;'>{book['title']}</span>", unsafe_allow_html=True)
                    with b_col2: st.markdown(f"<span style='font-size:1rem; color:#666;'>{book['note']}</span>", unsafe_allow_html=True)
                    with b_col3: render_download_btn(book['file'], label="PDF", unique_key=f"s_{i}_{book['title']}") # 按钮文字改短为 PDF，更显精致
                    
        st.markdown("<hr style='margin-top: 30px; margin-bottom: 30px; border-top: 1px solid #E0DCD5;'>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

#-------页脚
render_footer()