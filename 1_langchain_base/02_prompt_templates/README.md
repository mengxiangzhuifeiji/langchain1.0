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
