import os
import sys

# 1. 解决 Windows 终端输出乱码问题
sys.stdout.reconfigure(encoding='utf-8')

# ==========================================
# 配置区域 (请修改这里)
# ==========================================
# 填入你的 Key (保留引号)
MY_API_KEY = "sk-6CqRNrrPMboZ8tqVbvAZ8wkCV0Wcf3jvpTBJ3hTRvneOnK80" 

# 如果是 DeepSeek，保持这个；如果是 Kimi，改成 "https://api.moonshot.cn/v1"
MY_BASE_URL = "https://api.moonshot.cn/v1"

# 书籍文件的路径 (请确保文件是 UTF-8 编码的 txt)
BOOK_PATH = "./data/Man and His Symbols.txt"

# ==========================================
# 核心逻辑
# ==========================================

print("正在初始化荣格的大脑，请稍候...")
print("提示：第一次运行会下载嵌入模型（约80MB），请保持网络通畅，耐心等待...")

try:
    # 导入必要的库
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    # 这里使用了新版的 HuggingFace 库
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_openai import ChatOpenAI
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain_core.prompts import ChatPromptTemplate

    # ------------------------------------------------
    # 第一阶段：吃书（Ingestion）
    # ------------------------------------------------
    
    if not os.path.exists(BOOK_PATH):
        print(f"❌ 错误：找不到文件 {BOOK_PATH}")
        print("请检查：1. data文件夹是否存在？ 2. jung_book.txt是否在里面？")
        sys.exit()

    print(f"📖 正在读取书籍：{BOOK_PATH} ...")
    
    # 尝试用 utf-8 读取，如果报错可能是编码问题
    try:
        loader = TextLoader(BOOK_PATH, encoding='utf-8')
        docs = loader.load()
    except UnicodeDecodeError:
        print("⚠️ 警告：UTF-8 读取失败，尝试使用系统默认编码...")
        loader = TextLoader(BOOK_PATH, autodetect_encoding=True)
        docs = loader.load()

    print(f"✅ 成功读取，全书共 {len(docs[0].page_content)} 个字符。")

    # 切片
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,    # 每块的大小
        chunk_overlap=50,  # 重叠部分
    )
    splits = text_splitter.split_documents(docs)
    print(f"✂️ 已将书籍切分为 {len(splits)} 个记忆碎片。")

    # 向量化
    print("🧠 正在加载嵌入模型 (all-MiniLM-L6-v2)...")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("💾 正在存入向量数据库 (ChromaDB)...")
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embedding_model, 
        persist_directory="./chroma_db" # 数据会存在这里
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # ------------------------------------------------
    # 第二阶段：构建对话大脑
    # ------------------------------------------------

    # 定义大模型
    llm = ChatOpenAI(
        api_key=MY_API_KEY,
        base_url=MY_BASE_URL,
        model="moonshot-v1-8k", 
        temperature=0.7
    )

    # 定义提示词
    system_prompt = (
        "你现在是著名的心理学家卡尔·古斯塔夫·荣格。你面前坐着一位年轻的朋友。"
        "请根据下面的【背景知识】来回答他的问题。"
        "【背景知识】是一本英文心理学著作，但你必须消化理解后，用**中文**回答。"
        "回答风格要求：深邃、温暖、富有哲理，像一位智者与朋友谈心。"
        "如果背景知识里没有直接答案，请基于你的心理学理论进行推测，但不要胡编乱造。"
        "\n\n"
        "【背景知识】:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # ------------------------------------------------
    # 第三阶段：开始聊天
    # ------------------------------------------------
    print("\n" + "="*50)
    print("🕯️ 荣格医师已就座。")
    print("你可以问我关于《人及其象征》的问题，或者聊聊你的梦。")
    print("（输入 'quit' 或 'exit' 退出聊天）")
    print("="*50)

    while True:
        user_input = input("\n你: ")
        if user_input.lower() in ["quit", "exit"]:
            print("荣格: 愿自性的光芒指引你。再见。")
            break
        
        if not user_input.strip():
            continue

        print("Thinking...", end="", flush=True)
        response = rag_chain.invoke({"input": user_input})
        
        # 这里的 \r 是为了把 "Thinking..." 覆盖掉，让体验更好
        print(f"\r荣格: {response['answer']}")

except Exception as e:
    print("\n❌ 发生严重错误：")
    print(e)
    print("--------------------------------")
    print("建议：如果是网络错误，请检查网络连接；如果是缺少库，请运行安装命令。")