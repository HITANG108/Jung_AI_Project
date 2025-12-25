import sys
# 强制将标准输出设置为 utf-8，解决 Windows 终端乱码
sys.stdout.reconfigure(encoding='utf-8')

from openai import OpenAI

# ----------------------------------------------------------
# 配置区域：请在这里填入你的钥匙和地址
# ----------------------------------------------------------

# 1. 把你的 sk- 开头的长串密钥填在引号里
MY_API_KEY = "sk-6CqRNrrPMboZ8tqVbvAZ8wkCV0Wcf3jvpTBJ3hTRvneOnK80" 

# 2. 如果你用的是 DeepSeek，保持下面这个地址不要动
#    如果你用的是 Kimi (Moonshot)，把下面改成 "https://api.moonshot.cn/v1"
#BASE_URL = "https://api.deepseek.com" 
BASE_URL = "https://api.moonshot.cn/v1" 

# ----------------------------------------------------------
# 初始化客户端（建立连接通道）
# ----------------------------------------------------------
client = OpenAI(
    api_key=MY_API_KEY,
    base_url=BASE_URL,
)

print("Trying to connect with Jung's soul...")

# ----------------------------------------------------------
# 发送消息（核心咒语）
# ----------------------------------------------------------
response = client.chat.completions.create(
    #model="deepseek-chat",  # 如果是 Kimi，这里改成 "moonshot-v1-8k"
    model="moonshot-v1-8k",
    messages=[
        # System: 这里定义 AI 的“人格面具”。告诉它它是谁。
        {"role": "system", "content": "You are now the renowned psychologist Carl Gustav Jung. Please speak to me in a profound, philosophical, and warm tone. Don't act like a robot; act like a wise old man."},
        
        # User: 这里是你对它说的话。
        {"role": "user", "content": "Mr. Jung, I feel like a child who has just received a new toy, but I don't know where to go next. Can you give me some guidance?"},
    ],
    temperature=0.7, # 这个数字控制“创造力”。越高越发散，越低越严谨。
)

# ----------------------------------------------------------
# 接收并打印回复
# ----------------------------------------------------------
answer = response.choices[0].message.content
print("\n" + "="*30)
print("【Jung's reply】:")
print(answer)
print("="*30 + "\n")