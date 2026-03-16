# 01-HELLO LangChain

## 学习目标

通过本模块，你将学习：

1. **LangChain 1.0 的核心概念**
   - **LangChain 1.0 构建在 LangGraph 运行时之上**
   - 统一的模型初始化接口
   - 简化的 API 设计

2. **init_chat_model 函数**
   - 如何初始化聊天模型
   - 支持的参数和配置选项
   - 跨模型提供商的统一接口

3. **invoke 方法**
   - 同步调用模型
   - 输入格式（字符串、消息列表、字典）
   - 返回值结构

4. **Messages（消息类型）**
   - SystemMessage：系统提示
   - HumanMessage：用户输入
   - AIMessage：AI 响应

---

## 初始化一个模型（init_chat_model）
> init_chat_model: 统一的模型接入入口，
> 注意：需要下载对应的lagnchain_模型以来，例如:uv add langchain-groq

### 基本语法

```python
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "provider:model_name",  # 提供商:模型名称
    api_key="your-api-key",  # API 密钥（可选，可从环境变量读取）
    temperature=0.7,         # 温度参数（可选）
    max_tokens=1000,         # 最大 token 数（可选）
    **kwargs                 # 其他模型特定参数
)
```


### 参数详解

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `model` | `str` | **必需**。格式为 `"provider:model_name"`，如 `"groq:llama-3.3-70b-versatile"` | 无 |
| `api_key` | `str` | API 密钥。如果不提供，会从环境变量中读取（如 `GROQ_API_KEY`） | `None` |
| `temperature` | `float` | 控制输出随机性。范围 0.0-2.0。<br>- `0.0`：最确定性<br>- `1.0`：默认，平衡<br>- `2.0`：最随机 | `1.0` |
| `max_tokens` | `int` | 限制模型输出的最大 token 数量 | 模型默认值 |
| `model_kwargs` | `dict` | 传递给底层模型的额外参数 | `{}` |


## 调用（invoke）***
> 最核心的方法


简单来说，`invoke` 方法的作用就是：

1. **接收你的输入**（问题、指令、对话历史等）
2. **发送给 LLM 模型**（如 GPT-4, Llama, Claude 等）
3. **返回模型的响应**（文本回复 + 元数据信息）

**流程图：**
```
你的输入 → invoke() → LLM 模型 → 响应 → 返回给你
```

---

### 基本语法
```python

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

```


**参数详解：**

| 参数 | 类型 | 说明 | 必需 | 默认值 |
|------|------|------|------|--------|
| `input` | `str` \| `list[dict]` \| `list[Message]` | 你要发送给模型的内容 | ✅ 必需 | 无 |
| `config` | `dict` | 高级配置（回调函数、元数据、标签等） | ❌ 可选 | `None` |

---

#### 🔍 深入理解 input 参数 - 三种输入格式

这是最容易困惑的地方！`invoke` 支持**三种不同的输入格式**，让我们逐一详解：

---


##### 📌 格式 1：纯字符串（最简单，适合单次问答）

**使用场景：** 简单的一次性问答，不需要设置系统角色或对话历史

**语法：**
```python
response = model.invoke("你的问题或指令")
```

**完整示例：**
```python
from langchain.chat_models import init_chat_model

model = init_chat_model("groq:llama-3.3-70b-versatile", api_key="your_key")

# 直接传递字符串
response = model.invoke("什么是机器学习？用一句话解释")

print(response.content)
# 输出：机器学习是一种让计算机通过数据学习规律，而无需明确编程的技术。
```

**优点：**
- ✅ 最简单，代码最少
- ✅ 适合快速测试

**缺点：**
- ❌ 无法设置系统提示（system prompt）
- ❌ 无法传递对话历史
- ❌ 灵活性较低

**什么时候用？**
- 快速测试
- 简单的一次性问答
- 不需要上下文的场景

---

##### 📌 格式 2：消息对象列表（类型安全，但较繁琐）

**使用场景：** 需要类型检查、IDE 自动补全的场景

**语法：**
```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage(content="系统提示"),
    HumanMessage(content="用户消息"),
    AIMessage(content="AI回复")
]
response = model.invoke(messages)
```

**消息类型对照：**

| 消息类 | 对应字典格式 | 作用 |
|--------|-------------|------|
| `SystemMessage` | `{"role": "system", ...}` | 系统提示 |
| `HumanMessage` | `{"role": "user", ...}` | 用户输入 |
| `AIMessage` | `{"role": "assistant", ...}` | AI 回复 |

**完整示例：**
```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage(content="你是一个 Python 专家"),
    HumanMessage(content="什么是生成器？"),
]

response = model.invoke(messages)

# 继续对话
messages.append(AIMessage(content=response.content))
messages.append(HumanMessage(content="能给个例子吗？"))

response2 = model.invoke(messages)
```

**优点：**
- ✅ 类型安全
- ✅ IDE 自动补全
- ✅ 更容易发现错误

**缺点：**
- ❌ 代码较长
- ❌ 不如字典简洁
- ❌ 难以序列化（JSON）

**什么时候用？**
- 大型项目，需要类型检查
- 团队协作，需要严格规范
- 使用 TypeScript/MyPy 等类型检查工具

