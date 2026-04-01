"""
Level 4 — Chaining & Pipelines
--------------------------------
Goal: Run AI functions in sequence — output of one feeds the next.
Concepts: Multi-step pipelines, function chaining, output as input

Pipeline:
    topic → draft_post → add_title
                      → write_tweet
                      → write_linkedin

Run:
    python level4_pipelines.py
"""

import asyncio
import os

from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelArguments, kernel_function

load_dotenv()


# ---------------------------------------------------------------------------
# Plugin
# ---------------------------------------------------------------------------

class ContentPlugin:
    """A content-generation pipeline: draft → title + social posts."""

    @kernel_function(description="Write a short blog post draft about a topic")
    async def draft_post(self, kernel: Kernel, topic: str) -> str:
        result = await kernel.invoke_prompt(
            f"Write a short, engaging 3-paragraph blog post about: {topic}"
        )
        return str(result)

    @kernel_function(description="Generate a catchy title for a blog post")
    async def add_title(self, kernel: Kernel, content: str) -> str:
        result = await kernel.invoke_prompt(
            f"Write a single catchy blog title for this article. "
            f"Return only the title, no quotes, no explanation:\n\n{content}"
        )
        return str(result)

    @kernel_function(description="Write a tweet promoting the blog post")
    async def write_tweet(self, kernel: Kernel, content: str) -> str:
        result = await kernel.invoke_prompt(
            f"Write a Twitter/X post promoting this blog article. "
            f"Max 280 characters. Include 2–3 relevant hashtags:\n\n{content}"
        )
        return str(result)

    @kernel_function(description="Write a LinkedIn post promoting the blog post")
    async def write_linkedin(self, kernel: Kernel, content: str) -> str:
        result = await kernel.invoke_prompt(
            f"Write a short professional LinkedIn post (3–4 sentences) "
            f"promoting this blog article:\n\n{content}"
        )
        return str(result)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_kernel() -> Kernel:
    kernel = Kernel()
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    )
    return kernel


async def run_content_pipeline(kernel: Kernel, topic: str) -> dict:
    """Run the full content pipeline and return all outputs."""

    print(f"  [1/4] Drafting blog post about: '{topic}' ...")
    draft = await kernel.invoke(
        "content", "draft_post", arguments=KernelArguments(topic=topic)
    )

    print("  [2/4] Generating title ...")
    title = await kernel.invoke(
        "content", "add_title", arguments=KernelArguments(content=str(draft))
    )

    print("  [3/4] Writing tweet ...")
    tweet = await kernel.invoke(
        "content", "write_tweet", arguments=KernelArguments(content=str(draft))
    )

    print("  [4/4] Writing LinkedIn post ...")
    linkedin = await kernel.invoke(
        "content", "write_linkedin", arguments=KernelArguments(content=str(draft))
    )

    return {
        "title": str(title),
        "draft": str(draft),
        "tweet": str(tweet),
        "linkedin": str(linkedin),
    }


async def main():
    print("=" * 50)
    print("  Level 4 — Chaining & Pipelines")
    print("=" * 50)

    kernel = build_kernel()
    kernel.add_plugin(ContentPlugin(), plugin_name="content")

    topic = "Why Python is the best language for beginners"

    print(f"\nRunning content pipeline...\n")
    results = await run_content_pipeline(kernel, topic)

    print("\n" + "=" * 50)
    print(f"📰 TITLE\n{results['title']}")
    print(f"\n📝 BLOG DRAFT\n{results['draft']}")
    print(f"\n🐦 TWEET\n{results['tweet']}")
    print(f"\n💼 LINKEDIN\n{results['linkedin']}\n")


if __name__ == "__main__":
    asyncio.run(main())
