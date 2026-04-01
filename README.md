# Semantic Kernel — Python Tutorial Project

A working Python project covering all 5 levels of the Semantic Kernel tutorial.

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy the example env file and add your API key
cp .env.example .env
# Edit .env and replace sk-your-key-here with your real key
```

Get your API key at → https://platform.openai.com/api-keys

## Run

| File | Level | Description |
|------|-------|-------------|
| `level1_hello_ai.py` | Beginner | First AI response |
| `level2_prompt_templates.py` | Beginner | Dynamic prompt templates |
| `level3_plugins.py` | Beginner+ | Reusable plugin functions |
| `level4_pipelines.py` | Intermediate | Multi-step AI pipelines |
| `level5_memory.py` | Intermediate | Stateful chatbot with memory |
| `run_all.py` | — | Run levels 1–4 in sequence |

```bash
python level1_hello_ai.py
python level2_prompt_templates.py
python level3_plugins.py
python level4_pipelines.py
python level5_memory.py   # interactive chatbot
python run_all.py         # run levels 1-4 together
```

## Project Structure

```
semantic_kernel_tutorial/
├── .env                        ← your API key (never commit)
├── .env.example                ← template
├── .gitignore
├── requirements.txt
├── run_all.py
├── level1_hello_ai.py
├── level2_prompt_templates.py
├── level3_plugins.py
├── level4_pipelines.py
└── level5_memory.py
```
