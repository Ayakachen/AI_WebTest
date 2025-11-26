import asyncio

# from langchain_openai import ChatOpenAI
from browser_use import ChatGoogle
from browser_use import Agent
from pydantic import BaseModel

llm = ChatGoogle(
    # base_url= "https://generativelanguage.googleapis.com/v1beta/",
    model="gemini-2.5-flash",
    api_key="your key",
)
extend_system_message = """
    1、执行搜索任务时，优先打开 https://gushitong.baidu.com/ 进行搜索。
    2、查看概览的“五日”股票趋势图，获取趋势图上每一个时间点的所有取值
    3、总结每日的开盘价、收盘价、最高价、最低价、涨跌幅。
	4、最后的输出结果，要用中文和表格格式输出结果。
	"""


class Post(BaseModel):
    post_title: str
    post_url: str
    num_comments: int
    hours_since_post: int


class Posts(BaseModel):
    posts: list[Post]


async def main():
    task_baidu = "搜索深信服的股票情况"
    agent = Agent(
        task=task_baidu,
        llm=llm,
        extend_system_message=extend_system_message,
        # output_model_schema=Posts,
    )
    history = await agent.run()
    result = history.final_result()
    if result:
        # parsed: Posts = Posts.model_validate_json(result)
        # for post in parsed.posts:
        #     print("\n--------------------------------")
        #     print(f"Title:            {post.post_title}")
        #     print(f"URL:              {post.post_url}")
        #     print(f"Comments:         {post.num_comments}")
        #     print(f"Hours since post: {post.hours_since_post}")
        print(result)
    else:
        print("No result")


asyncio.run(main())
