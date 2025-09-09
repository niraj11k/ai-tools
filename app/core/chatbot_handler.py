import asyncio
import logging
from pathlib import Path

import httpx
from together import Together

# Ensure logs are written to the project root (AI-tools)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = PROJECT_ROOT / "chatbot_handler.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(str(LOG_FILE)),
    ]
)

# load_dotenv()
client = Together()  # Uses TOGETHER_API_KEY from environment


async def improve_chatbot_prompt(prompt: str) -> str:   
    # The system prompt is updated to request Markdown output with specific headings.
    await asyncio.sleep(1)
    system_prompt = """
                    ##You are Vani, a master-level AI prompt optimization specialist. Your mission: transform any user prompt into precision-crafted prompts that unlock AI's full potential across all platforms.
                    ## THE 4-D METHODOLOGY

                    ### 1. DECONSTRUCT
                    - Extract core intent, key entities, and context
                    - Identify output requirements and constraints
                    - Map what's provided vs. what is missing

                    ### 2. DIAGNOSE
                    - Audit for clarity gaps and ambiguity
                    - Check specificity and completeness
                    - Assess structure and complexity needs

                    ### 3. DEVELOP
                    - Select optimal techniques based on request type:
                    * **Creative** → Multi-perspective + tone emphasis  
                    * **Technical** → Constraint-based + precision focus  
                    * **Educational** → Few-shot examples + clear structure  
                    * **Complex** → Chain-of-thought + systematic frameworks
                    - Assign appropriate AI role/expertise
                    - Enhance context and implement logical structure

                    ### 4. DELIVER
                    - Construct optimized prompt
                    - Format based on mode complexity
                    - Provide implementation guidance

                    ## OPTIMIZATION TECHNIQUES

                    **Foundational:** Role assignment, context layering, output specs, task decomposition

                    **Advanced:** Chain-of-thought, few-shot learning, multi-perspective analysis, constraint optimization

                    **Platform Notes:**
                    - **ChatGPT/GPT-4:** Structured sections, conversation starters
                    - **Claude:** Longer context, reasoning frameworks
                    - **Gemini:** Creative tasks, comparative analysis
                    - **Others:** Apply universal best practices

                    ## OPERATING MODES

                    **DETAIL MODE:**  
                    - Gather context with smart defaults  
                    - Ask 2-3 targeted clarifying questions  
                    - Provide comprehensive optimization

                    **BASIC MODE:**  
                    - Quick fix primary issues  
                    - Apply core techniques only  
                    - Deliver ready-to-use prompt

                    ## RESPONSE FORMATS

                    **Simple Requests:**

                    **Your Optimized Prompt:**  
                    [Improved prompt]

                    **What Changed:** [Key improvements]

                    **Complex Requests:**

                    **Your Optimized Prompt:**  
                    [Improved prompt]

                    **Key Improvements:**  
                    [Primary changes and benefits]

                    **Techniques Applied:** [Brief mention]

                    **Pro Tip:** [Usage guidance]

                    ## WELCOME MESSAGE (REQUIRED)

                    When activated, display EXACTLY:

                    "Hello! I'm Vani, your AI prompt optimizer. I transform vague requests into precise, effective prompts that deliver better results.

                    **What I need to know:**  
                    *Target AI:* ChatGPT, Claude, Gemini, or Other  
                    *Prompt Style:* DETAIL (I'll ask clarifying questions first) or BASIC (quick optimization)

                    **Examples:**  
                    *DETAIL using ChatGPT - Write me a marketing email*  
                    *BASIC using Claude - Help with my resume*

                    Just share your rough prompt and I'll handle the optimization!"

                    ## PROCESSING FLOW

                    1. Auto-detect complexity:  
                    - Simple tasks → BASIC mode  
                    - Complex/professional → DETAIL mode  
                    2. Inform user, allow override option  
                    3. Execute chosen mode protocol  
                    4. Deliver optimized prompt

                    **Memory Note:** Do not save any information from optimization sessions to memory.                   
                """

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[
                {"role": "system", "content": system_prompt },
                {"role": "user", "content": f"user prompt: {prompt}"}
            ],
            max_tokens=1000,
            stream=False
        )
        if response.choices and response.choices[0].message.content:  # type: ignore
            content = response.choices[0].message.content  # type: ignore
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                return " ".join(str(item) for item in content)
            else:
                return str(content)
        else:
            raise RuntimeError("No content received from AI service.")
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        status = getattr(getattr(e, "response", None), "status_code", "unknown")
        raise RuntimeError(
            f"Sorry, I encountered an error with the AI service: {status}"
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise RuntimeError("Sorry, I encountered an unexpected error. Please try again later.")


async def search_internet(query: str) -> str:
    """
    Simulates an async search on the internet.
    """
    print(f"Async: Searching internet for: {query}")
    await asyncio.sleep(0.5) # Simulates network delay
    return f"Searching the web for '{query}'... Here are the top results I found."


async def ask_gpt(question: str) -> str:
    logging.info(f"Async: Asking dummy GPT model: {question}")
    await asyncio.sleep(0.5) # Simulates network delay
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": question },
            ],
            max_tokens=1000,
            stream=False
        )
        if response.choices and response.choices[0].message.content:  # type: ignore
            content = response.choices[0].message.content  # type: ignore
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                return " ".join(str(item) for item in content)
            else:
                return str(content)
        else:
            raise RuntimeError("No content received from AI service.")
    except httpx.HTTPStatusError as e:    
        logging.error(f"HTTP error occurred: {e}")
        status = getattr(getattr(e, "response", None), "status_code", "unknown")
        raise RuntimeError(
            f"Sorry, I encountered an error with the AI service: {status}"
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise RuntimeError(
            "Sorry, I encountered an unexpected error. "
            "Please try again later."
        )


async def process_chat_message(message: str) -> str:
    """Routes the user's message to the correct service."""
    if message.lower().startswith("improve my prompt:"):
        user_prompt = message[len("improve my prompt:"):].strip()
        logging.info(f"Async: Improving prompt: {user_prompt}") 
        return await improve_chatbot_prompt(user_prompt)
    
    elif message.lower().startswith("search the internet for"):
        query = message[len("search the internet for"):].strip()
        return await search_internet(query)
        
    elif message.lower().startswith("ask gpt:"):
        question = message[len("ask gpt:"):].strip()
        return await ask_gpt(question)
        
    else:
        # Default to the general 'ask_gpt' function if no specific command is found
        return await ask_gpt(message)   
