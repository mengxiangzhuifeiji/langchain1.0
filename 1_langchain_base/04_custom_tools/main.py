import os
import sys

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

# 加载环境变量
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
    raise ValueError(
        "\n请先在 .env 文件中设置有效的 GROQ_API_KEY\n"
        "访问 https://console.groq.com/keys 获取免费密钥"
    )

# 添加tools目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tool'))

# 初始化模型
model = init_chat_model("groq:llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

from time_tool import time_tool

if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here_replace_this":
    raise ValueError(
        "\n请先在 .env 文件中设置有效的 GROQ_API_KEY\n"
        "访问 https://console.groq.com/keys 获取免费密钥"
    )

# 绑定工具
model_with_tools = model.bind_tools([time_tool])

# ============================================================================
# 示例：模型调用工具
# ============================================================================
def example_1_why_templates():
    original_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个{role}，你的目标用户是{audience}。"),
        ("user", "请{task}")
    ])

    message = original_template.format_messages(role="智能小管家", audience="程序员", task="告诉我当前时间")
    content = model_with_tools.invoke(message)
    if content.tool_calls:
        print("AI 想调用工具：", content.tool_calls)
    else:
        print("AI 直接回答：", content.content)
    print("="*10)
    # 注意：这里是没有真实的调用工具的，模型只是想，但是目前并没有agent，所以没有东西去接收到指令然后去调用
    print(content)

if __name__ == '__main__':
    example_1_why_templates()
