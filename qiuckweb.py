import gradio as gr
import json
from datetime import datetime
import os


class BlogApp:
    def __init__(self):
        self.posts_file = "blog_posts.json"
        self.posts = self.load_posts()
        self.setup_ui()

    def load_posts(self):
        """加载博客文章数据"""
        if os.path.exists(self.posts_file):
            try:
                with open(self.posts_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return self.get_default_posts()
        else:
            return self.get_default_posts()

    def save_posts(self):
        """保存博客文章数据"""
        with open(self.posts_file, "w", encoding="utf-8") as f:
            json.dump(self.posts, f, ensure_ascii=False, indent=2)

    def get_default_posts(self):
        """获取默认的博客文章"""
        return [
            {
                "id": 1,
                "title": "欢迎使用Gradio博客",
                "content": "这是一个使用Gradio库创建的简单博客应用。Gradio是一个用于构建机器学习模型界面的Python库，但它也可以用来创建各种web应用。\n\n在这个博客中，你可以：\n- 查看文章列表\n- 阅读文章详情\n- 搜索文章\n- 添加新文章\n\n希望你喜欢这个简单的博客应用！",
                "author": "管理员",
                "date": "2025-01-05",
                "category": "技术",
            },
            {
                "id": 2,
                "title": "Python编程入门",
                "content": "Python是一种高级编程语言，以其简洁的语法和强大的功能而闻名。\n\nPython的主要特点：\n1. 语法简洁易读\n2. 丰富的标准库\n3. 跨平台兼容性\n4. 强大的社区支持\n\n学习Python的建议：\n- 从基础语法开始\n- 多做练习项目\n- 参与开源项目\n- 阅读优秀代码",
                "author": "Python爱好者",
                "date": "2025-01-04",
                "category": "编程",
            },
            {
                "id": 3,
                "title": "Web开发最佳实践",
                "content": "现代Web开发涉及许多技术和最佳实践。\n\n前端开发：\n- 使用现代框架（React, Vue, Angular）\n- 响应式设计\n- 性能优化\n- 用户体验设计\n\n后端开发：\n- RESTful API设计\n- 数据库优化\n- 安全性考虑\n- 可扩展性架构\n\n全栈开发需要综合考虑前后端的协调工作。",
                "author": "Web开发者",
                "date": "2025-01-03",
                "category": "Web开发",
            },
        ]

    def get_post_list(self):
        """获取文章列表"""
        post_list = []
        for post in self.posts:
            post_list.append(
                f"**{post['title']}**\n作者：{post['author']} | 日期：{post['date']} | 分类：{post['category']}"
            )
        return "\n\n---\n\n".join(post_list)

    def get_post_content(self, post_index):
        """获取文章内容"""
        if 0 <= post_index < len(self.posts):
            post = self.posts[post_index]
            return f"# {post['title']}\n\n**作者：** {post['author']}  \n**日期：** {post['date']}  \n**分类：** {post['category']}\n\n---\n\n{post['content']}"
        return "请选择一篇文章"

    def search_posts(self, query):
        """搜索文章"""
        if not query:
            return self.get_post_list()

        results = []
        for post in self.posts:
            if (
                query.lower() in post["title"].lower()
                or query.lower() in post["content"].lower()
                or query.lower() in post["category"].lower()
            ):
                results.append(
                    f"**{post['title']}**\n作者：{post['author']} | 日期：{post['date']} | 分类：{post['category']}"
                )

        if results:
            return "\n\n---\n\n".join(results)
        else:
            return f"没有找到包含 '{query}' 的文章"

    def add_post(self, title, content, author, category):
        """添加新文章"""
        if not title or not content or not author:
            return "请填写标题、内容和作者"

        new_post = {
            "id": len(self.posts) + 1,
            "title": title,
            "content": content,
            "author": author,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "category": category or "未分类",
        }

        self.posts.insert(0, new_post)  # 添加到开头
        self.save_posts()

        return f"文章 '{title}' 已成功添加！"

    def setup_ui(self):
        """设置用户界面"""
        with gr.Blocks(title="Gradio博客", theme=gr.themes.Soft()) as self.app:
            gr.Markdown("# 📝 Gradio博客应用")
            gr.Markdown("一个简单而优雅的博客系统")

            with gr.Tabs():
                # 文章列表标签页
                with gr.TabItem("📚 文章列表"):
                    with gr.Row():
                        with gr.Column(scale=2):
                            search_input = gr.Textbox(
                                label="🔍 搜索文章",
                                placeholder="输入关键词搜索文章标题、内容或分类...",
                                lines=1,
                            )
                            search_btn = gr.Button("搜索", variant="primary")

                        with gr.Column(scale=1):
                            refresh_btn = gr.Button("🔄 刷新列表")

                    post_list_output = gr.Markdown(
                        label="文章列表", value=self.get_post_list()
                    )

                # 文章详情标签页
                with gr.TabItem("📖 文章详情"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            post_selector = gr.Dropdown(
                                label="选择文章",
                                choices=[
                                    f"{post['title']} - {post['author']}"
                                    for post in self.posts
                                ],
                                value=None,
                            )
                            view_btn = gr.Button("查看文章", variant="primary")

                        with gr.Column(scale=2):
                            post_content_output = gr.Markdown(
                                label="文章内容", value="请从左侧选择一篇文章"
                            )

                # 添加文章标签页
                with gr.TabItem("✍️ 添加文章"):
                    with gr.Column():
                        gr.Markdown("### 发布新文章")

                        title_input = gr.Textbox(
                            label="文章标题", placeholder="请输入文章标题...", lines=1
                        )

                        author_input = gr.Textbox(
                            label="作者", placeholder="请输入作者名称...", lines=1
                        )

                        category_input = gr.Textbox(
                            label="分类", placeholder="请输入文章分类...", lines=1
                        )

                        content_input = gr.Textbox(
                            label="文章内容", placeholder="请输入文章内容...", lines=10
                        )

                        add_btn = gr.Button("📝 发布文章", variant="primary")
                        add_output = gr.Textbox(label="发布结果", interactive=False)

            # 事件绑定
            search_btn.click(
                fn=self.search_posts, inputs=search_input, outputs=post_list_output
            )

            search_input.submit(
                fn=self.search_posts, inputs=search_input, outputs=post_list_output
            )

            refresh_btn.click(fn=self.get_post_list, outputs=post_list_output)

            view_btn.click(
                fn=lambda x: self.get_post_content(
                    self.posts.index(
                        next(
                            p
                            for p in self.posts
                            if f"{p['title']} - {p['author']}" == x
                        )
                    )
                ),
                inputs=post_selector,
                outputs=post_content_output,
            )

            add_btn.click(
                fn=self.add_post,
                inputs=[title_input, content_input, author_input, category_input],
                outputs=add_output,
            ).then(
                fn=lambda: gr.update(
                    choices=[
                        f"{post['title']} - {post['author']}" for post in self.posts
                    ]
                ),
                outputs=post_selector,
            ).then(
                fn=self.get_post_list, outputs=post_list_output
            )

            # 清空输入框
            add_btn.click(
                fn=lambda: [
                    gr.update(value=""),
                    gr.update(value=""),
                    gr.update(value=""),
                    gr.update(value=""),
                ],
                inputs=[],
                outputs=[title_input, content_input, author_input, category_input],
            )

    def launch(self):
        """启动应用"""
        self.app.launch()


if __name__ == "__main__":
    blog_app = BlogApp()
    blog_app.launch()
