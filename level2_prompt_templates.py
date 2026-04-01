"""
Level 2 — Prompt Templates
----------------------------
Goal: Use dynamic prompts with {{$variable}} placeholders.
Concepts: Prompt templates, KernelArguments

Run:
    python level2_prompt_templates.py
"""

import asyncio
import os

from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelArguments

load_dotenv()


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


async def explain_topic(kernel: Kernel, topic: str, audience: str) -> str:
    """Explain any topic for any audience using a reusable template."""
    prompt = "Explain {{$topic}} in simple terms for a {{$audience}}."
    result = await kernel.invoke_prompt(
        prompt,
        arguments=KernelArguments(topic=topic, audience=audience),
    )
    return str(result)


async def main():
    print("=" * 50)
    print("  Level 2 — Prompt Templates")
    print("=" * 50)

    kernel = build_kernel()

    examples = [
        ("quantum computing", "10-year-old"),
        ("machine learning", "retired teacher"),
        ("blockchain", "small business owner"),
    ]

    for topic, audience in examples:
        print(f"\nTopic : {topic}")
        print(f"Audience: {audience}")
        print("Response:")
        response = await explain_topic(kernel, topic, audience)
        print(f"  {response}\n")
        print("-" * 50)


if __name__ == "__main__":
    asyncio.run(main())
