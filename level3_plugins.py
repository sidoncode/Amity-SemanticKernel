"""
Level 3 — Plugins
------------------
Goal: Package AI functions as reusable plugins.
Concepts: Plugin class, @kernel_function, kernel.add_plugin(), kernel.invoke()

Run:
    python level3_plugins.py
"""

import asyncio
import os

from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelArguments, kernel_function

load_dotenv()


# ---------------------------------------------------------------------------
# Plugin definition
# ---------------------------------------------------------------------------

class WritingPlugin:
    """A plugin with reusable text-transformation functions."""

    @kernel_function(description="Summarize a given text in 2 sentences")
    async def summarize(self, kernel: Kernel, text: str) -> str:
        result = await kernel.invoke_prompt(
            f"Summarize the following in exactly 2 sentences:\n\n{text}"
        )
        return str(result)

    @kernel_function(description="Rewrite text in a professional, formal tone")
    async def make_formal(self, kernel: Kernel, text: str) -> str:
        result = await kernel.invoke_prompt(
            f"Rewrite this text in a professional, formal tone:\n\n{text}"
        )
        return str(result)

    @kernel_function(description="Translate text to the specified language")
    async def translate(self, kernel: Kernel, text: str, language: str) -> str:
        result = await kernel.invoke_prompt(
            f"Translate the following text to {language}. "
            f"Return only the translation, nothing else:\n\n{text}"
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


async def main():
    print("=" * 50)
    print("  Level 3 — Plugins")
    print("=" * 50)

    kernel = build_kernel()
    kernel.add_plugin(WritingPlugin(), plugin_name="writing")

    sample = (
        "hey so i was thinking maybe we should do the meeting on friday? "
        "idk if everyone is free but we gotta talk about the project stuff asap"
    )

    print(f"\nOriginal:\n  {sample}\n")
    print("-" * 50)

    summary = await kernel.invoke(
        "writing", "summarize", arguments=KernelArguments(text=sample)
    )
    print(f"\nSummary:\n  {summary}")

    formal = await kernel.invoke(
        "writing", "make_formal", arguments=KernelArguments(text=sample)
    )
    print(f"\nFormal version:\n  {formal}")

    translated = await kernel.invoke(
        "writing",
        "translate",
        arguments=KernelArguments(text=sample, language="Spanish"),
    )
    print(f"\nSpanish translation:\n  {translated}\n")


if __name__ == "__main__":
    asyncio.run(main())
