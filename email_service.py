
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from prompt_templates import email_prompt

load_dotenv()


def generate_email_reply(email: str, tone: str) -> str:
    """Generate an email reply using the selected tone."""

    if not os.getenv("GROQ_API_KEY"):
        raise ValueError(
            "GROQ_API_KEY is missing. Check your .env file."
        )

    if not email or not email.strip():
        raise ValueError("Please provide an email.")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=500,
    )

    # Connect the prompt template to the language model.
    chain = email_prompt | llm

    # Fill {email} and {tone}, then invoke the LLM.
    response = chain.invoke({
        "email": email.strip(),
        "tone": tone,
    })

    return response.content
