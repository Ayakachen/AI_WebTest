import asyncio
# from langchain_openai import ChatOpenAI
from browser_use import ChatGoogle
from browser_use import Agent
llm = ChatGoogle(
    # base_url= "https://generativelanguage.googleapis.com/v1beta/",
    model="gemini-2.5-flash",
    api_key= "AIzaSyCQswJ8iMgcS4xcPSeSWzEHA7jRZ-wMD0Y"
)
extend_system_message = """
记住最重要的规则:
1、执行搜索任务时，优先打开 https://www.bing.com/?mkt=zh-CN 进行搜索。
2、最后的输出结果，要用中文回答用户的问题。
"""
async def main():
    task_baidu = "Search for today's weather"
    agent = Agent(task=task_baidu, llm=llm, message_context=extend_system_message)
    result = await agent.run()
    print(result)
asyncio.run(main())