---



##### 📌 格式 3：字典列表（推荐，最灵活）

**使用场景：** 需要设置系统角色、多轮对话、精确控制对话流程


**语法：**
```python
messages = [
    {"role": "system", "content": "系统提示"},
    {"role": "user", "content": "用户消息"},
    {"role": "assistant", "content": "AI回复"},  # 可选，用于对话历史
    {"role": "user", "content": "继续提问"}
]
response = model.invoke(messages)
```

**角色说明：**

| 角色 | 英文 | 作用 | 示例 |
|------|------|------|------|
| `system` | System | 设定 AI 的行为、角色、规则 | "你是一个专业的 Python 导师" |
| `user` | Human/User | 用户的输入/问题 | "什么是装饰器？" |
| `assistant` | AI/Assistant | AI 的历史回复（用于对话上下文） | "装饰器是一种设计模式..." |



**完整示例 1：设置系统提示**
```python
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

response = model.invoke(messages)
print(response.content)
```

**完整示例 2：多轮对话（带历史）这里理应持久化存储**
```python
# 第一轮对话
messages = [
    {"role": "system", "content": "你是一个友好的助手"},
    {"role": "user", "content": "我叫小明"}
]

response1 = model.invoke(messages)
print(response1.content)  # "你好，小明！很高兴认识你。"

# 第二轮对话 - 添加历史
messages.append({"role": "assistant", "content": response1.content})
messages.append({"role": "user", "content": "我刚才说我叫什么？"})

response2 = model.invoke(messages)
print(response2.content)  # "你说你叫小明。"
```

**完整示例 3：构建完整对话**
```python
# 初始化对话
conversation = [
    {"role": "system", "content": "你是一个 Python 专家"}
]

# 用户提问 1
conversation.append({"role": "user", "content": "什么是列表？"})
response1 = model.invoke(conversation)
print(f"AI: {response1.content}")

# 保存 AI 回复到历史
conversation.append({"role": "assistant", "content": response1.content})

# 用户提问 2（基于上下文）
conversation.append({"role": "user", "content": "它和元组有什么区别？"})
response2 = model.invoke(conversation)
print(f"AI: {response2.content}")

# 此时 conversation 包含完整的对话历史
print(f"\n完整对话历史: {conversation}")
```

**优点：**
- ✅ 最灵活，完全控制
- ✅ 可以设置系统提示
- ✅ 支持多轮对话
- ✅ 与 OpenAI API 格式一致
- ✅ JSON 兼容，易于存储和传输

**缺点：**
- ❌ 代码稍微多一点（但更清晰）

**什么时候用？**
- ✅ **推荐用于所有场景**
- 需要设置系统角色
- 多轮对话
- 需要保存对话历史
- 生产环境应用

---


#### 🎁 invoke 返回值详解

`invoke` 返回一个 **AIMessage 对象**，包含丰富的信息：

**返回对象结构：**
```python
response = model.invoke("Hello")

# 1. 主要内容
response.content              # str - AI 的回复文本
response.response_metadata    # dict - 响应元数据
response.id                   # str - 消息唯一 ID
response.usage_metadata       # dict - Token 使用情况
response.additional_kwargs    # dict - 其他额外信息
```

**完整示例：访问所有信息**
```python
response = model.invoke("用一句话解释什么是 AI")

# 1. 获取回复内容
print("AI 回复:", response.content)

# 2. 获取模型信息
metadata = response.response_metadata
print(f"使用的模型: {metadata['model_name']}")
print(f"结束原因: {metadata['finish_reason']}")

# 3. 获取 Token 使用情况
usage = metadata.get('token_usage', {})
print(f"提示 tokens: {usage.get('prompt_tokens')}")
print(f"完成 tokens: {usage.get('completion_tokens')}")
print(f"总计 tokens: {usage.get('total_tokens')}")

# 4. 获取消息 ID
print(f"消息 ID: {response.id}")
```

**response_metadata 完整结构：**
```python
{
    'model_name': 'llama-3.3-70b-versatile',      # 使用的模型
    'system_fingerprint': 'fp_4cfc2deea6',        # 系统指纹
    'finish_reason': 'stop',                      # 结束原因：stop/length/error
    'model_provider': 'groq',                     # 模型提供商
    'token_usage': {                              # Token 使用统计
        'prompt_tokens': 15,                      # 输入 tokens
        'completion_tokens': 25,                  # 输出 tokens
        'total_tokens': 40,                       # 总计 tokens
        'prompt_time': 0.002,                     # 输入处理时间（秒）
        'completion_time': 0.23                   # 输出生成时间（秒）
    }
}
```

---


## 常见问题 (FAQ)

### Q1: 为什么推荐使用字典格式而不是消息对象？

**A:** 两种方式都可以，但字典格式有以下优势：
- 更简洁，代码量更少
- 与 OpenAI API 格式一致
- 更容易序列化和存储
- JSON 兼容，便于网络传输

### Q2: 如何处理 API 调用失败？

**A:** 使用 try-except 块捕获异常：

```python
try:
    response = model.invoke("Hello")
    print(response.content)
except ValueError as e:
    print(f"配置错误: {e}")
except ConnectionError as e:
    print(f"网络错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

---