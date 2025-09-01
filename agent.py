import asyncio

# from langchain_openai import ChatOpenAI
from browser_use import ChatGoogle
from browser_use import Agent
from pydantic import BaseModel

llm = ChatGoogle(
    # base_url= "https://generativelanguage.googleapis.com/v1beta/",
    model="gemini-2.5-flash",
    api_key="AIzaSyCQswJ8iMgcS4xcPSeSWzEHA7jRZ-wMD0Y",
)
extend_system_message = """
    1、执行搜索任务时，优先打开 https://www.baidu.com/ 进行搜索。
	2、最后的输出结果，要用中文输出结果。
	"""


class Post(BaseModel):
    post_title: str
    post_url: str
    num_comments: int
    hours_since_post: int


class Posts(BaseModel):
    posts: list[Post]


async def main():
    task_baidu = "搜索今天的天气"
    agent = Agent(
        task=task_baidu,
        llm=llm,
        extend_system_message=extend_system_message,
        output_model_schema=Posts,
    )
    history = await agent.run()
    result = history.final_result()
    if result:
        parsed: Posts = Posts.model_validate_json(result)
        for post in parsed.posts:
            print("\n--------------------------------")
            print(f"Title:            {post.post_title}")
            print(f"URL:              {post.post_url}")
            print(f"Comments:         {post.num_comments}")
            print(f"Hours since post: {post.hours_since_post}")
    else:
        print("No result")


asyncio.run(main())
