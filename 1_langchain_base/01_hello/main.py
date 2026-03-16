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

# ============================================================================
# 示例 1：最简单的 LLM 调用
# ============================================================================
def example_1_simple_invoke():
    """
    示例1：最简单的模型调用

    核心概念：
    - init_chat_model: 用于初始化聊天模型的统一接口
    - invoke: 同步调用模型的方法
    """
    print("\n" + "="*70)
    print("示例 1：最简单的 LLM 调用")
    print("="*70)

    # 初始化模型
    # 格式：init_chat_model("提供商:模型名称")
    # 使用文件开头初始化的 model

    # 使用字符串直接调用模型
    response = model.invoke("你好！请用一句话介绍什么是人工智能。")

    print(f"用户输入: 你好！请用一句话介绍什么是人工智能。")
    print(f"AI 回复: {response.content}")
    print(f"\n返回对象类型: {type(response)}")
    print(f"返回对象: {response}")


# ============================================================================
# 示例 2：使用消息列表进行对话
# ============================================================================
def example_2_messages():
    """
    示例2：使用消息列表

    核心概念：
    - SystemMessage: 系统消息，用于设定 AI 的行为和角色
    - HumanMessage: 用户消息
    - AIMessage: AI 的回复消息

    消息列表允许你构建多轮对话历史
    """
    print("\n" + "="*70)
    print("示例 2：使用消息列表构建对话")
    print("="*70)

    # model 已在文件开头通过 get_model() 初始化

    # 构建消息列表
    messages = [
        SystemMessage(content="你是一个友好的 Python 编程助手，擅长用简单易懂的方式解释编程概念。 回答字数不超过100字。"),
        HumanMessage(content="什么是 Python 装饰器？ "),
    ]

    print("系统提示:", messages[0].content)
    print("用户问题:", messages[1].content)

    # 调用模型
    response = model.invoke(messages)

    print(f"\nAI 回复:\n{response.content}")

    # 继续对话：将 AI 的回复添加到对话历史
    messages.append(response)
    messages.append(HumanMessage(content="能给我一个简单的例子吗？"))

    print("\n" + "-"*70)
    print("继续对话...")
    print("用户问题:", messages[-1].content)

    response2 = model.invoke(messages)
    print(f"\nAI 回复:\n{response2.content}")


# ============================================================================
# 示例 3：使用字典格式的消息
# ============================================================================
def example_3_dict_messages():
    """
    示例3：使用字典格式的消息

    LangChain 1.0 支持更简洁的字典格式：
    {"role": "system"/"user"/"assistant", "content": "消息内容"}

    这种格式与 OpenAI API 的格式一致，更易于使用
    """
    print("\n" + "="*70)
    print("示例 3：使用字典格式的消息（推荐）")
    print("="*70)

    # model 已在文件开头通过 get_model() 初始化

    # 使用字典格式构建消息

    messages = [
        {
            "role": "system",
            "content": "你是一个专业的 Python 编程导师。回答要简洁、准确，并提供代码示例。"
        },
        {
            "role": "user",
            "content": "什么是 Python 列表推导式？"
        }
    ]

    print("消息列表:")
    for msg in messages:
        print(f"  {msg['role']}: {msg['content']}")

    response = model.invoke(messages)

    print(f"\nAI 回复:\n{response.content}")


# ============================================================================
# 示例 4：配置模型参数
# ============================================================================
def example_4_model_parameters():
    """
    示例4：配置模型参数

    init_chat_model 支持的常用参数：
    - temperature: 控制输出的随机性（0.0-2.0）
      * 0.0: 最确定性，输出几乎不变
      * 1.0: 默认值，平衡创造性和一致性
      * 2.0: 最随机，最有创造性
    - max_tokens: 限制输出的最大 token 数量
    - model_kwargs: 传递给底层模型的额外参数
    """
    print("\n" + "="*70)
    print("示例 4：配置模型参数")
    print("="*70)

    # 创建一个温度较低的模型（更确定性）
    model_deterministic = init_chat_model(
        "groq:llama-3.3-70b-versatile",
        temperature=0.0,  # 最确定性
        max_tokens=100    # 限制输出长度
    )

    prompt = "写一个关于春天的句子。"

    print(f"提示词: {prompt}")
    print("\n使用 temperature=0.0 (确定性输出):")

    # 调用两次，观察输出的一致性
    for i in range(2):
        response = model_deterministic.invoke(prompt)
        print(f"  第 {i+1} 次: {response.content}")

    print("\n" + "-"*70)

    # 创建一个温度较高的模型（更随机）
    model_creative = init_chat_model(
        "groq:llama-3.3-70b-versatile",
        temperature=1.5,  # 更有创造性
        max_tokens=100
    )

    print("\n使用 temperature=1.5 (创造性输出):")
    # 调用两次，观察输出的差异
    for i in range(2):
        response = model_creative.invoke(prompt)
        print(f"  第 {i + 1} 次: {response.content}")

    # 创建一个温度最高的模型（更随机）
    model_creative_max = init_chat_model(
        "groq:llama-3.3-70b-versatile",
        temperature=2.0,  # 最高温度
        max_tokens=1500
    )

    print("\n使用 temperature=2.0 (创造性输出):")

    # 调用两次，观察输出的差异
    for i in range(2):
        response = model_creative_max.invoke(prompt)
        print(f"  第 {i+1} 次: {response.content}")


# ============================================================================
# 示例 5：理解 invoke 方法的返回值
# ============================================================================
def example_5_response_structure():
    """
    示例5：深入理解 invoke 返回值

    invoke 方法返回一个 AIMessage 对象，包含：
    - content: 模型的文本回复
    - response_metadata: 响应元数据（如 token 使用量、模型信息等）
    - additional_kwargs: 额外的关键字参数
    - id: 消息 ID
    """
    print("\n" + "="*70)
    print("示例 5：invoke 返回值详解")
    print("="*70)

    # model 已在文件开头通过 get_model() 初始化

    response = model.invoke("解释一下什么是递归？用一句话。")

    print("1. 主要内容 (content):")
    print(f"   {response.content}\n")

    print("2. 响应元数据 (response_metadata):")
    for key, value in response.response_metadata.items():
        print(f"   {key}: {value}")

    print(f"\n3. 消息类型: {type(response).__name__}")
    print(f"4. 消息 ID: {response.id}")

    # 检查 token 使用情况（如果可用）
    if "token_usage" in response.response_metadata:
        usage = response.response_metadata["token_usage"]
        print("\n5. Token 使用情况:")
        print(f"   提示 tokens: {usage.get('prompt_tokens', 'N/A')}")
        print(f"   完成 tokens: {usage.get('completion_tokens', 'N/A')}")
        print(f"   总计 tokens: {usage.get('total_tokens', 'N/A')}")


if __name__ == '__main__':
    example_5_response_structure()