# 🧠 Semantic Kernel — Step-by-Step Tutorial

> A beginner-to-intermediate guide to building AI-powered apps with Microsoft's Semantic Kernel SDK.


```

Option A — OpenAI (recommended for beginners)

1. Go to platform.openai.com/signup and create a free account.
2. Click your profile icon → API Keys → Create new secret key.
3. Copy the key (starts with sk-...). You only see it once — save it.
4. Add a small credit balance under Billing (even $5 covers hundreds of test calls).


```
---

## 📋 Table of Contents

- [What is Semantic Kernel?](#what-is-semantic-kernel)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Level 1 — Hello AI (Beginner)](#level-1--hello-ai-beginner)
- [Level 2 — Prompts & Templates (Beginner)](#level-2--prompts--templates-beginner)
- [Level 3 — Plugins (Beginner → Intermediate)](#level-3--plugins-beginner--intermediate)
- [Level 4 — Chaining & Pipelines (Intermediate)](#level-4--chaining--pipelines-intermediate)
- [Level 5 — Memory & Context (Intermediate)](#level-5--memory--context-intermediate)
- [Cheat Sheet](#cheat-sheet)
- [Next Steps](#next-steps)

---

## What is Semantic Kernel?

**Semantic Kernel (SK)** is an open-source SDK by Microsoft that lets you integrate Large Language Models (LLMs) like OpenAI's GPT or Azure OpenAI into your apps — using **C#**, **Python**, or **Java**.

Think of it as a **bridge between your code and AI**, giving you structure to:

- Send prompts to AI models
- Create reusable AI functions ("plugins")
- Build multi-step AI pipelines
- Give AI memory and context

```
Your App  →  Semantic Kernel  →  LLM (OpenAI / Azure / Hugging Face)
```

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Language | Python 3.10+ (this tutorial uses Python) |
| API Key | OpenAI API key — get one at [platform.openai.com](https://platform.openai.com) |
| Package manager | `pip` |
| IDE | VS Code recommended |

---

## Setup

### 1. Install the SDK

```bash
pip install semantic-kernel
```

### 2. Set your API key

Create a `.env` file in your project root:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

### 3. Install dotenv (to load your `.env`)

```bash
pip install python-dotenv
```

---

## Level 1 — Hello AI (Beginner)

> **Goal:** Connect to an LLM and get your first response.

### Concepts
- `Kernel` — the central object in Semantic Kernel
- `ChatCompletion` service — the AI brain you plug in

### Code

```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    # 1. Create the kernel
    kernel = Kernel()

    # 2. Add an AI service
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id=os.getenv("OPENAI_MODEL"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    )

    # 3. Ask a question
    result = await kernel.invoke_prompt("What is Semantic Kernel in one sentence?")
    print(result)

asyncio.run(main())
```

### Expected Output
```
Semantic Kernel is an open-source SDK that enables developers to integrate 
large language models into their applications.
```

### 💡 What just happened?
1. You created a `Kernel` (the engine)
2. Registered an OpenAI chat service
3. Sent a plain string prompt and got a response back

---

## Level 2 — Prompts & Templates (Beginner)

> **Goal:** Use dynamic prompt templates with variables.

### Concepts
- **Prompt templates** — reusable prompts with `{{$variable}}` placeholders
- **KernelArguments** — the way you pass values into templates

### Code

```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelArguments
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    kernel = Kernel()
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id=os.getenv("OPENAI_MODEL"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    )

    # Prompt template with a variable
    prompt = "Explain {{$topic}} in simple terms for a 10-year-old."

    # Pass variable values using KernelArguments
    result = await kernel.invoke_prompt(
        prompt,
        arguments=KernelArguments(topic="quantum computing")
    )
    print(result)

asyncio.run(main())
```

### Try changing the topic
```python
KernelArguments(topic="machine learning")
KernelArguments(topic="blockchain")
KernelArguments(topic="the stock market")
```

### 💡 What just happened?
- `{{$topic}}` is a placeholder — SK fills it in before sending to the LLM
- `KernelArguments` is a dict-like object for passing values

---

## Level 3 — Plugins (Beginner → Intermediate)

> **Goal:** Package AI functions as reusable **plugins**.

### Concepts
- **Plugin** — a class that groups related AI functions
- **`@kernel_function`** — decorator that registers a method as an AI function
- **Invoke by name** — call plugins like regular functions

### Code

```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function, KernelArguments
from dotenv import load_dotenv
import os

load_dotenv()

# --- Define a Plugin ---
class WritingPlugin:

    @kernel_function(description="Summarize a given text")
    async def summarize(self, kernel: Kernel, text: str) -> str:
        prompt = f"Summarize the following in 2 sentences:\n\n{text}"
        result = await kernel.invoke_prompt(prompt)
        return str(result)

    @kernel_function(description="Make text more formal")
    async def make_formal(self, kernel: Kernel, text: str) -> str:
        prompt = f"Rewrite this text in a professional, formal tone:\n\n{text}"
        result = await kernel.invoke_prompt(prompt)
        return str(result)


async def main():
    kernel = Kernel()
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id=os.getenv("OPENAI_MODEL"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    )

    # Register the plugin
    kernel.add_plugin(WritingPlugin(), plugin_name="writing")

    sample_text = """
    hey so i was thinking maybe we should like do the meeting on friday? 
    idk if everyone is free but we gotta talk about the project stuff
    """

    # Call plugin functions
    summary = await kernel.invoke(
        plugin_name="writing",
        function_name="summarize",
        arguments=KernelArguments(text=sample_text)
    )

    formal = await kernel.invoke(
        plugin_name="writing",
        function_name="make_formal",
        arguments=KernelArguments(text=sample_text)
    )

    print("=== Summary ===")
    print(summary)

    print("\n=== Formal Version ===")
    print(formal)

asyncio.run(main())
```

### 💡 What just happened?
- `WritingPlugin` groups two related AI functions
- `@kernel_function` tells SK "this is an AI-callable function"
- You invoke by **plugin name + function name** — clean, reusable, organized

---

## Level 4 — Chaining & Pipelines (Intermediate)

> **Goal:** Run multiple AI functions in sequence — output of one feeds the next.

### Concepts
- **Function chaining** — run functions one after another
- **Pipelines** — structured multi-step AI workflows
- Output from Step 1 becomes input for Step 2

### Code

```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function, KernelArguments
from dotenv import load_dotenv
import os

load_dotenv()

class ContentPlugin:

    @kernel_function(description="Generate a blog post draft on a topic")
    async def draft_post(self, kernel: Kernel, topic: str) -> str:
        prompt = f"Write a short 3-paragraph blog post about: {topic}"
        result = await kernel.invoke_prompt(prompt)
        return str(result)

    @kernel_function(description="Add an engaging title to content")
    async def add_title(self, kernel: Kernel, content: str) -> str:
        prompt = f"Write a catchy blog title for this content:\n\n{content}\n\nTitle only, no explanation."
        result = await kernel.invoke_prompt(prompt)
        return str(result)

    @kernel_function(description="Write a tweet promoting the blog post")
    async def write_tweet(self, kernel: Kernel, content: str) -> str:
        prompt = f"Write a Twitter/X post promoting this blog article (max 280 chars, include relevant hashtags):\n\n{content}"
        result = await kernel.invoke_prompt(prompt)
        return str(result)


async def main():
    kernel = Kernel()
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id=os.getenv("OPENAI_MODEL"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    )
    kernel.add_plugin(ContentPlugin(), plugin_name="content")

    topic = "Why Python is great for beginners"

    # Step 1: Draft the post
    print("✍️  Drafting blog post...")
    draft = await kernel.invoke("content", "draft_post", arguments=KernelArguments(topic=topic))

    # Step 2: Generate a title from the draft
    print("🏷️  Generating title...")
    title = await kernel.invoke("content", "add_title", arguments=KernelArguments(content=str(draft)))

    # Step 3: Write a tweet from the draft
    print("🐦  Writing tweet...")
    tweet = await kernel.invoke("content", "write_tweet", arguments=KernelArguments(content=str(draft)))

    print(f"\n📰 Title: {title}")
    print(f"\n📝 Draft:\n{draft}")
    print(f"\n🐦 Tweet:\n{tweet}")

asyncio.run(main())
```

### Pipeline Flow
```
topic  →  [draft_post]  →  draft
                        →  [add_title]  →  title
                        →  [write_tweet]  →  tweet
```

### 💡 What just happened?
- Each function call uses the **output of the previous** as input
- This is the heart of building AI workflows — composable, modular, testable

---

## Level 5 — Memory & Context (Intermediate)

> **Goal:** Give the AI a "memory" so it can hold a multi-turn conversation.

### Concepts
- **`ChatHistory`** — stores the conversation (user + assistant turns)
- **Stateful conversations** — AI remembers what was said earlier
- Without this, every call to the LLM is independent (it forgets everything)

### Code

```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    kernel = Kernel()

    chat_service = OpenAIChatCompletion(
        service_id="chat",
        ai_model_id=os.getenv("OPENAI_MODEL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    kernel.add_service(chat_service)

    # Initialize chat history with a system message (sets AI personality)
    history = ChatHistory()
    history.add_system_message(
        "You are a friendly Python tutor. Keep answers short and encouraging."
    )

    print("🤖 Python Tutor ready! Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break

        # Add user message to history
        history.add_user_message(user_input)

        # Get AI response (with full history for context)
        settings = OpenAIChatPromptExecutionSettings(max_tokens=300)
        response = await chat_service.get_chat_message_content(
            chat_history=history,
            settings=settings,
            kernel=kernel,
        )

        # Add AI response to history (so next turn has context)
        history.add_assistant_message(str(response))

        print(f"\n🤖 Tutor: {response}\n")

asyncio.run(main())
```

### Example Conversation
```
You: What is a list in Python?
🤖 Tutor: A list is an ordered collection of items, like a shopping list!
          Example: fruits = ["apple", "banana", "cherry"]

You: How do I add something to it?
🤖 Tutor: Great question! Use .append() — for example: fruits.append("mango")
          The AI remembered you asked about lists! ✅
```

### 💡 What just happened?
- `ChatHistory` stores every message (user + assistant)
- Each new request includes the **full history** — the LLM can now "remember"
- The system message sets the AI's persona and behavior

---

## Cheat Sheet

```python
# Create kernel
kernel = Kernel()

# Add OpenAI service
kernel.add_service(OpenAIChatCompletion(service_id="chat", ...))

# Simple prompt
result = await kernel.invoke_prompt("Your prompt here")

# Prompt with variables
result = await kernel.invoke_prompt("Tell me about {{$topic}}", 
    arguments=KernelArguments(topic="space"))

# Register a plugin
kernel.add_plugin(MyPlugin(), plugin_name="my_plugin")

# Call a plugin function
result = await kernel.invoke("my_plugin", "function_name", 
    arguments=KernelArguments(param="value"))

# Chat with memory
history = ChatHistory()
history.add_system_message("You are a helpful assistant.")
history.add_user_message("Hello!")
response = await chat_service.get_chat_message_content(history, settings, kernel)
history.add_assistant_message(str(response))
```

---

## Project Structure

```
my-sk-project/
├── .env                  # API keys (never commit this!)
├── .gitignore
├── main.py               # Entry point
├── plugins/
│   ├── writing_plugin.py
│   └── content_plugin.py
└── requirements.txt
```

**requirements.txt**
```
semantic-kernel
python-dotenv
```

---

## Next Steps

Once you're comfortable with these levels, explore:

| Topic | What You'll Learn |
|-------|-------------------|
| 🔌 **Native Functions** | Mix Python logic with AI functions in the same plugin |
| 📂 **File-based Plugins** | Store prompts in `.txt`/`.yaml` files instead of code |
| 🧠 **Vector Memory** | Store and search documents with embeddings |
| 🤖 **Auto Function Calling** | Let the AI decide which plugins to use automatically |
| ☁️ **Azure OpenAI** | Swap OpenAI for enterprise-grade Azure deployment |

### Useful Links

- 📖 [Official Docs](https://learn.microsoft.com/en-us/semantic-kernel/overview/)
- 💻 [GitHub Repo](https://github.com/microsoft/semantic-kernel)
- 🧪 [Python Samples](https://github.com/microsoft/semantic-kernel/tree/main/python/samples)
- 💬 [Discord Community](https://aka.ms/SKDiscord)

---

> Made with ❤️ for the SK community. Star ⭐ the repo if this helped you!
