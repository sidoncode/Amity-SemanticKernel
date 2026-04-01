"""
Level 1 — Hello AI
-------------------
Goal: Connect to OpenAI and get your first AI response.
Concepts: Kernel, OpenAIChatCompletion, invoke_prompt()

Run:
    python level1_hello_ai.py
"""

import asyncio
import os

from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

load_dotenv()


def build_kernel() -> Kernel:
    """Create a Kernel and attach the OpenAI chat service."""
    kernel = Kernel()
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    )
    return kernel


async def main():
    print("=" * 50)
    print("  Level 1 — Hello AI")
    print("=" * 50)

    kernel = build_kernel()

    print("\nSending prompt to OpenAI...\n")
    result = await kernel.invoke_prompt(
        "What is Semantic Kernel in one sentence?"
    )

    print(f"Response:\n  {result}\n")


if __name__ == "__main__":
    asyncio.run(main())
