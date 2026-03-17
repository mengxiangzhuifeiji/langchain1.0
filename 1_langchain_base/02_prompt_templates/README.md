# 02 - Prompt Templates: 提示词模板

## 知识点

1. **为什么需要提示词模板**
   - 字符串拼接的问题
   - 模板的优势

2. **PromptTemplate**
   - 基本用法
   - 变量替换
   - 格式化方法

3. **ChatPromptTemplate**
   - 聊天消息模板
   - 多角色支持
   - 对话历史管理

4. **高级特性**
   - 部分变量
   - 模板组合
   - 可复用模板库


## 核心概念详解

### 1. 为什么需要提示词模板？

#### 🔴 问题：字符串拼接的缺点

```python
# ❌ 不推荐的做法
user_name = "张三"
topic = "Python"

prompt = f"你好 {user_name}，我来帮你学习 {topic}"
```

**问题：**
- ❌ 难以维护和修改
- ❌ 容易出现格式错误
- ❌ 不能复用
- ❌ 难以测试
- ❌ 混合了逻辑和数据

#### ✅ 解决方案：使用模板

```python
# ✅ 推荐的做法
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "你好 {user_name}，我来帮你学习 {topic}"
)

prompt = template.format(user_name="张三", topic="Python")
```
---


### 2. PromptTemplate - 简单文本模板

`PromptTemplate` 用于创建**简单的文本提示词**，适合单一提示的场景。

#### 基本语法

```python
from langchain_core.prompts import PromptTemplate

# 方法 1：from_template（最简单，推荐）
template = PromptTemplate.from_template("你的模板文本 {变量名}")

# 方法 2：完整定义
template = PromptTemplate(
    input_variables=["变量1", "变量2"],
    template="你的模板文本 {变量1} 和 {变量2}"
)
```

#### 创建模板的三种方法

**方法 1：from_template（推荐）**

```python
template = PromptTemplate.from_template(
    "将以下文本翻译成{language}：\n{text}"
)

# 自动识别变量
print(template.input_variables)  # ['language', 'text']
```

**方法 2：显式指定变量**

```python
template = PromptTemplate(
    input_variables=["product", "feature"],
    template="为{product}写一句广告语，重点突出{feature}特点。"
)
```

**方法 3：部分变量预填充**

```python
template = PromptTemplate.from_template(
    "你是一个{role}，请{task}"
)

# 预填充 role
partial_template = template.partial(role="Python 导师")

# 现在只需要提供 task
prompt = partial_template.format(task="解释装饰器")
```

#### 使用模板

**方式 1：format() - 返回字符串**

```python
template = PromptTemplate.from_template("你好 {name}")

# 返回格式化后的字符串
prompt_str = template.format(name="张三")
print(prompt_str)  # "你好 张三"

# 直接传递给模型
response = model.invoke(prompt_str)
```

**方式 2：invoke() - 返回 PromptValue**

```python
template = PromptTemplate.from_template("你好 {name}")

# 返回 PromptValue 对象
prompt_value = template.invoke({"name": "张三"})

# 获取文本
print(prompt_value.text)  # "你好 张三"
```

#### 实用示例

**示例 1：翻译模板**

```python
translator = PromptTemplate.from_template(
    "将以下{source_lang}文本翻译成{target_lang}：\n{text}"
)

prompt = translator.format(
    source_lang="英语",
    target_lang="中文",
    text="Hello, how are you?"
)
```

**示例 2：代码生成模板**

```python
code_generator = PromptTemplate.from_template(
    "用{language}编写一个{functionality}的函数。\n"
    "要求：\n"
    "1. {requirement1}\n"
    "2. {requirement2}"
)

prompt = code_generator.format(
    language="Python",
    functionality="计算斐波那契数列",
    requirement1="使用递归实现",
    requirement2="添加类型注解"
)
```

---

### 3. ChatPromptTemplate - 聊天消息模板

`ChatPromptTemplate` 用于创建**聊天格式的消息**，支持多种角色（system、user、assistant）。

#### 为什么需要 ChatPromptTemplate？

**PromptTemplate vs ChatPromptTemplate：**

| 特性 | PromptTemplate | ChatPromptTemplate |
|------|----------------|-------------------|
| 输出格式 | 纯文本字符串 | 消息列表 |
| 角色支持 | ❌ 无 | ✅ system/user/assistant |
| 对话历史 | ❌ 不支持 | ✅ 支持 |
| 适用场景 | 简单提示 | 聊天、对话、多轮交互 |

#### 基本语法

```python
from langchain_core.prompts import ChatPromptTemplate

# 使用元组格式（推荐）
template = ChatPromptTemplate.from_messages([
    ("system", "系统提示"),
    ("user", "用户消息 {variable}"),
    ("assistant", "AI 回复"),
    ("user", "下一个用户消息")
])
```

#### 消息类型

| 角色字符串 | 含义 | 用途 |
|-----------|------|------|
| `"system"` | 系统消息 | 设定 AI 的行为、角色、规则 |
| `"user"` / `"human"` | 用户消息 | 用户的输入/问题 |
| `"assistant"` / `"ai"` | AI 消息 | AI 的回复（用于对话历史） |

#### 创建方法

**方法 1：元组格式（最简单，推荐）**

```python
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}"),
    ("user", "{question}")
])

messages = template.format_messages(
    role="Python 导师",
    question="什么是装饰器？"
)
```

**方法 2：字符串简写**

```python
# 单独的字符串会被解释为 user 消息
template = ChatPromptTemplate.from_messages([
    ("system", "你是助手"),
    "{user_input}"  # 相当于 ("user", "{user_input}")
])
```

**方法 3：使用 MessagePromptTemplate（高级）**

