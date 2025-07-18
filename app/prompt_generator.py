# app/prompt_creator.py
import os
import requests
from dotenv import load_dotenv
from together import Together


load_dotenv()
client = Together()  # Uses TOGETHER_API_KEY from environment

# Load API keys from .env
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
# def clean_deepseek_response(text: str) -> str:
#     # Remove everything between <think> and </think>, including the tags
#     return re.sub(r"<think[\s\S]*?</think>", "", text, flags=re.IGNORECASE).strip()

def create_prompt(task_description: str, provider: str) -> str:
    provider = provider.lower()
    """
    Takes a simple task description and uses an LLM to generate
    a structured, optimized prompt in Markdown format.
    """
    
    # The system prompt is updated to request Markdown output with specific headings.
    system_prompt = """You are a highly experienced prompt engineer and AI architect. Your sole function is to act as a "Prompt Optimizer." You will receive a simple user request and must instantly re-engineer it into a sophisticated, structured prompt. This new prompt must be designed to guide another AI to produce a clear, accurate, and non-hallucinatory result.
                    **Your Task:**
                    Analyze the user's simple request. Based on this analysis construct a new, detailed prompt.
                    **Your Output MUST adhere to the following strict rules:**
                    1.  **Format:** The entire output must be formatted using Markdown. Do not include any text, greetings, or explanations before or after the Markdown content.
                    2.  **Markdown Structure:** The prompt must be organized with the following H3 (###) headings:
                        * `### Persona`: **(Mandatory)** Assume a appropirate role based on the task description.
                            For example, 
                            if the task is related to cooking, assume a "Chef" persona.
                            If the task is related to software development, assume a "Developer" or "Engineer" persona.
                            If the task is related to Website or app development, assume a "Web Developer" persona.
                            If the task is related to design, assume a "Designer" or "Creative professional" persona.
                            If the task is related to wireframe or mockup creation, assume a "UI/UX Designer" persona.
                            If the task is related to data analysis, assume a "Data Analyst" or "Data Scientist" persona.
                            If the task is related to education, assume a "Tutor" or "Mentor" persona.
                            If the task is related to health, assume a "Health professional" persona.
                            If the task is related to writing, assume a "Writer" or "Author" persona.
                            If the task is related to marketing, assume a "Marketing professional" persona.
                            If the task is related to business, assume a "Business consultant" persona.
                            If the task is related to finance, assume a "Financial advisor" persona.
                            If the task is related to art, assume an "Artist" or "Designer" persona.
                            If the task is related to science, assume a "Scientist" or "Researcher" persona.
                            If the task is related to law, assume a "Lawyer" or "Legal expert" persona.
                            If the task is related to technology, assume a "Tech expert" or "Engineer" persona.
                            If the task is related to travel, assume a "Travel expert" or "Tour guide" persona.
                            If the task is related to history, assume a "Historian" or "Archaeologist" persona.
                            If the task is related to psychology, assume a "Psychologist" or "Counselor" persona.
                            If the task is related to sports, assume a "Coach" or "Athlete" persona.
                            If the task is related to music, assume a "Musician" or "Composer" persona.
                            If the task is related to language, assume a "Linguist" or "Language expert" persona.
                            If the task is related to any other field, assume a relevant persona that fits the task description.
                            The persona should be specific and relevant to the task.
                        * `### Task`: **(Mandatory)** Rewrite the user's request into a clear, direct, and unambiguous instruction.
                        * `### Constraints`: **(Mandatory)** List any constraints or requirements for the AI's response.
                        * `### Audience`: **(Optional)** Only include this section if the original user prompt explicitly mentions a target audience.
                        * `### Tone & Style`: **(Optional)** Only include this section if the original user prompt explicitly mentions a desired tone or style.
                    **Example Transformation:**
                        If the user prompt is "Recipe for butter chicken", your required Markdown output would be:
                        ### Persona
                            #You are a world-class chef from Northern India, specializing in authentic Mughlai cuisine. You are an expert at making recipes easy to follow for home cooks.
                        ### Task
                            # Provide a clear, step-by-step recipe for making authentic Butter Chicken (Murgh Makhani). Include a list of ingredients with quantities and detailed cooking instructions.
                    Now, review the user prompt yourself and convert it to a optimized prompt to make sure it is clear, direct, and unambiguous. Once you've optimized the prompt, continue that follows and generate the Markdown output immediately, following all rules without exception."""

    try:
        if provider == "vision":
            response = client.chat.completions.create(
                model="meta-llama/Llama-Vision-Free",
                messages=[
                    {"role": "system", "content": system_prompt },
                    {"role": "user", "content": f"user prompt: {task_description}"}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content

        elif provider == "together":
            url = "https://api.together.xyz/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                "messages": [
                    {"role": "system", "content": "You have to convert the user prompt prompt that will get an output at a professional level. Assume a appropirate role before sending me the prompt, review it yourself and optimize to make it extremely detailed."},
                    {"role": "user", "content": f"Here is the user prompt: {task_description}"}
                ]
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

        elif provider == "mistral":
            response = client.chat.completions.create(
                model="mistralai/Mistral-7B-Instruct-v0.1",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"user prompt: {task_description}"}
                ]
            )
            output = response.choices[0].message.content
            # output = clean_deepseek_response(output)
            return output

        else:
            return f"❌ Unknown provider: {provider}"

    except Exception as e:
        return f"❌ Error: {str(e)}"    
            
def create_short_prompt(task_description: str, provider: str) -> str:
    provider = provider.lower()
    try:
        if provider == "vision":
            response = client.chat.completions.create(
                model="meta-llama/Llama-Vision-Free",
                messages=[
                    {"role": "system", "content": "You have to convert the user prompt that will get an output at a professional level. Before sending me the prompt, review it yourself and optimize to make it under 101 tokens." },
                    {"role": "user", "content": f"Here is the task for which you need to optimize the prompt:: {task_description}"}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content
        elif provider == "together":
            url = "https://api.together.xyz/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                "messages": [
                    {"role": "system", "content": "You have to convert the user prompt that will get an output at a professional level. Before sending me the prompt, review it yourself and optimize to make it under 101 tokens."},
                    {"role": "user", "content": f"Here is the task for which you need to write the prompt: {task_description}"}
                ],
                "max_tokens": 100
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        elif provider == "mistral":
            response = client.chat.completions.create(
                model="mistralai/Mistral-7B-Instruct-v0.1",
                messages=[
                    {"role": "system", "content": "You have to convert the user prompt that will get an output at a professional level. Before sending me the prompt, review it yourself and optimize to make it under 101 tokens." },
                    {"role": "user", "content": f"user prompt: {task_description}"}
                ],
                max_tokens=100
            )
            output = response.choices[0].message.content
            # output = clean_deepseek_response(output)
            return output
        else:
            return "Provider not supported."
    except Exception as e:
        return f"Error: {str(e)}"
