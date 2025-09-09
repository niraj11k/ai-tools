# app/prompt_creator.py
import os

from dotenv import load_dotenv
import requests
from together import Together


load_dotenv()
client = Together()  # Uses TOGETHER_API_KEY from environment

# Load API keys from .env
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def _safe_extract_content(response) -> str:
    """Best-effort extraction of text from Together SDK responses.
    Handles variations where choices/message/content may be missing or None.
    """
    try:
        choices = getattr(response, "choices", None)
        if choices:
            first = choices[0]
            msg = getattr(first, "message", None)
            if msg and getattr(msg, "content", None):
                return msg.content
            if getattr(first, "text", None):
                return first.text
        if isinstance(response, dict):
            ch = response.get("choices")
            if ch and isinstance(ch, list):
                first = ch[0]
                if isinstance(first, dict):
                    msg = first.get("message") or {}
                    if isinstance(msg, dict) and msg.get("content"):
                        return msg["content"]
                    if first.get("text"):
                        return first["text"]
        return ""
    except Exception:
        return ""

def create_prompt(task_description: str, provider: str) -> str:
    provider = provider.lower()
    """
    Takes a simple task description and uses an LLM to generate
    a structured, optimized prompt in Markdown format.
    """
    
    # The system prompt is updated to request Markdown output with specific headings.
    system_prompt = (
        "You are a senior prompt engineer. Transform the user's request into a "
        "structured,"
        " professional prompt in Markdown with the following sections:"
        "\n\n### Persona\nDescribe the relevant role."
        "\n\n### Task\nRewrite the user request as a clear instruction."
        "\n\n### Constraints\nList concrete requirements, acceptance criteria, "
        "and boundaries."
        "\n\n### Audience (include only if explicitly provided)"
        "\n\n### Tone & Style (include only if explicitly provided)"
    )

    try:
        if provider == "openai":
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": system_prompt },
                    {"role": "user", "content": f"user prompt: {task_description}"}
                ],
                
            )
            return _safe_extract_content(response)

        elif provider == "llama":
            url = "https://api.together.xyz/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You have to convert the user prompt prompt that will get an "
                            "output at a professional level. Assume an appropriate role "
                            "before sending me the prompt, review it yourself and optimize "
                            "to make it extremely detailed."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "Here is the user prompt: "
                            f"{task_description}"
                        ),
                    },
                ],
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

        elif provider == "gemma":
            response = client.chat.completions.create(
                model="google/gemma-3n-E4B-it",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"user prompt: {task_description}"}
                ]
            )
            return _safe_extract_content(response)

        else:
            return f"❌ Unknown provider: {provider}"

    except Exception as e:
        return f"❌ Error: {str(e)}"    
            
def create_short_prompt(task_description: str, provider: str) -> str:
    provider = provider.lower()
    try:
        if provider == "openai":
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You have to convert the user prompt that will get an output "
                            "at a professional level. Before sending me the prompt, review "
                            "it yourself and optimize to make it under 101 tokens."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "Here is the task for which "
                            "you need to optimize the prompt: "
                            f"{task_description}"
                        ),
                    },
                ],
                max_tokens=100,
            )
            return _safe_extract_content(response)
        elif provider == "llama":
            url = "https://api.together.xyz/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You have to convert the user prompt that will get an output "
                            "at a professional level. Before sending me the prompt, review "
                            "it yourself and optimize to make it under 101 tokens."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "Here is the task for which "
                            "you need to write the prompt: "
                            f"{task_description}"
                        ),
                    },
                ],
                "max_tokens": 100,
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        elif provider == "gemma":
            response = client.chat.completions.create(
                model="google/gemma-3n-E4B-it",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You have to convert the user prompt that will get an output "
                            "at a professional level. Before sending me the prompt, review "
                            "it yourself and optimize to make it under 101 tokens."
                        ),
                    },
                    {"role": "user", "content": f"user prompt: {task_description}"},
                ],
                max_tokens=100,
            )
            return _safe_extract_content(response)
        else:
            return "Provider not supported."
    except Exception as e:
        return f"Error: {str(e)}"