```python
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

system_template = SystemMessagePromptTemplate.from_template(
    "你是一个{role}"
)
human_template = HumanMessagePromptTemplate.from_template(
    "{question}"
)

template = ChatPromptTemplate.from_messages([
    system_template,
    human_template
])
```

#### 使用模板

**方式 1：format_messages() - 返回消息列表**

```python
template = ChatPromptTemplate.from_messages([
    ("system", "你是{role}"),
    ("user", "{input}")
])

# 返回消息列表
messages = template.format_messages(
    role="助手",
    input="你好"
)

# 直接传递给模型
response = model.invoke(messages)
```

**方式 2：invoke() - 返回 ChatPromptValue**

```python
# 返回 ChatPromptValue 对象
prompt_value = template.invoke({
    "role": "助手",
    "input": "你好"
})

# 获取消息列表
messages = prompt_value.to_messages()
```

#### 实用示例

**示例 1：简单聊天**

```python
chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的{role}，擅长{skill}"),
    ("user", "{question}")
])

messages = chat_template.format_messages(
    role="编程导师",
    skill="用简单语言解释复杂概念",
    question="什么是递归？"
)

response = model.invoke(messages)
```

**示例 2：多轮对话**

```python
conversation_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}"),
    ("user", "{question1}"),
    ("assistant", "{answer1}"),
    ("user", "{question2}")
])

messages = conversation_template.format_messages(
    role="Python 专家",
    question1="什么是列表？",
    answer1="列表是 Python 的有序可变集合。",
    question2="它和元组有什么区别？"  # 基于上下文
)
```

**示例 3：结构化指令**

```python
structured_template = ChatPromptTemplate.from_messages([
    ("system",
     "你是一个{domain}专家。\n"
     "回答风格：{style}\n"
     "回答长度：{length}字以内"),
    ("user", "{question}")
])

messages = structured_template.format_messages(
    domain="机器学习",
    style="技术性强、简洁",
    length="100",
    question="什么是梯度下降？"
)
```

---

### 4. 高级特性

#### 4.1 部分变量（Partial Variables）

预填充某些固定不变的变量，创建模板的变体。

**使用场景：**
- 某些变量在所有调用中都相同
- 需要为不同用户/场景创建定制模板

**语法：**

```python
# 原始模板
template = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，目标用户是{audience}"),
    ("user", "{task}")
])

# 部分填充
customer_support_template = template.partial(
    role="客服专员",
    audience="普通用户"
)

# 现在只需要提供 task
messages = customer_support_template.format_messages(
    task="解释退款政策"
)
```

**实用示例：**

```python
# 基础翻译模板
translator = ChatPromptTemplate.from_messages([
    ("system", "你是专业翻译，精通{source}和{target}"),
    ("user", "翻译：{text}")
])

# 创建英译中的专用模板
en_to_zh = translator.partial(source="英语", target="中文")

# 创建中译英的专用模板
zh_to_en = translator.partial(source="中文", target="英语")

# 使用
messages1 = en_to_zh.format_messages(text="Hello")
messages2 = zh_to_en.format_messages(text="你好")
```

#### 4.2 模板组合

将多个模板片段组合成复杂的提示词。

**方法 1：字符串组合**

```python
# 定义可复用的部分
role_part = "你是一个{domain}专家。"
style_part = "回答风格：{style}。"
constraint_part = "限制：{constraint}。"

# 组合
full_system = role_part + style_part + constraint_part

template = ChatPromptTemplate.from_messages([
    ("system", full_system),
    ("user", "{question}")
])
```

**方法 2：使用 + 运算符**

```python
template1 = ChatPromptTemplate.from_messages([
    ("system", "你是助手")
])

template2 = ChatPromptTemplate.from_messages([
    ("user", "{input}")
])

# 组合（LangChain 1.0 支持）
combined = template1 + template2
```

#### 4.3 可复用模板库

在实际项目中，建议创建模板库。

**示例：模板库**

```python
# templates.py
from langchain_core.prompts import ChatPromptTemplate

class PromptLibrary:
    """可复用的提示词模板库"""

    TRANSLATOR = ChatPromptTemplate.from_messages([
        ("system", "你是专业翻译，精通{source_lang}和{target_lang}"),
        ("user", "翻译以下文本：\n{text}")
    ])

    CODE_REVIEWER = ChatPromptTemplate.from_messages([
        ("system", "你是{language}代码审查专家，重点关注{focus}"),
        ("user", "审查代码：\n```{language}\n{code}\n```")
    ])

    SUMMARIZER = ChatPromptTemplate.from_messages([
        ("system", "你是内容摘要专家"),
        ("user", "将以下内容总结为{num}个要点：\n{content}")
    ])

    TUTOR = ChatPromptTemplate.from_messages([
        ("system", "你是{subject}导师，学生水平：{level}"),
        ("user", "{question}")
    ])

# 使用
from templates import PromptLibrary

messages = PromptLibrary.TRANSLATOR.format_messages(
    source_lang="英语",
    target_lang="中文",
    text="Hello World"
)
```

---

### 5. LCEL 链式调用（预览）

**LCEL** = LangChain Expression Language，LangChain 的表达式语言。

#### 什么是链（Chain）？

链是将多个组件连接在一起的方式，形成处理流程。

```
输入 → 模板 → 模型 → 输出
```

#### 使用管道运算符 `|`

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

# 创建组件
template = ChatPromptTemplate.from_messages([
    ("system", "你是{role}"),
    ("user", "{input}")
])

model = init_chat_model("groq:llama-3.3-70b-versatile")

# 使用 | 创建链
chain = template | model

# 直接调用链
response = chain.invoke({
    "role": "Python 导师",
    "input": "什么是装饰器？"
})
