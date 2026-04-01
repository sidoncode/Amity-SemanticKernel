"""
run_all.py — Run Levels 1–4 back to back (non-interactive demo).

Level 5 is a live chatbot and must be run separately:
    python level5_memory.py

Run this file:
    python run_all.py
"""

import asyncio

import level1_hello_ai
import level2_prompt_templates
import level3_plugins
import level4_pipelines


async def main():
    print("\n" + "🔷" * 25)
    print("  SEMANTIC KERNEL — Full Tutorial Run")
    print("🔷" * 25 + "\n")

    await level1_hello_ai.main()
    print()
    await level2_prompt_templates.main()
    print()
    await level3_plugins.main()
    print()
    await level4_pipelines.main()

    print("=" * 50)
    print("  All levels complete!")
    print("  Run level5_memory.py for the interactive chatbot.")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
