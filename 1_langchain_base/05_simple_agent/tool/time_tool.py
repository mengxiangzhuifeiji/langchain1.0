import datetime

from langchain_core.tools import tool


@tool
def time_tool() -> str:
    """
    获取当前时间

    返回:
        时间字符串
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
