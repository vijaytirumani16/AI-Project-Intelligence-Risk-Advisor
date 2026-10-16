import os

from dotenv import load_dotenv
from google import genai
from groq import Groq
from openai import OpenAI

load_dotenv()


def generate_gemini_response(prompt):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found.")

    client = genai.Client(api_key=api_key)

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text


def generate_groq_response(prompt):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def generate_openrouter_response(prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def generate_response(prompt):
    """
    Generate an AI response using multiple LLM providers.

    Priority:
    1. Groq
    2. Gemini
    3. OpenRouter
    """

    # ---------------------------------------------------------
    # Try Groq first
    # ---------------------------------------------------------

    try:
        print("Trying Groq...")

        response = generate_groq_response(prompt)

        print("Response generated using Groq.")

        return response

    except Exception as groq_error:

        print(f"Groq unavailable: {groq_error}")
        print("Falling back to Gemini...")


    # ---------------------------------------------------------
    # Try Gemini
    # ---------------------------------------------------------

    try:
        print("Trying Gemini...")

        response = generate_gemini_response(prompt)

        print("Response generated using Gemini.")

        return response

    except Exception as gemini_error:

        print(f"Gemini unavailable: {gemini_error}")
        print("Falling back to OpenRouter...")


    # ---------------------------------------------------------
    # Try OpenRouter
    # ---------------------------------------------------------

    try:
        print("Trying OpenRouter...")

        response = generate_openrouter_response(prompt)

        print("Response generated using OpenRouter.")

        return response

    except Exception as openrouter_error:

        print(f"OpenRouter unavailable: {openrouter_error}")

        raise RuntimeError(
            "All configured LLM providers failed.\n"
            f"Groq error: {groq_error}\n"
            f"Gemini error: {gemini_error}\n"
            f"OpenRouter error: {openrouter_error}"
        )