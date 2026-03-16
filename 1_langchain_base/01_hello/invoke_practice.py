import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 加载环境变量
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
    raise ValueError(
        "\n请先在 .env 文件中设置有效的 GROQ_API_KEY\n"
        "访问 https://console.groq.com/keys 获取免费密钥"
    )

# 初始化模型
model = init_chat_model("groq:llama-3.3-70b-versatile", api_key=GROQ_API_KEY)


def chatBot():
    """
        练习目标：综合运用所学知识，构建一个简单的聊天机器人
    """
    # 系统提示词
    context = [
        {"role":"system", "content":"你是豆包"}
    ]

    total_tokens_used = 0
    turn = 0

    # 模拟几轮对话（非交互式）
    demo_questions = [
        "你好！",
        "你能做什么？",
        "告诉我一个编程笑话",
        "我想学 Python，有什么建议吗？"
    ]

    for question in demo_questions:
        turn += 1
        print(f"\n--- 第 {turn} 轮 ---")
        print(f"用户：{question}")

        # 添加用户消息
        context.append({"role": "user", "content": question})

        # 调用模型
        response = model.invoke(context)

        # 显示 AI 回复
        print(f"AI：{response.content}")

        # 统计 token
        usage = response.response_metadata.get('token_usage', {})
        tokens = usage.get('total_tokens', 0)
        total_tokens_used += tokens
        print(f"[本轮使用 {tokens} tokens，累计 {total_tokens_used} tokens]")

        # 保存 AI 回复到历史
        context.append({"role": "assistant", "content": response.content})

    print("\n" + "="*70)
    print(f"对话结束！共进行 {turn} 轮对话")
    print(f"总计使用 {total_tokens_used} tokens")
    print(f"对话历史包含 {len(context)} 条消息")
    print("="*70)

if __name__ == '__main__':
    chatBot()