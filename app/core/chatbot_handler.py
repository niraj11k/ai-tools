import logging
import httpx
from together import Together
import asyncio
import json
from ..models.chatbot_models import ChatbotResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("log/prompt-genie/chatbot_handler.log"),
        logging.StreamHandler()     
    ]   
)

client = Together()  # Uses TOGETHER_API_KEY from environment


def _safe_extract_content(response) -> str:
    """Best-effort extraction of text from Together SDK responses.
    Avoids subscripting None when choices/message may be missing.
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

async def improve_chatbot_prompt(prompt: str) -> ChatbotResponse:   
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
            # max_tokens=1000
        )
        return _safe_extract_content(response)
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise f"Sorry, I encountered an error with the AI service: {e.response.status_code}"
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise f"Sorry, I encountered an unexpected error. Please try again later."
async def search_internet(query: str) -> str:
    """
    Simulates an async search on the internet.
    """
    print(f"Async: Searching internet for: {query}")
    await asyncio.sleep(0.5) # Simulates network delay
    return f"Searching the web for '{query}'... Here are the top results I found."

async def ask_gpt(question: str) -> ChatbotResponse:
    logging.info(f"Async: Asking dummy GPT model: {question}")
    await asyncio.sleep(0.5) # Simulates network delay
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": question },
            ],
            max_tokens=1000
        )
        return _safe_extract_content(response)
    except httpx.HTTPStatusError as e:    
        logging.error(f"HTTP error occurred: {e}")
        raise f"Sorry, I encountered an error with the AI service: {e.response.status_code}"
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise f"Sorry, I encountered an unexpected error. Please try again later."
async def process_chat_message(message: str) -> str:
    """
    The main async handler function. It routes the user's message to the correct service.
    """
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
