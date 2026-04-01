"""
Level 5 — Memory & Conversation
---------------------------------
Goal: Build a stateful multi-turn chatbot using ChatHistory.
Concepts: ChatHistory, system messages, multi-turn context

The AI remembers everything said in the session.
Type 'quit' or 'exit' to end the conversation.
Type 'history' to print the full conversation log.
Type 'reset' to start a fresh conversation.

Run:
    python level5_memory.py
"""

import asyncio
import os

from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.contents import ChatHistory

load_dotenv()


SYSTEM_PROMPT = """
You are a friendly and encouraging Python tutor named Py.
- Keep answers concise and beginner-friendly.
- Use short code examples when helpful.
- If the user seems confused, offer to explain differently.
- Always be positive and patient.
"""


def build_kernel_and_service():
    kernel = Kernel()
    service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    kernel.add_service(service)
    return kernel, service


def create_history() -> ChatHistory:
    history = ChatHistory()
    history.add_system_message(SYSTEM_PROMPT)
    return history


def print_history(history: ChatHistory):
    print("\n--- Conversation History ---")
    for msg in history.messages:
        role = msg.role.value if hasattr(msg.role, "value") else str(msg.role)
        if role == "system":
            continue
        label = "You  " if role == "user" else "Py   "
        print(f"  {label}: {msg.content}")
    print("----------------------------\n")


async def chat(kernel, service, history: ChatHistory, user_input: str) -> str:
    history.add_user_message(user_input)

    settings = OpenAIChatPromptExecutionSettings(max_tokens=400)
    response = await service.get_chat_message_content(
        chat_history=history,
        settings=settings,
        kernel=kernel,
    )

    history.add_assistant_message(str(response))
    return str(response)


async def main():
    print("=" * 50)
    print("  Level 5 — Memory & Conversation")
    print("=" * 50)
    print("\n  Commands: 'quit' · 'history' · 'reset'\n")

    kernel, service = build_kernel_and_service()
    history = create_history()

    print("🐍 Py: Hi! I'm Py, your Python tutor. What would you like to learn today?\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("\n🐍 Py: Great session! Keep coding! 👋\n")
            break

        if user_input.lower() == "history":
            print_history(history)
            continue

        if user_input.lower() == "reset":
            history = create_history()
            print("\n🐍 Py: Fresh start! What would you like to learn?\n")
            continue

        response = await chat(kernel, service, history, user_input)
        print(f"\n🐍 Py: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())
