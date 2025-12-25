import os
# 设置环境变量，强迫 Python 内部用 utf-8 处理数据
os.environ["PYTHONIOENCODING"] = "utf-8"

from openai import OpenAI

# ----------------------------------------------------------
# 1. 填入你的 Key (DeepSeek 或 Kimi)
# ----------------------------------------------------------
MY_API_KEY = "sk-6CqRNrrPMboZ8tqVbvAZ8wkCV0Wcf3jvpTBJ3hTRvneOnK80" 

BASE_URL = "https://api.moonshot.cn/v1" 

client = OpenAI(
    api_key=MY_API_KEY,
    base_url=BASE_URL,
)

print("正在尝试连接荣格的灵魂...（请稍等，结果将写入文件）")

try:
    # ----------------------------------------------------------
    # 发送请求
    # ----------------------------------------------------------
    response = client.chat.completions.create(
        model="moonshot-v1-8k",  # Kimi 改为 "moonshot-v1-8k"
        messages=[
            {"role": "system", "content": "你现在是著名的心理学家卡尔·古斯塔夫·荣格。请用深邃、富有哲理且温暖的语气与我对话。不要像个机器人，要像一位充满智慧的老者。"},
            {"role": "user", "content": "荣格先生，我现在感觉像个拿到新玩具的孩子，但我不知道下一步该往哪走，你能给我一句指引吗？"},
        ],
        temperature=0.7,
    )

    answer = response.choices[0].message.content

    # ----------------------------------------------------------
    # 核心修改：不再打印到黑框框，而是写入文件
    # ----------------------------------------------------------
    # 在当前目录下创建一个叫 jung_reply.txt 的文件
    with open("jung_reply.txt", "w", encoding="utf-8") as f:
        f.write("【荣格的回信】:\n")
        f.write(answer)

    print("-" * 30)
    print("成功了！请在你的文件夹里打开 'jung_reply.txt' 查看回信。")
    print("-" * 30)

except Exception as e:
    print("发生错误：", e)