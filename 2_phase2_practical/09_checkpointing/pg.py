import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()

model = init_chat_model("groq:llama-3.3-70b-versatile")

# 直接使用连接字符串
conn_string = os.getenv("POSTGRES_URI", "postgresql://postgres:4869@localhost:5432/langgraph")
def main():
    with PostgresSaver.from_conn_string(
        "postgresql://postgres:4869@localhost:5432/langgraph"
    ) as checkpointer:

        checkpointer.setup()  # ✅ 现在可以用了

        agent = create_agent(
            model=model,
            tools=[],
            system_prompt="你是一个有帮助的助手。",
            checkpointer=checkpointer
        )

        config = {"configurable": {"thread_id": "postgres_user_001"}}

        print("用户: 我叫王五")
        agent.invoke(
            {"messages": [{"role": "user", "content": "我叫王五"}]},
            config=config
        )

        print("用户: 我叫什么？")
        response = agent.invoke(
            {"messages": [{"role": "user", "content": "我叫什么？"}]},
            config=config
        )

        print(f"Agent: {response['messages'][-1].content}")

if __name__ == "__main__":
    main()